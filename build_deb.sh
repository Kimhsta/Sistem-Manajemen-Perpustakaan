#!/usr/bin/env bash
set -e

APP_NAME="PerpustakaanApp"
PKG_NAME="perpustakaanapp"
VERSION="1.0.0"

# root project
ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DIST_DIR="$ROOT_DIR/dist/$APP_NAME"

if [ ! -d "$DIST_DIR" ]; then
  echo "❌ Folder $DIST_DIR tidak ditemukan."
  echo "Jalankan dulu: bash build_linux.sh"
  exit 1
fi

# folder kerja paket
PKG_ROOT="$ROOT_DIR/build-deb/${PKG_NAME}_${VERSION}"
rm -rf "$PKG_ROOT"
mkdir -p "$PKG_ROOT"

# struktur standar deb
mkdir -p \
  "$PKG_ROOT/DEBIAN" \
  "$PKG_ROOT/opt/$PKG_NAME" \
  "$PKG_ROOT/usr/local/bin" \
  "$PKG_ROOT/usr/share/applications" \
  "$PKG_ROOT/usr/share/pixmaps"

# 1) copy app hasil PyInstaller ke /opt/perpustakaanapp
cp -r "$DIST_DIR/"* "$PKG_ROOT/opt/$PKG_NAME/"

# 2) script launcher di /usr/local/bin/perpustakaanapp
cat > "$PKG_ROOT/usr/local/bin/$PKG_NAME" <<EOF
#!/usr/bin/env bash
/opt/$PKG_NAME/$APP_NAME "\$@"
EOF
chmod +x "$PKG_ROOT/usr/local/bin/$PKG_NAME"

# 3) copy icon (pakai app.png di src/assets, kalau ada)
if [ -f "$ROOT_DIR/src/assets/app.png" ]; then
  cp "$ROOT_DIR/src/assets/app.png" "$PKG_ROOT/usr/share/pixmaps/$PKG_NAME.png"
fi

# 4) file .desktop buat muncul di menu aplikasi
cat > "$PKG_ROOT/usr/share/applications/$PKG_NAME.desktop" <<EOF
[Desktop Entry]
Type=Application
Name=Perpustakaan App
Comment=Sistem Manajemen Perpustakaan
Exec=$PKG_NAME
Icon=$PKG_NAME
Terminal=false
Categories=Education;Office;
EOF

# 5) file control (metadata debian)
cat > "$PKG_ROOT/DEBIAN/control" <<EOF
Package: $PKG_NAME
Version: $VERSION
Section: utils
Priority: optional
Architecture: amd64
Maintainer: Nama Kamu <email@example.com>
Description: Sistem Manajemen Perpustakaan (Python + Tkinter + SQLite)
 Aplikasi desktop untuk mengelola buku, mahasiswa, peminjaman,
 pengembalian, dan laporan denda.
EOF

# 6) build deb
OUT_DEB="$ROOT_DIR/${PKG_NAME}_${VERSION}_amd64.deb"
dpkg-deb --build "$PKG_ROOT" "$OUT_DEB"

echo
echo "✅ Berhasil membuat paket .deb:"
echo "    $OUT_DEB"
echo
echo "Install (test) dengan:"
echo "    sudo dpkg -i $(basename "$OUT_DEB")"
echo
echo "Lalu cari 'Perpustakaan App' di menu aplikasi."
