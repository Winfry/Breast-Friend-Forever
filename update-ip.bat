@echo off
REM Script to automatically update mobile app with current IP address

echo Detecting current IP address...

REM Get IP address from ipconfig
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /C:"IPv4" ^| findstr /C:"192.168"') do (
    set IP=%%a
    goto :found
)

:found
REM Trim spaces
set IP=%IP: =%

if "%IP%"=="" (
    echo ❌ Could not detect IP address
    pause
    exit /b 1
)

echo 🔍 Detected IP: %IP%

REM Update apiConstants.js
powershell -Command "(Get-Content 'Mobile\src\services\apiConstants.js') -replace 'BASE_URL: ''http://[0-9.]+:8000''', 'BASE_URL: ''http://%IP%:8000''' | Set-Content 'Mobile\src\services\apiConstants.js'"

REM Update api.js
powershell -Command "(Get-Content 'Mobile\src\utils\api.js') -replace 'baseURL: ''http://[0-9.]+:8000''', 'baseURL: ''http://%IP%:8000''' | Set-Content 'Mobile\src\utils\api.js'"

echo ✅ Updated mobile config to: http://%IP%:8000
echo.
echo 📱 Now reload your app (press 'r' in Metro bundler)
echo.
pause
