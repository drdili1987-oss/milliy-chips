#!/usr/bin/env bash
# Katalog (PDF + sahifa rasmlari) va saytni src/foto/ dagi rasmlardan qayta yig'adi.
# Talab: Python 3 + Pillow, Node.js 18+, poppler-utils (pdftoppm).
# Ishga tushirish (repo ildizidan):  bash src/yangilash.sh
set -euo pipefail
cd "$(dirname "$0")"
[ -d node_modules ] || npm install --no-audit --no-fund
[ -n "${PLAYWRIGHT_BROWSERS_PATH:-}" ] || npx playwright install chromium

python3 build.py foto catalog.html
python3 site.py  foto site.html
node render.js                                   # catalog.html -> Milliy-Chips-katalog.pdf

wrap() {  # artifact-fragmentni to'liq HTML hujjatga o'raydi
python3 - "$1" "$2" <<'PY'
import sys
s = open(sys.argv[1], encoding="utf-8").read()
i = s.index("</style>") + len("</style>")
open(sys.argv[2], "w", encoding="utf-8").write(
    '<!doctype html>\n<html lang="uz">\n<head>\n<meta charset="utf-8">\n'
    '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
    + s[:i] + "\n</head>\n<body>" + s[i:] + "</body>\n</html>\n")
PY
}
wrap site.html ../index.html
wrap catalog.html ../katalog/index.html
mv Milliy-Chips-katalog.pdf ../katalog/
rm -f ../katalog/sahifalar/*.jpg
pdftoppm -r 130 -jpeg -jpegopt quality=88 ../katalog/Milliy-Chips-katalog.pdf ../katalog/sahifalar/sahifa
rm -f catalog.html site.html
echo "Tayyor: index.html, katalog/index.html, katalog/Milliy-Chips-katalog.pdf, katalog/sahifalar/"
