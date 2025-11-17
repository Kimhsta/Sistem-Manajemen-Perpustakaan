@echo off
setlocal
set APP_NAME=PerpustakaanApp
set ENTRY=app.py
set ICON=src\assets\app.ico

if not exist .venv (
  py -3 -m venv .venv
)
call .venv\Scripts\activate

python -m pip install --upgrade pip
pip install -r requirements.txt

pyinstaller ^
  --name "%APP_NAME%" ^
  --noconfirm ^
  --noconsole ^
  --icon "%ICON%" ^
  --paths src ^
  --add-data "src\assets;assets" ^
  "%ENTRY%"

echo.
echo ============================================
echo Build selesai!
echo File hasil: dist\%APP_NAME%\%APP_NAME%.exe
echo ============================================
pause
