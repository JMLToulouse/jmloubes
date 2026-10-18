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
