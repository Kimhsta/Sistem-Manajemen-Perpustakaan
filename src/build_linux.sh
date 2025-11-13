#!/usr/bin/env bash
set -e
APP_NAME="PerpustakaanApp"
ENTRY="app.py"
ICON="src/assets/app.png"

python3 -m venv .venv || true
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt

# Tk untuk GUI (Linux perlu paket OS)
if ! dpkg -s python3-tk >/dev/null 2>&1; then
  echo "==> butuh sudo untuk python3-tk"
  sudo apt update && sudo apt install -y python3-tk
fi

pyinstaller \
  --name "$APP_NAME" \
  --noconfirm \
  --noconsole \
  --icon "$ICON" \
  --paths src \
  --add-data "src/assets:assets" \
  "$ENTRY"

echo
echo "Selesai. Hasil ada di: dist/$APP_NAME/"
echo "Kemas rilis:  tar -C dist -czf ${APP_NAME}-linux.tar.gz $APP_NAME"
