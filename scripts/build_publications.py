#!/usr/bin/env python3
"""Build _data/publications.json from the BibTeX files in _bibliography/.

Every entry needs a `theme` field naming one or more research themes from
_data/research_themes.yml, separated by commas or semicolons:

    theme = {Optimal Transport; Machine Learning},

The publication type (preprint / journal / conference / patent) is inferred
from the entry type, and can be forced with `pubtype = {preprint}`.

Only the Python standard library is used, so the script runs as is:

    python3 scripts/build_publications.py
"""

import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BIB_DIR = ROOT / "_bibliography"
THEMES_FILE = ROOT / "_data" / "research_themes.yml"
OUT_FILE = ROOT / "_data" / "publications.json"
TIMELINE_FILE = ROOT / "_data" / "theme_timeline.json"

HIGHLIGHT_AUTHOR = "Loubes"

MONTHS = {m: i + 1 for i, m in enumerate(
    ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"])}

ARXIV_ID = re.compile(r"arxiv[^\d]{0,12}(\d{4}\.\d{4,5})", re.I)
PREPRINT_VENUE = re.compile(r"arxiv|preprint|submitted|working paper|hal\b", re.I)


# --------------------------------------------------------------------------
# Themes
# --------------------------------------------------------------------------

def theme_names():
    """Theme slugs and names in display order."""
    names, slug = [], None
    for line in THEMES_FILE.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\s*-?\s*(name|slug):\s*(.+?)\s*$", line)
        if m and m.group(1) == "name":
            names.append([None, m.group(2).strip("\"'")])
        elif m and m.group(1) == "slug":
            names[-1][0] = m.group(2).strip("\"'")
    return names


def timeline(pubs):
    """Publications per theme and per year, for the chart on the Publications page."""
    years = [p["year"] for p in pubs if p["year"] > 0]
    span = list(range(min(years), max(years) + 1))
    themes = []
    for slug, name in theme_names():
        counts = [sum(1 for p in pubs if p["year"] == y and slug in p["themes"]) for y in span]
        themes.append({"slug": slug, "name": name, "counts": counts, "total": sum(counts)})
    return {"years": span, "themes": themes}


def load_themes():
    """Read name/slug pairs from the themes YAML (flat list, no PyYAML needed)."""
    themes, current = [], {}
    for line in THEMES_FILE.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\s*-?\s*(name|slug):\s*(.+?)\s*$", line)
        if not m:
            continue
        if m.group(1) == "name" and current:
            themes.append(current)
            current = {}
        current[m.group(1)] = m.group(2).strip("\"'")
    if current:
        themes.append(current)
    lookup = {}
    for t in themes:
        lookup[t["name"].lower()] = t["slug"]
        lookup[t["slug"].lower()] = t["slug"]
    return lookup


# --------------------------------------------------------------------------
# BibTeX parsing
# --------------------------------------------------------------------------

def read_braced(text, i):
    """Return (content, next_index) for a {...} group starting at text[i]."""
    depth, start = 0, i
    while i < len(text):
        c = text[i]
        if c == "\\":
            i += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return text[start + 1:i], i + 1
        i += 1
    raise ValueError("unbalanced braces")


def read_quoted(text, i):
    """Return (content, next_index) for a "..." value starting at text[i]."""
    depth, j = 0, i + 1
    while j < len(text):
        c = text[j]
        if c == "\\":
            j += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
        elif c == '"' and depth == 0:
            return text[i + 1:j], j + 1
        j += 1
    raise ValueError("unterminated quoted value")


def parse_fields(body):
    fields, i = {}, 0
    while i < len(body):
        m = re.compile(r"\s*,?\s*([\w\-:.]+)\s*=\s*").match(body, i)
        if not m:
            break
        name, i = m.group(1).lower(), m.end()
        parts = []
        while i < len(body):
            if body[i] == "{":
                value, i = read_braced(body, i)
            elif body[i] == '"':
                value, i = read_quoted(body, i)
            else:
                v = re.compile(r"[^,#}\s]+").match(body, i)
                value, i = v.group(0), v.end()
            parts.append(value)
            m2 = re.compile(r"\s*#\s*").match(body, i)
            if not m2:
                break
            i = m2.end()
        fields[name] = "".join(parts)
    return fields


def parse_bibtex(text):
    entries, i = [], 0
    pattern = re.compile(r"@(\w+)\s*\{")
    while True:
        m = pattern.search(text, i)
        if not m:
            break
        etype = m.group(1).lower()
        body, i = read_braced(text, m.end() - 1)
        if etype in ("comment", "string", "preamble"):
            continue
        key, _, rest = body.partition(",")
        entries.append({"type": etype, "key": key.strip(), "fields": parse_fields(rest)})
    return entries


# --------------------------------------------------------------------------
# LaTeX to text
# --------------------------------------------------------------------------

ACCENTS = {"'": "\u0301", "`": "\u0300", "^": "\u0302", '"': "\u0308", "~": "\u0303",
           "=": "\u0304", ".": "\u0307", "c": "\u0327", "u": "\u0306", "v": "\u030c",
           "H": "\u030b", "k": "\u0328", "r": "\u030a"}
SPECIALS = {"ss": "ß", "o": "ø", "O": "Ø", "ae": "æ", "AE": "Æ", "oe": "œ", "OE": "Œ",
            "aa": "å", "AA": "Å", "l": "ł", "L": "Ł", "i": "ı", "j": "ȷ"}


def latex_to_text(s):
    if not s:
        return ""
    s = re.sub(r"\\([cuvHkr])\s+(\w)", r"\\\1{\2}", s)       # \c c  -> \c{c}

    def accent(m):
        base = m.group(2) or m.group(3)
        base = {"\\i": "i", "\\j": "j"}.get(base, base)
        return base + ACCENTS[m.group(1)]
    s = re.sub(r"\\(['`^\"~=.cuvHkr])\s*(?:\{\s*(\\?\w)\s*\}|(\\[ij](?![a-zA-Z])|\w))", accent, s)
    s = re.sub(r"\\(ss|o|O|ae|AE|oe|OE|aa|AA|l|L|i|j)(?![a-zA-Z])\s*",
               lambda m: SPECIALS[m.group(1)], s)
    s = s.replace("\\&", "&").replace("\\%", "%").replace("\\_", "_").replace("\\$", "$").replace("\\#", "#")
    s = s.replace("---", "—").replace("--", "–").replace("~", " ")
    s = re.sub(r"\\(emph|textit|textbf|textsc|textrm|mathrm|mathcal|mathbb|text)\s*", "", s)
    s = re.sub(r"\\([a-zA-Z]+)", r"\1", s)                    # leftover commands: keep the word
    s = s.replace("{", "").replace("}", "").replace("$", "")
    s = re.sub(r"\s+", " ", s).strip()
    return unicodedata.normalize("NFC", s)


# --------------------------------------------------------------------------
# Entry conversion
# --------------------------------------------------------------------------

def format_author(name):
    name = latex_to_text(name)
    if "," in name:
        last, first = [p.strip() for p in name.split(",", 1)]
        name = f"{first} {last}".strip()
    return name


def pub_type(etype, f):
    forced = f.get("pubtype", "").strip().lower()
    if forced in ("preprint", "journal", "conference", "patent"):
        return forced
    if etype == "patent":
        return "patent"
    if etype in ("inproceedings", "conference", "proceedings"):
        return "conference"
    if etype in ("article", "incollection", "inbook", "book"):
        if PREPRINT_VENUE.search(f.get("journal", "")) and not f.get("volume"):
            return "preprint"
        return "journal"
    return "preprint"            # unpublished, techreport, misc, phdthesis, ...


def venue(etype, kind, f):
    if kind == "patent":
        return latex_to_text(" — ".join(x for x in (f.get("holder", ""), f.get("number", "")) if x))
    v = f.get("journal") or f.get("booktitle") or ""
    if not v and kind == "preprint":
        v = f.get("institution") or ("arXiv" if f.get("eprint") or "arxiv" in f.get("url", "").lower() else "")
    return latex_to_text(v)


def month_num(raw):
    raw = (raw or "").strip().lower()[:3]
    if raw.isdigit():
        return int(raw)
    return MONTHS.get(raw, 0)


def convert(entry, themes, source):
    f, etype = entry["fields"], entry["type"]
    raw_themes = [t.strip() for t in re.split(r"[;,]", f.get("theme", "")) if t.strip()]
    slugs, unknown = [], []
    for t in raw_themes:
        slug = themes.get(latex_to_text(t).lower())
        (slugs if slug else unknown).append(slug or t)
    if unknown:
        print(f"  ! {source}: {entry['key']}: unknown theme(s) {unknown}", file=sys.stderr)
    if not slugs:
        print(f"  ! {source}: {entry['key']}: no valid theme, entry skipped", file=sys.stderr)
        return None

    kind = pub_type(etype, f)
    doi = f.get("doi", "").strip()
    url = f.get("url", "").strip()
    authors = [format_author(a) for a in re.split(r"\s+and\s+", f.get("author", "")) if a.strip()]
    year = re.sub(r"\D", "", f.get("year", ""))[:4]
    arxiv = ARXIV_ID.search(" ".join(["arxiv:" + f.get("eprint", ""), f.get("journal", ""), url, f.get("note", "")]))
    return {
        "key": entry["key"],
        "type": kind,
        "themes": slugs,
        "title": latex_to_text(f.get("title", "")),
        "authors": authors,
        "me": [HIGHLIGHT_AUTHOR in a for a in authors],
        "venue": venue(etype, kind, f),
        "year": int(year) if year else 0,
        "month": month_num(f.get("month")),
        "doi": doi,
        "url": f"https://doi.org/{doi}" if doi else url,
        "pdf": f.get("pdf", "").strip(),
        "hal": url if "hal." in url else "",
        "arxiv": arxiv.group(1) if arxiv else "",
        "code": f.get("code", "").strip(),
    }


def main():
    themes = load_themes()
    pubs, seen = [], set()
    files = sorted(BIB_DIR.glob("*.bib"))
    for path in files:
        entries = parse_bibtex(path.read_text(encoding="utf-8"))
        for e in entries:
            if e["key"] in seen:
                print(f"  ! {path.name}: duplicate key {e['key']}, entry skipped", file=sys.stderr)
                continue
            p = convert(e, themes, path.name)
            if p:
                seen.add(e["key"])
                pubs.append(p)
    pubs.sort(key=lambda p: (-p["year"], -p["month"], p["title"].lower()))
    OUT_FILE.write_text(json.dumps(pubs, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    TIMELINE_FILE.write_text(json.dumps(timeline(pubs), ensure_ascii=False) + "\n", encoding="utf-8")
    counts = {k: sum(p["type"] == k for p in pubs) for k in ("journal", "conference", "preprint", "patent")}
    print(f"{len(pubs)} publications from {len(files)} file(s) -> {OUT_FILE.relative_to(ROOT)} {counts}")


if __name__ == "__main__":
    main()
