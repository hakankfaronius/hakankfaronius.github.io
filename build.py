#!/usr/bin/env python3
"""Generate a dependency-free, GitHub Pages-compatible research homepage."""
import html
import json
from pathlib import Path
import shutil
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent

def esc(value):
    return html.escape(str(value), quote=True)

def link(url, label):
    if not url:
        return ""
    parsed = urlparse(url)
    if parsed.scheme not in ("https", "http", "mailto"):
        raise ValueError(f"Unsupported URL scheme: {url}")
    return f'<a href="{esc(url)}">{esc(label)}</a>'

def work(item, section):
    title = link(item.get("url", ""), item["title"]) or esc(item["title"])
    if section == "theses":
        meta = f'{esc(item["kind"])} · {esc(item["institution"])}'
    else:
        meta = esc(item.get("authors", ""))
        if item.get("venue"):
            meta += f'<br>{esc(item["venue"])}' if meta else esc(item["venue"])
    links = []
    if item.get("url"):
        label = "DiVA record" if section == "theses" else "arXiv" if section == "preprints" else "Project" if section == "projects" else "Article"
        links.append(link(item["url"], label))
    if item.get("pdf_url"):
        links.append(link(item["pdf_url"], "PDF"))
    if item.get("github_url"):
        links.append(link(item["github_url"], "Code on GitHub"))
    description = f'<p class="work-description">{esc(item["description"])}</p>' if item.get("description") else ""
    return f'''<article class="work">
      <div class="year">{esc(item.get("year", ""))}</div>
      <div><h3>{title}</h3>
      <p class="work-meta">{meta}</p>{description}
      <div class="work-links">{"".join(links)}</div></div>
    </article>'''

def build(data):
    sections = []
    for key, title, note, empty in [
        ("publications", "Published articles", "", "No published articles listed yet."),
        ("preprints", "Preprints", "Not peer-reviewed", "No preprints listed yet."),
        ("projects", "Projects & code", "", "Repository links will be added here."),
        ("theses", "Theses & degree projects", "", "No degree projects listed yet.")
    ]:
        items = "\n".join(work(item, key) for item in data[key])
        if not items:
            items = f'<p class="empty">{empty}</p>'
        annotation = f'<span class="section-note">{note}</span>' if note else ""
        sections.append(f'<section id="{key}" aria-labelledby="{key}-heading"><div class="section-heading"><h2 id="{key}-heading">{title}</h2>{annotation}</div>{items}</section>')
    profile_links = link(data.get("github_url", ""), "GitHub")
    if data.get("email"):
        profile_links += link("mailto:" + data["email"], "Email")
    profile_links = f'<div class="profile-links">{profile_links}</div>' if profile_links else ""
    affiliation = f'<p class="sidebar-label">{esc(data["affiliation"])}</p>' if data.get("affiliation") else ""
    intro = "".join(f'<p>{esc(p)}</p>' for p in data["research"])
    name = esc(data["name"])
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{name} | Research</title>
  <meta name="description" content="{name} — research on the mathematical foundations of neurosymbolic AI, probabilistic circuits, Bayesian networks, and reasoning shortcuts.">
  <meta name="theme-color" content="#fbfaf7">
  <meta property="og:title" content="{name} | Research">
  <meta property="og:description" content="Mathematical foundations of neurosymbolic AI. Research, preprints, projects, and theses.">
  <meta property="og:type" content="website">
  <link rel="icon" href="./favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="./styles.css">
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<div class="layout">
  <aside class="sidebar" aria-label="Profile and navigation">
    <div class="monogram" aria-hidden="true">HKF</div>
    <p class="sidebar-name">{name}</p>
    <p class="sidebar-label">Research homepage</p>{affiliation}{profile_links}
    <nav aria-label="Main navigation">
      <a href="#research">Research</a>
      <a href="#publications">Published articles</a>
      <a href="#preprints">Preprints</a>
      <a href="#projects">Projects & code</a>
      <a href="#theses">Theses & degree projects</a>
    </nav>
    <div class="sidebar-foot">Mathematics · Learning · Reasoning</div>
  </aside>
  <main id="main">
    <section id="research" aria-labelledby="research-heading">
      <p class="eyebrow">Neurosymbolic AI</p>
      <h1 id="research-heading">{name}</h1>
      <div class="intro">{intro}</div>
      <ul class="research-topics" aria-label="Core research topics">
        <li>Probabilistic circuits</li><li>Bayesian networks</li><li>Reasoning shortcuts</li>
      </ul>
    </section>
    {"".join(sections)}
    <footer><span>{name}</span><a href="#research">Back to top ↑</a></footer>
  </main>
</div>
</body>
</html>
'''

if __name__ == "__main__":
    data = json.loads((ROOT / "content.json").read_text(encoding="utf-8"))
    (ROOT / "index.html").write_text(build(data), encoding="utf-8")
    dist = ROOT / "dist"
    dist.mkdir(exist_ok=True)
    for filename in ("index.html", "styles.css", "favicon.svg", ".nojekyll"):
        shutil.copy2(ROOT / filename, dist / filename)
    print("Generated index.html and dist/ from content.json.")
