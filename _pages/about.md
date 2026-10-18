---
layout: onepage
permalink: /
redirect_from:
  - /about/
  - /about.html
---

{% comment %}
  Home page. The sections are filled from:
    News        -> _data/news.yml
    Selected    -> _data/selected_publications.yml (full list: _pages/publications.html)
    Teaching    -> _data/teaching.yml
    Curriculum  -> _data/curriculum.yml
    Links (top) -> _data/links.yml
{% endcomment %}

<div id="toptitle">
  <h1>Jean-Michel Loubes</h1>
</div>

<div class="presentation">
  <img src="{{ '/images/jmloubes.jpg' | relative_url }}" alt="Jean-Michel Loubes" width="200">
  <div class="presentation__text">
    <ul>
      <li>Research Director @ <a href="https://www.inria.fr/en" target="_blank" rel="noopener noreferrer">Inria</a>,
        on leave from Professor of Mathematics (Exceptional Class) at the <a href="https://www.univ-tlse3.fr/home" target="_blank" rel="noopener noreferrer">University of Toulouse</a>,
        <a href="https://www.math.univ-toulouse.fr/en/" target="_blank" rel="noopener noreferrer">Institut de Mathématiques de Toulouse</a>.</li>
      <li>Head of the <a href="https://team.inria.fr/regaliasite/" target="_blank" rel="noopener noreferrer">Regalia</a> Lab (Regulation of AI).</li>
      <li>Principal Investigator, Chair <a href="https://aniti.univ-toulouse.fr/en/hybridizing-ai-and-large-scale-simulations-for-engineering-design-2/" target="_blank" rel="noopener noreferrer">TRIAL</a> (Trustworthy AI &amp; Machine Learning) @ <a href="https://aniti.univ-toulouse.fr/" target="_blank" rel="noopener noreferrer">ANITI</a>.</li>
      <li>Scientific Direction at the French AI Safety Institute (<a href="https://www.sgdsn.gouv.fr/notre-organisation/composantes/institut-national-pour-levaluation-et-la-securite-de-lintelligence" target="_blank" rel="noopener noreferrer">INESIA</a>) and Director of the national program on AI evaluation.</li>
    </ul>
    <p><strong>Expertise:</strong> Mathematical Statistics, Machine Learning, Optimal Transport, Evaluation of Artificial Intelligence, Trustworthy AI (Fairness, Robustness, Reliability and Explainability).</p>
    <p><strong>Contact:</strong><br>✉ jean-michel.loubes@inria.fr</p>
  </div>
</div>

<div class="section" id="news">
  <h2>News</h2>
  <ul>
    {% for n in site.data.news %}
      <li><strong>{{ n.date }}</strong> {{ n.text }}</li>
    {% endfor %}
  </ul>
</div>

<div class="section" id="curriculum">
  <h2>Curriculum</h2>
  {% for group in site.data.curriculum %}
    <h3 class="cv-heading">{{ group.section }}</h3>
    <ul>
      {% for c in group.items %}
        <li><strong>{{ c.years }}:</strong> {{ c.text }}
          {% if c.items %}
            <ul>
              {% for i in c.items %}
                <li><strong>{{ i.years }}:</strong> {{ i.text }}</li>
              {% endfor %}
            </ul>
          {% endif %}
        </li>
      {% endfor %}
    </ul>
  {% endfor %}
  <p>A detailed CV is available <a href="{{ '/cv/' | relative_url }}">here</a>.</p>
</div>

<div class="section" id="research">
  <h2>Research</h2>
  <p>
    Trained as a mathematician, I began by modelling complex systems driven by randomness: building statistical
    models that estimate their structure and forecast their behaviour, from road traffic to inverse problems and
    deformations of curves and distributions. This work has always been tied to industry, which I see both as a
    field of application for mathematics and as a source of new mathematical problems.
  </p>
  <p>
    My work then moved to <a href="{{ '/publications/' | relative_url }}#machine-learning">machine learning</a>, with
    applications in industry and biology: anomaly detection and predictive maintenance in aerospace and manufacturing,
    and the analysis of genomic and metagenomic data. These collaborations led to
    <a href="{{ '/publications/' | relative_url }}#industrial-projects">industrial patents</a> and to more than fifteen
    research contracts and industrial PhDs with partners such as Airbus (EADS), Continental, Michelin, L'Oréal,
    Total, EDF and Liebherr Aerospace.
  </p>
  <p>
    As machine learning came to make decisions that affect people, I turned to <strong>trustworthy AI</strong>:
    robustness, bias and fairness, and explainability, using tools such as
    <a href="{{ '/publications/' | relative_url }}#optimal-transport">optimal transport</a> and sensitivity analysis.
    A better AI is not only a mathematical question, so this work is multidisciplinary, carried out with lawyers,
    economists and specialists of governance and regulation.
  </p>
  <p>
    Today my research focuses on the <a href="{{ '/publications/' | relative_url }}#evaluation-of-ai">evaluation of AI</a>.
    Evaluation is the starting point for a better and safer AI: a system can only be trusted, regulated or improved once
    its behaviour can be measured. This is the aim of the Regalia team at Inria and of the national program on AI
    evaluation at INESIA.
  </p>
</div>

<div class="section" id="selected">
  <h2>Selected publications</h2>
  {% for topic in site.data.selected_publications %}
    <div class="selected-topic">
      <h3>{{ topic.title }}</h3>
      {% if topic.intro %}<p>{{ topic.intro }}</p>{% endif %}
      <ol class="pub-list">
        {% for key in topic.keys %}
          {% assign p = site.data.publications | where: "key", key | first %}
          {% if p %}{% include pub-item.html %}{% endif %}
        {% endfor %}
      </ol>
    </div>
  {% endfor %}
  <p class="more-link"><a href="{{ '/publications/' | relative_url }}">→ All publications, by research theme</a></p>
</div>

<div class="section" id="teaching">
  <h2>Teaching</h2>
  <ul>
    {% for t in site.data.teaching %}
      <li><strong>{{ t.title }}:</strong> {{ t.text }}</li>
    {% endfor %}
  </ul>
  {% assign current = site.data.phd_students | where: "status", "current" %}
  {% assign former = site.data.phd_students | where: "status", "former" %}
  <h3 class="cv-heading">PhD students</h3>
  <p><strong>Current:</strong>
    {% for st in current %}{{ st.name }}{% if st.context != "" %} ({{ st.context }}){% endif %}{% unless forloop.last %}; {% endunless %}{% endfor %}.</p>
  <p><strong>Former ({{ former | size }}):</strong>
    {% for st in former %}{{ st.name }}{% unless forloop.last %}, {% endunless %}{% endfor %}.</p>
  <p class="more-link"><a href="{{ '/students/' | relative_url }}">→ Full list with thesis titles, dates and current positions</a></p>

  <h3 class="cv-heading">Resources</h3>
  <ul>
    {% for r in site.data.resources %}
      <li><a href="{{ r.url }}" target="_blank" rel="noopener noreferrer">{{ r.title }}</a> — {{ r.source }}</li>
    {% endfor %}
  </ul>
  <h3 class="cv-heading">In the press</h3>
  <ul>
    {% for r in site.data.press %}
      <li><a href="{{ r.url }}" target="_blank" rel="noopener noreferrer">{{ r.title }}</a> — <em>{{ r.source }}</em>{% if r.date %}, {{ r.date }}{% endif %}</li>
    {% endfor %}
  </ul>
</div>
