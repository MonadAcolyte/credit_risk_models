#!/usr/bin/env bash
#
# clean.sh - remove the auxiliary files pdflatex and latexmk leave behind.
#
# PDFs are not deleted!
#
# Usage:
#   ./clean.sh            remove the files
#   ./clean.sh -n         dry run; list what would go, delete nothing
#   ./clean.sh -h         this help

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Auxiliary extensions, taken from .gitignore. Add to this list, not to the
# find call below.
EXTENSIONS=(
  aux bbl bcf blg brf fdb_latexmk fls fmt fot glg glo gls idx ilg ind lof
  log lot nav out run.xml snm synctex synctex.gz toc vrb xdv
)

DRY_RUN=0
while getopts ":nh" opt; do
  case "$opt" in
    n) DRY_RUN=1 ;;
    h) sed -n '2,12p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "clean.sh: unknown option -$OPTARG; try -h" >&2; exit 1 ;;
  esac
done

# Build the find expression: -name '*.aux' -o -name '*.bbl' -o ...
FIND_ARGS=()
for ext in "${EXTENSIONS[@]}"; do
  [ ${#FIND_ARGS[@]} -gt 0 ] && FIND_ARGS+=(-o)
  FIND_ARGS+=(-name "*.${ext}")
done

# Skip .git so a stray object name can never be matched.
mapfile -t FILES < <(
  find "$ROOT" -path "$ROOT/.git" -prune -o -type f \( "${FIND_ARGS[@]}" \) -print | sort
)

if [ ${#FILES[@]} -eq 0 ]; then
  echo "Nothing to clean."
  exit 0
fi

for file in "${FILES[@]}"; do
  echo "${file#"$ROOT"/}"
done

if [ "$DRY_RUN" -eq 1 ]; then
  echo
  echo "${#FILES[@]} file(s) would be removed. Dry run; nothing deleted."
  exit 0
fi

rm -f -- "${FILES[@]}"
echo
echo "${#FILES[@]} file(s) removed."

# Many of these are tracked in git, so deleting them shows up as deletions.
if command -v git >/dev/null 2>&1 && git -C "$ROOT" rev-parse --git-dir >/dev/null 2>&1; then
  tracked=$(git -C "$ROOT" ls-files --deleted | wc -l)
  if [ "$tracked" -gt 0 ]; then
    echo
    echo "Note: $tracked of these were tracked in git and now show as deletions."
    echo "To stop tracking them for good:"
    echo "  git rm --cached \$(git ls-files --deleted) && git commit -m 'Untrack LaTeX build artefacts'"
  fi
fi
