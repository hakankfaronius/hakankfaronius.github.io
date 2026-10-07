# Håkan Karlsson Faronius — research homepage

A small, responsive academic homepage for GitHub Pages. It works without JavaScript, external fonts, dependencies, tracking, or a backend. The ready-to-publish files are `index.html`, `styles.css`, `favicon.svg`, and `.nojekyll` at the repository root.

## Publish on GitHub Pages

1. Create a repository named `YOUR-USERNAME.github.io`, replacing `YOUR-USERNAME` with your GitHub username in lowercase. Use a public repository if you are using GitHub Free.
2. Upload the **contents** of this folder to its `main` branch. Keep `index.html` at the repository root, rather than inside another folder. No build or Actions configuration is required.
3. Open **Settings → Pages**. Under **Build and deployment**, select **Deploy from a branch**, then **main** and **/(root)**, and save.
4. GitHub will show the published URL, normally `https://YOUR-USERNAME.github.io/`. Publication may take up to 10 minutes.

Official instructions: https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site

An ordinary project repository also works: relative asset links support `https://YOUR-USERNAME.github.io/REPOSITORY/`.

## Update your homepage

Edit `content.json`, then run this from the repository folder:

```bash
python3 build.py
```

Commit `content.json` and the regenerated `index.html` together. GitHub Pages serves the already generated HTML; it does not need to run Python. `dist/` is an identical deployment copy for the hosted preview and can be omitted from the GitHub repository. You can also edit `index.html` directly for small changes, but running `build.py` again replaces those changes with the content in `content.json`.

### Add a project

Replace the empty `projects` array with your actual projects, for example:

```json
"projects": [
  {
    "title": "YOUR REAL PROJECT TITLE",
    "year": "YEAR",
    "description": "A short description of work you have done.",
    "url": "",
    "github_url": "https://github.com/YOUR-USERNAME/YOUR-REPOSITORY"
  }
]
```

The example above is only an editing template; it is not included in the website. Leave `url` empty if the repository is the only link. Add more objects separated by commas for additional projects.

### Add code links to your paper or theses

Set the relevant entry's `github_url` to the actual repository URL. The page automatically adds a **Code on GitHub** link. Blank URLs are hidden, so no placeholder buttons appear.

### Add a published article

Add an object to `publications` with `title`, `authors`, `year`, `venue`, `description`, `url`, and optional `pdf_url` and `github_url`. If an existing preprint is published, update or move its record as appropriate.

### Add personal details

The optional top-level `github_url`, `affiliation`, and `email` fields are empty. Set them only to details you want to make public. You can change the display name and research paragraphs in the same file.

## Content and verification

The site contains one supplied arXiv preprint and two supplied Uppsala University degree projects. Published articles and projects are empty. No current affiliation, contact address, GitHub account, additional papers, or repositories have been assumed. See `SOURCES.md` for the verified bibliographic sources.

## Local viewing

Open `index.html` directly in a browser. There is no setup step for viewing the site.
