#!/bin/bash
# Every page footer says "This site does not use cookies or tracking technologies". (Solander's
# pages, which made the same claim for Paddle's domain review, now live in the solander-site
# repo and carry their own copy of this check.) A claim on a public page needs a
# check behind it: one added web font, embedded video or CDN script makes it false, silently.
#
# Links to other sites are fine — the privacy notice has to link Paddle's own. What is
# checked is anything the browser *loads*.
#
# Skipped: generated documentation output (contractex/, rag-assistant/docs/), which is built
# by mkdocs and not hand-authored, and `_`-prefixed partials, which are templates rather than
# pages anyone is served.
set -uo pipefail
cd "$(dirname "$0")/.."

status=0
while IFS= read -r file; do
  # src=, and href= only on <link>, which is the loading kind.
  loaded=$(grep -oiE '(src=|<link[^>]*href=)"(https?:)?//[^"]+"' "$file" \
           | sed 's/.*"\(.*\)"/\1/' | grep -v 'quietsignalslab\.com' | sort -u || true)
  if [ -n "$loaded" ]; then
    echo "FAIL $file loads from another origin:" >&2
    echo "$loaded" | sed 's/^/     /' >&2
    status=1
  fi
  for tracker in google-analytics googletagmanager 'gtag(' plausible fathom hotjar segment.com facebook.net; do
    if grep -qiF "$tracker" "$file"; then
      echo "FAIL $file references $tracker" >&2
      status=1
    fi
  done
done < <(find . -name '*.html' \
           -not -path './contractex/*' \
           -not -path './rag-assistant/docs/*' \
           -not -path './.git/*' \
           -not -name '_*')

[ $status -eq 0 ] && echo "ok   no page loads anything from another origin"
exit $status
