@echo off
echo.
echo ========================================
echo 🚀 ZIPZY PLATFORM - START ALL SERVICES
echo ========================================
echo.
echo Starting all ZIPZY services...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js 16+ and try again
    pause
    exit /b 1
)

echo ✅ Python and Node.js found
echo.

REM Start Chatbot Service (Port 8001)
echo 🔧 Starting Chatbot Service on port 8001...
start "ZIPZY Chatbot Service" cmd /k "cd backend\python-ml-service && python chatbot_service.py"
timeout /t 3 /nobreak >nul

REM Start Main Backend (Port 8000)
echo 🔧 Starting Main Backend on port 8000...
start "ZIPZY Main Backend" cmd /k "cd app && pip install -r requirements.txt && uvicorn main:app --reload --port 8000"
timeout /t 5 /nobreak >nul

REM Start Frontend Apps
echo 🔧 Starting Frontend Applications...

echo 📱 Starting ZIPZY Unified (Main App)...
start "ZIPZY Unified" cmd /k "cd frontend\zipzy-unified && npm run dev"

echo 📱 Starting Mobile App...
start "ZIPZY Mobile App" cmd /k "cd frontend\mobile-app && npm run dev"

echo 🏢 Starting Admin Dashboard...
start "ZIPZY Admin Dashboard" cmd /k "cd frontend\admin-dashboard && npm run dev"

echo 👥 Starting Customer Web...
start "ZIPZY Customer Web" cmd /k "cd frontend\customer-web && npm run dev"

echo 🤝 Starting Partner App...
start "ZIPZY Partner App" cmd /k "cd frontend\partner-app && npm run dev"

echo.
echo ========================================
echo 🎉 ALL SERVICES STARTED SUCCESSFULLY!
echo ========================================
echo.
echo 🌐 Service URLs:
echo    Main Backend:    http://localhost:8000
echo    Chatbot Service: http://localhost:8001
echo    ZIPZY Unified:   http://localhost:3000
echo    Mobile App:      http://localhost:3000
echo    Admin Dashboard: http://localhost:3030
echo    Customer Web:    http://localhost:3000
echo    Partner App:     http://localhost:3040
echo.
echo 📱 All services are now running in separate windows
echo 🔧 You can monitor each service in its respective window
echo 🚀 Your ZIPZY platform is ready for development!
echo.
echo Press any key to open the main application...
pause >nul

REM Open main app in browser
start http://localhost:3000

echo.
echo 🌐 Opening ZIPZY Unified in your browser...
echo.
echo Happy coding! 🎉
pause
