@echo off
echo.
echo ========================================
echo    ZIPZY Unified Frontend Launcher
echo ========================================
echo.
echo Starting ZIPZY Unified Platform...
echo.

cd frontend\zipzy-unified

echo Installing dependencies...
call npm install

if %errorlevel% neq 0 (
    echo.
    echo Error: Failed to install dependencies
    echo Please check your Node.js installation
    pause
    exit /b 1
)

echo.
echo Dependencies installed successfully!
echo.
echo Starting development server...
echo.
echo Access your app at: http://localhost:3000
echo.
echo Press Ctrl+C to stop the server
echo.

call npm run dev

pause
