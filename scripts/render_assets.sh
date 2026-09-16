#!/usr/bin/env bash
# Randează PNG-urile/WebP din SVG-urile sursă din assets/.
# Ordine de încercare pentru SVG -> PNG: rsvg-convert, qlmanage (macOS), magick.
# Ordine de încercare pentru PNG -> WebP: cwebp, Pillow (python3).
set -euo pipefail
cd "$(dirname "$0")/../assets"

have() { command -v "$1" >/dev/null 2>&1; }

render() { # $1=svg $2=png $3=dimensiune (px, latura maximă a cutiei de randare)
  local svg="$1" png="$2" size="$3"
  if have rsvg-convert; then
    rsvg-convert -w "$size" "$svg" -o "$png"
  elif have qlmanage; then
    # -x: fără cadru/umbră de tip Finder — altfel qlmanage completează cu alb
    # până la un canvas pătrat și strică raportul de aspect (1200x630 -> 1200x1200).
    rm -f "$svg.png"
    qlmanage -t -x -s "$size" -o . "$svg" >/dev/null 2>&1
    if [ ! -f "$svg.png" ]; then
      echo "BLOCAT: qlmanage nu a produs $svg.png" >&2
      return 1
    fi
    mv "$svg.png" "$png"
  elif have magick; then
    magick -background none "$svg" -resize "${size}x${size}" "$png"
  else
    echo "BLOCAT: nicio unealtă disponibilă pentru randare SVG->PNG (rsvg-convert, qlmanage, magick)." >&2
    return 1
  fi
  echo "ok: $png"
}

towebp() { # $1=png $2=webp
  local png="$1" webp="$2"
  if have cwebp; then
    cwebp -q 80 "$png" -o "$webp" >/dev/null
  elif python3 -c "import PIL" >/dev/null 2>&1; then
    python3 -c "from PIL import Image; Image.open('$png').convert('RGB').save('$webp', 'WEBP', quality=80)"
  else
    echo "BLOCAT: nici cwebp, nici Pillow (python3) nu sunt disponibile pentru conversia WebP." >&2
    return 1
  fi
  echo "ok: $webp"
}

render og-default.svg og-default.png 1200
render og-produs.svg og-produs.png 1200
render og-articol.svg og-articol.png 1200
render logo.svg logo.png 840
render apple-touch-icon.svg apple-touch-icon.png 180

# Poza reală (assets/marina.webp, assets/marina-portret.webp) se pune manual; vezi README.
