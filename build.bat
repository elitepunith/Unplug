@echo off
echo ====================================
echo  Building Shutdown Reminder
echo ====================================
echo.

pip install -r requirements.txt
pip install pyinstaller

echo.
echo packaging...
pyinstaller --onefile --windowed --name ShutdownReminder ^
    --add-data "settings.json;." ^
    --add-data "alert.wav;." ^
    --add-data "icon.png;." ^
    --icon=icon.png ^
    main.py

echo.
echo done! check the dist/ folder for ShutdownReminder.exe
echo ====================================
pause