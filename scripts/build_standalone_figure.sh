#!/usr/bin/env bash
# Build a standalone TikZ figure from images/ into a cropped PDF (+ PNG preview).
#
# Why this exists: the local TeX Live 2025 "basic" install has tikz but NOT
# standalone.cls. The figure sources in images/ are written against standalone so
# they build unchanged on Overleaf; this script swaps in an equivalent article-based
# wrapper sized to the picture's own bounding box so they also build locally.
#
# Usage:  scripts/build_standalone_figure.sh mass_ordering
#         scripts/build_standalone_figure.sh feyn_cc_vertex
#
# Requires: pdflatex (/Library/TeX/texbin), pdftoppm (poppler) for the PNG preview.

set -euo pipefail

export PATH="/Library/TeX/texbin:$PATH"

NAME="${1:?usage: build_standalone_figure.sh <figure-basename-without-.tex>}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="$ROOT/images/$NAME.tex"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

[[ -f "$SRC" ]] || { echo "no such figure source: $SRC" >&2; exit 1; }

# Pass 1: article wrapper on a deliberately oversized page, purely to measure the
# picture's natural box dimensions.
python3 - "$SRC" "$WORK/measure.tex" <<'PY'
import sys, re
src = open(sys.argv[1]).read()
pre, rest = src.split(r'\begin{document}', 1)
body = rest.split(r'\end{document}')[0]
pre = re.sub(r'\\documentclass(\[[^\]]*\])?\{standalone\}', r'\\documentclass{article}', pre)
pre += ('\\usepackage[paperwidth=60cm,paperheight=60cm,margin=1cm]{geometry}\n'
        '\\pagestyle{empty}\\setlength{\\parindent}{0pt}\n'
        '\\newsavebox\\figbox\n')
open(sys.argv[2], 'w').write(
    pre + '\\begin{document}%\n\\savebox\\figbox{%' + body + '}%\n'
    '\\typeout{FIGDIM \\the\\wd\\figbox\\space \\the\\ht\\figbox\\space \\the\\dp\\figbox}%\n'
    '\\end{document}\n')
PY

cp "$SRC" "$WORK/" 2>/dev/null || true
# Note: write the log to a file rather than piping into grep -m1; an early-closing
# pipe makes pdflatex exit on SIGPIPE, which `set -o pipefail` then turns into a
# spurious failure.
(cd "$WORK" && pdflatex -interaction=nonstopmode measure.tex >measure.out 2>&1) || true
DIMS=$(grep '^FIGDIM ' "$WORK/measure.out" | tail -n 1)
[[ -n "$DIMS" ]] || { echo "could not measure $NAME -- see $WORK/measure.out" >&2; exit 1; }
read -r _ W H D <<<"$DIMS"
echo "measured: width=$W height=$H depth=$D"

# Pass 2: article wrapper on a page sized exactly to the measured box, plus an 8pt border.
python3 - "$SRC" "$WORK/$NAME.tex" "$W" "$H" "$D" <<'PY'
import sys, re
src = open(sys.argv[1]).read()
w, h, d = (float(v.replace('pt', '')) for v in sys.argv[3:6])
pre, rest = src.split(r'\begin{document}', 1)
body = rest.split(r'\end{document}')[0]
pre = re.sub(r'\\documentclass(\[[^\]]*\])?\{standalone\}', r'\\documentclass{article}', pre)
pre += (f'\\usepackage[paperwidth={w+16:.2f}pt,paperheight={h+d+16:.2f}pt,'
        f'textwidth={w:.2f}pt,textheight={h+d+2.5:.2f}pt,left=8pt,top=8pt]{{geometry}}\n'
        '\\pagestyle{empty}\n'
        '\\setlength{\\parindent}{0pt}\\setlength{\\topskip}{0pt}\n'
        '\\setlength{\\parskip}{0pt}\\setlength{\\lineskip}{0pt}\n')
open(sys.argv[2], 'w').write(pre + '\\begin{document}%\n' + body + '\\end{document}\n')
PY

(cd "$WORK" && pdflatex -interaction=nonstopmode "$NAME.tex" >/dev/null 2>&1)

PAGES=$(cd "$WORK" && pdfinfo "$NAME.pdf" | awk '/^Pages:/{print $2}')
[[ "$PAGES" == "1" ]] || { echo "expected 1 page, got $PAGES -- check $WORK/$NAME.log" >&2; exit 1; }

cp "$WORK/$NAME.pdf" "$ROOT/images/$NAME.pdf"
WROTE="images/$NAME.pdf"
if command -v pdftoppm >/dev/null 2>&1; then
    pdftoppm -png -r 150 "$ROOT/images/$NAME.pdf" "$WORK/prev"
    cp "$WORK/prev-1.png" "$ROOT/images/$NAME.png"
    WROTE="$WROTE and images/$NAME.png"
fi

echo "wrote $WROTE"
