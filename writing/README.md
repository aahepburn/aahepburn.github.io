# Writing — Quiet Signals Lab

The engineering blog at `quietsignalslab.com/writing/`. Plain HTML, styled by `/lab.css`
like the rest of the site. No build step.

## Publish a post

1. **Pick a slug**: short, lowercase, hyphenated (`why-a-black-box-isnt-a-redaction`).
   The post lives at `writing/<slug>/index.html` and is served at `/writing/<slug>/`.

2. **Copy the template**

   ```bash
   mkdir writing/<slug>
   cp writing/_template.html writing/<slug>/index.html
   ```

3. **Fill every `<!-- PLACEHOLDER -->`**: title, one-sentence description, slug, date
   (ISO `YYYY-MM-DD` in attributes, "1 June 2026" in the text), reading time
   (words ÷ 200, rounded), topic words, standfirst. Write the body between the `══` banners.
   Put images next to `index.html`, give each `alt`, `width` and `height`.

4. **List it in three places**, newest first:
   - `writing/index.html`: a new `<li class="q-post">` at the top of the list.
   - `index.html` (homepage), the Engineering blog box: keep the three newest.
   - `writing/feed.xml`: copy the `[ITEM TEMPLATE]` block to the top of the items, and set
     `<lastBuildDate>`. RFC 2822 dates: `date -R`.

5. **Check and push**

   ```bash
   ./ci/no-external-loads.sh && ./ci/markup-sanity.sh
   git add writing/ index.html && git commit -m "writing: publish '<title>'" && git push
   ```

## Rules

- Nothing loads from another origin: no CDN scripts, fonts or embeds. The footer promises
  no tracking, and `ci/no-external-loads.sh` fails the deploy if a page breaks that. Code
  blocks are plain `<pre><code>`; if a post ever needs maths or syntax highlighting,
  self-host the library.
- One `<h1>` per page, the post title. Sections start at `<h2>`.

## Hide a post without deleting it

Comment out its `<li>` in `writing/index.html` and its `<item>` in `feed.xml`.
The page itself stays reachable at its URL.
