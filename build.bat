@echo off
echo ====================================
echo  Building Unplug
echo ====================================
echo.

py -m pip install -r requirements.txt
py -m pip install pyinstaller

echo.
echo packaging...

set EXTRA_DATA=
if exist icon.png set EXTRA_DATA=%EXTRA_DATA% --add-data "icon.png;."
if exist alert.wav set EXTRA_DATA=%EXTRA_DATA% --add-data "alert.wav;."

pyinstaller --onefile --windowed --name Unplug ^
    --add-data "settings.json;." ^
    %EXTRA_DATA% ^
    main.py

echo.
echo done! check the dist\ folder for Unplug.exe
echo ====================================
pause