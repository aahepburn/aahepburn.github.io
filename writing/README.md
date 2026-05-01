# Writing section — Quiet Signals Lab

Technical longform pieces at `quietsignalslab.com/writing/`.

---

## How to publish a new post

### 1. Choose a slug

Pick a short, lowercase, hyphenated identifier for the post URL. Examples:

- `membership-inference-thresholds`
- `rag-retrieval-failures`
- `dp-sgd-utility-tradeoffs`

The slug becomes the directory name and the URL:
`/writing/<slug>/index.html` → served at `quietsignalslab.com/writing/<slug>/`

**Why directory-style URLs?** They survive server reconfigurations cleanly,
look better when shared, and GitHub Pages handles both `.html` and `/index.html`
forms — the directory form is preferred.

---

### 2. Copy the template

```bash
cp writing/_template.html writing/<slug>/index.html
```

---

### 3. Fill in the template

Open `writing/<slug>/index.html` and replace every `<!-- PLACEHOLDER -->` comment.
Required fields (search for these):

| Placeholder | What to fill in |
|---|---|
| `<!-- POST TITLE -->` | Title text (used in `<title>`, OG tags, JSON-LD, and `<h1>`) |
| `<!-- ONE-SENTENCE DESCRIPTION -->` | 120–160 chars for `<meta name="description">` |
| `<!-- SLUG -->` | The slug from step 1 |
| `<!-- YYYY-MM-DD -->` | Publication date (appears in three places) |
| `<!-- D Month YYYY -->` | Human-readable date e.g. `15 June 2026` |
| `<!-- ONE-LINE SUBTITLE -->` | Optional — delete the `<p class="post-subtitle">` if unused |

**Date format rationale:** Day-first long form ("15 June 2026") is used because
ISO-8601 ("2026-06-15") reads as bureaucratic in prose, and US month-first
("June 15, 2026") is unfamiliar to EU readers. The `datetime` attribute on
`<time>` always carries the machine-readable ISO date.

---

### 4. Write the content

Fill in the article body between the two `══` comment banners.

**Available elements:**

```html
<h2>Section heading</h2>
<h3>Sub-section heading</h3>
<h4>Run-in label</h4>
<p>Body paragraph.</p>

<ul>
    <li>List item</li>
</ul>

<blockquote>
    <p>Pull quote or extended quotation.</p>
</blockquote>

<!-- Code block (replace language-* class to match) -->
<pre><code class="language-python">
def example():
    pass
</code></pre>

<!-- Inline code -->
<code>some_function()</code>

<!-- Figure (column width) -->
<figure>
    <img src="figure.png" alt="Description" width="720" height="480">
    <figcaption>Figure N. Caption text.</figcaption>
</figure>

<!-- Wide figure (breaks out of text column) -->
<figure class="figure-wide">
    <img src="wide-figure.png" alt="Description" width="1200" height="600">
    <figcaption>Figure N. Wide caption.</figcaption>
</figure>
```

**Math** (KaTeX, loaded automatically):

```
Inline:  $\theta$ or \(\theta\)
Display: $$\mathcal{L}(\theta)$$ or \[\mathcal{L}(\theta)\]
```

**Footnotes:**

In body text:
```html
some claim<sup><a href="#fn1" id="ref1">1</a></sup>
```

At end of article, before the post footer:
```html
<aside class="footnotes" role="doc-endnotes">
    <h4>Notes</h4>
    <ol>
        <li id="fn1">
            Footnote text. <a href="#ref1" class="fn-back">↩</a>
        </li>
    </ol>
</aside>
```

**Supported Prism.js languages** (via autoloader — no extra configuration needed):
`python`, `bash`, `javascript`, `json`, `yaml`, `sql`, `rust`, `typescript`

---

### 5. Add figures and images

Place image files in the post directory alongside `index.html`:

```
writing/<slug>/
    index.html
    figure-1.png
    roc-curve.svg
    og-image.png        ← social preview, 1200×630px
```

Reference them with relative paths: `src="figure-1.png"`.

---

### 6. Update the writing index

Open `writing/index.html` and prepend a new `<li>` as the first item in
`<ol class="post-list">`. Copy the structure of the existing item:

```html
<li class="post-list-item">
    <a class="post-list-link" href="/writing/<slug>/">
        <h2 class="post-list-title">Post Title</h2>
        <p class="post-list-desc">One-sentence description.</p>
        <div class="post-list-meta">
            <time datetime="YYYY-MM-DD">D Month YYYY</time>
            <span class="sep" aria-hidden="true">·</span>
            <span>N min read</span>
        </div>
    </a>
</li>
```

Reading time: count words in the post body, divide by 200, round to nearest
minute. Or let the JS on the post page tell you and fill it in by hand.

---

### 7. Append to the RSS feed

Open `writing/feed.xml`. Copy the `[ITEM TEMPLATE]` comment block, fill in
the five fields, and insert it as the **first `<item>`** inside `<channel>`
(above any existing items). Then update `<lastBuildDate>` to the publish date.

To get RFC 2822 date format:
```bash
date -R   # macOS / Linux — outputs e.g. "Thu, 01 May 2026 00:00:00 +0000"
```

---

### 8. Commit and push

```bash
git add writing/<slug>/ writing/index.html writing/feed.xml
git commit -m "writing: publish '<Post Title>'"
git push origin main
```

GitHub Pages deploys in ~60 seconds. No build step.

---

## Naming conventions

| Thing | Convention | Example |
|---|---|---|
| Post slug | Lowercase, hyphens, no trailing slash in source | `dp-sgd-utility-tradeoffs` |
| Post directory | `writing/<slug>/` | `writing/dp-sgd-utility-tradeoffs/` |
| HTML file | Always `index.html` | `writing/dp-sgd-utility-tradeoffs/index.html` |
| Figure files | `figure-N.png` or descriptive | `roc-curve.svg` |
| OG image | `og-image.png` | — |
| Font files | `<family>-<subset>-<weight>.woff2` | `source-serif-4-latin-400.woff2` |

---

## Gotchas

- **`<h1>` is used once per page**, for the post title only. Do not use `<h1>`
  inside article body. Use `<h2>` for top-level sections.

- **Math delimiters**: KaTeX auto-render is configured to handle `$...$` and
  `$$...$$`. If you need a literal dollar sign, escape it: `\$`. If a paragraph
  starts with `$`, it will be treated as math — rephrase or use `\$` at the start.

- **Code blocks**: always set the `class="language-*"` on the `<code>` element
  (not the `<pre>`). Prism's autoloader uses this class to fetch the grammar.
  Missing language class = no syntax highlighting, but no error.

- **Wide figures** (`.figure-wide`): these use CSS Grid column expansion.
  The figure spans beyond the 68ch text column up to `--w-wide-content` (90ch).
  On viewports narrower than the content column, they automatically fall back
  to column width — no extra CSS needed.

- **Prism and KaTeX** are loaded from CDN (jsDelivr). They are defer-loaded
  so they do not block page rendering. If you are offline, code highlighting
  and math rendering will not work, but the page is fully readable.

- **Self-hosted fonts**: all fonts are in `/fonts/` and loaded via `@font-face`
  in `writing.css`. No external font requests. If a font file is missing,
  the browser falls back to Georgia (body) or system sans-serif (headings).
  Re-download instructions:

  ```bash
  # From the repo root — re-downloads all writing section fonts
  bash writing/download-fonts.sh
  ```

  *(Create `download-fonts.sh` from the curl commands in the git history if
  the font files are ever lost from the repo.)*

- **Dark mode**: implemented via `@media (prefers-color-scheme: dark)` in
  `writing.css`. Tested on macOS (Safari, Chrome) and iOS. No JS toggle.

- **Reading time** is computed by a small JS snippet at the bottom of each
  post. It is a client-side estimate (words / 200 wpm); the reading index
  shows a manually entered estimate that you should update after writing.

---

## File structure

```
writing/
├── index.html              Writing index (post list)
├── writing.css             All styles for the writing section
├── feed.xml                RSS 2.0 feed (manually maintained)
├── README.md               This file
├── _template.html          Copy this to start a new post
└── example-post/
    └── index.html          Example post (demonstrates all features)

fonts/                      Self-hosted font files (woff2, Latin subset)
├── source-serif-4-latin-400.woff2
├── source-serif-4-latin-400italic.woff2
├── source-serif-4-latin-700.woff2
├── jetbrains-mono-latin-400.woff2
└── jetbrains-mono-latin-400italic.woff2
```
