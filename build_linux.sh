#!/usr/bin/env bash
set -e

# --- Lokasi folder proyek (otomatis deteksi) ---
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT_DIR="$SCRIPT_DIR"              # kalau skrip ini di root
REQ_FILE="$ROOT_DIR/requirements.txt"
APP_NAME="PerpustakaanApp"
ENTRY="app.py"
ICON="$ROOT_DIR/src/assets/app.png"

# pastikan requirements.txt ada
if [ ! -f "$REQ_FILE" ]; then
  echo "❌ Tidak menemukan requirements.txt di $ROOT_DIR"
  exit 1
fi

# 1️⃣ buat venv
python3 -m venv "$ROOT_DIR/.venv" || true
source "$ROOT_DIR/.venv/bin/activate"

# 2️⃣ install deps
python -m pip install --upgrade pip
pip install -r "$REQ_FILE"

# pastikan Tk ada
if ! dpkg -s python3-tk >/dev/null 2>&1; then
  echo "==> butuh sudo untuk python3-tk"
  sudo apt update && sudo apt install -y python3-tk
fi

# 3️⃣ build
pyinstaller \
  --name "$APP_NAME" \
  --noconfirm \
  --noconsole \
  --icon "$ICON" \
  --paths "$ROOT_DIR/src" \
  --add-data "$ROOT_DIR/src/assets:assets" \
  "$ROOT_DIR/$ENTRY"

echo
echo "✅ Build selesai!"
echo "Hasil ada di: $ROOT_DIR/dist/$APP_NAME/"
echo "Kemas rilis:  tar -C $ROOT_DIR/dist -czf ${APP_NAME}-linux.tar.gz $APP_NAME"
