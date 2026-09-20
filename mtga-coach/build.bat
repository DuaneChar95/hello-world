@echo off
REM Build MTGA Coach into two executables in .\dist\
REM Double-click this file, or run it from PowerShell.
setlocal
cd /d "%~dp0"

echo.
echo   MTGA Coach - building Windows executables
echo   =========================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
  echo   Python was not found on PATH.
  echo   Install it from https://python.org and tick "Add python.exe to PATH".
  pause
  exit /b 1
)

echo   [1/3] regenerating the icon...
python assets\make_icon.py || goto :fail

echo   [2/3] checking PyInstaller...
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
  echo         not installed - installing now
  python -m pip install --quiet --upgrade pyinstaller || goto :fail
)

echo   [3/3] building ^(this takes a minute^)...
python -m PyInstaller mtga-coach.spec --noconfirm --clean || goto :fail

echo.
echo   Done. Your executables are in:
echo       %cd%\dist\
echo.
echo       MTGA Coach.exe             double-click this one
echo       MTGA Coach (console).exe   used by the terminal modes
echo.
echo   Keep both files together in the same folder.
echo.
pause
exit /b 0

:fail
echo.
echo   Build failed - see the messages above.
pause
exit /b 1
