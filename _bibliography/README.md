# Publications

The Research page (`/research/`) is built automatically from the BibTeX files in this folder.

## Adding a publication

1. Add the BibTeX entry to any `.bib` file here (for example `new.bib`; all `.bib` files are read).
2. Give it a `theme` field with one or more themes, separated by `;`:

   ```bibtex
   @inproceedings{doe2026fair,
     title     = {A Fair Paper},
     author    = {Doe, Jane and Loubes, Jean-Michel},
     booktitle = {International Conference on Machine Learning (ICML)},
     year      = {2026},
     theme     = {Machine Learning; Optimal Transport},
     url       = {https://arxiv.org/abs/2601.01234},
   }
   ```

3. Commit and push. The *Build publication list* GitHub Action regenerates
   `_data/publications.json` and the site updates.

To preview locally, run `python3 scripts/build_publications.py` from the repository root.

## Themes

Use the names (or slugs) defined in `_data/research_themes.yml`:

| Theme | Slug |
|---|---|
| Evaluation of AI | `evaluation-of-ai` |
| Machine Learning | `machine-learning` |
| Optimal Transport | `optimal-transport` |
| Statistics and Data Science | `statistics-and-data-science` |
| Industrial Projects | `industrial-projects` |

An entry with no valid theme is skipped, and the build prints a warning.
To add or rename a theme, edit `_data/research_themes.yml`.

## Publication type (colour code)

| Type | Colour | Inferred from |
|---|---|---|
| Journal | blue | `@article`, `@incollection`, `@book` |
| Conference | purple | `@inproceedings`, `@conference` |
| Preprint | amber | `@unpublished`, `@techreport`, `@misc`, or an `@article` whose journal is arXiv |
| Patent | red | `@patent` (use `holder` for the applicants and `number` for the patent number) |

Force a type with `pubtype = {preprint}` (or `journal`, `conference`, `patent`). Once a preprint
is accepted, change its entry type or `pubtype` and its venue.

## Optional fields used on the page

`doi`, `url`, `pdf`, `eprint` (arXiv id), `code` (link to a repository), `month`.
The author whose name contains "Loubes" is shown in bold.

## Files

- `publications.bib` — the full list, merged from HAL and Google Scholar on 2026-10-17;
  the themes were proposed automatically and should be checked.
