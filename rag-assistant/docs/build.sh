#!/usr/bin/env bash
# Build the RAG Assistant documentation portal from markdown in _src/.
# The website repo is the single source of truth — content lives only here.
# Run:  ./build.sh    then commit the generated *.html and push (static.yml deploys it).
set -euo pipefail

OUT="$(cd "$(dirname "$0")" && pwd)"
SRC="$OUT/_src"
TEMPLATE="$OUT/template.html"
BASE="/rag-assistant/docs"

# SINGLE SOURCE OF TRUTH — drives pages, hub, and sidebar.
# Format:  section | slug | title | one-line description   (source: _src/<slug>.md)
DOCS=(
  "Getting Started|overview|Overview|What RAG Assistant is and how it works."
  "Getting Started|installation|Installation|Install on macOS, Windows, and Linux."
  "Getting Started|platform-support|Platform Support|Supported operating systems and Zotero requirements."
  "Core Features|indexing|Indexing Your Library|How indexing works, embedding models, and re-indexing."
  "Core Features|profiles|Profiles|Separate workspaces with their own settings, library, and chat history."
  "Core Features|prompting|Prompting & Generation|How answers are generated and how to tune them."
  "Configuration & Privacy|providers|LLM Providers & API Keys|Connect local or cloud models and manage API keys."
  "Configuration & Privacy|privacy|Privacy & Data Controls|What stays local and what is sent to cloud providers."
  "Troubleshooting|wont-index|The app won't index my library|Fixing indexing that won't start."
  "Troubleshooting|profile-wont-start|App won't start after deleting a profile|Recreate a default profile to recover."
)

esc() { printf '%s' "${1//&/&amp;}"; }

# --- sidebar (generated once, injected into every page) ---
{
  echo '<nav id="wiki-nav">'
  echo "  <a class=\"wiki-nav-home\" href=\"$BASE/\">Documentation</a>"
  section=""
  for entry in "${DOCS[@]}"; do
    IFS='|' read -r s slug title desc <<< "$entry"
    if [ "$s" != "$section" ]; then
      [ -n "$section" ] && echo '  </ul>'
      echo "  <div class=\"wiki-nav-section\">$(esc "$s")</div>"
      echo '  <ul>'
      section="$s"
    fi
    echo "    <li><a href=\"$BASE/$slug.html\">$(esc "$title")</a></li>"
  done
  echo '  </ul>'
  echo '</nav>'
} > "$OUT/_nav.html"

# --- pages ---
for entry in "${DOCS[@]}"; do
  IFS='|' read -r s slug title desc <<< "$entry"
  [ -f "$SRC/$slug.md" ] || { echo "missing $SRC/$slug.md" >&2; exit 1; }
  pandoc "$SRC/$slug.md" \
    --standalone --template="$TEMPLATE" \
    --metadata title="$title" \
    --metadata desc="$desc" \
    -o "$OUT/$slug.html"
  echo "built $slug.html"
done

# --- hub (rendered through the same template) ---
{
  echo "# RAG Assistant Documentation"
  echo
  echo "Setup and usage guides for RAG Assistant for Zotero."
  echo
  section=""
  for entry in "${DOCS[@]}"; do
    IFS='|' read -r s slug title desc <<< "$entry"
    if [ "$s" != "$section" ]; then echo; echo "## $s"; echo; section="$s"; fi
    echo "- [$title](./$slug.html) — $desc"
  done
} | pandoc --standalone --template="$TEMPLATE" \
    --metadata title="Documentation" \
    --metadata desc="Setup and usage guides for RAG Assistant for Zotero." \
    -o "$OUT/index.html"
echo "built index.html"

# --- inject sidebar into every generated page ---
python3 - "$OUT" <<'PY'
import sys, glob, pathlib
out = sys.argv[1]
nav = pathlib.Path(out, "_nav.html").read_text()
for f in glob.glob(f"{out}/*.html"):
    p = pathlib.Path(f)
    if p.name == "template.html":
        continue
    s = p.read_text()
    if "<!--WIKI_NAV-->" in s:
        p.write_text(s.replace("<!--WIKI_NAV-->", nav))
print("injected sidebar")
PY
