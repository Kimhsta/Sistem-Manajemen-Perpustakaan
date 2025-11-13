@echo off
setlocal
set APP_NAME=PerpustakaanApp
set ENTRY=app.py
set ICON=src\assets\app.ico

REM 1) venv
if not exist .venv (
  py -3 -m venv .venv
)
call .venv\Scripts\activate

REM 2) deps
python -m pip install --upgrade pip
pip install -r requirements.txt
REM Tk dibawa PyInstaller untuk Windows, tidak perlu paket OS

REM 3) build
pyinstaller ^
  --name "%APP_NAME%" ^
  --noconfirm ^
  --noconsole ^
  --icon "%ICON%" ^
  --paths src ^
  --add-data "src\assets;assets" ^
  "%ENTRY%"

echo.
echo Selesai. Hasil ada di: dist\%APP_NAME%\
echo Zip-kan folder itu untuk rilis (klik kanan -> Send to -> Compressed (zipped) folder).
pause
