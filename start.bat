@echo off
echo.
echo ========================================
echo    🚀 ZIPZY - Starting Application
echo ========================================
echo.

echo 📋 Checking prerequisites...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    pause
    exit /b 1
)

node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed or not in PATH
    pause
    exit /b 1
)

echo ✅ Prerequisites check passed
echo.

echo 🔧 Installing dependencies...
echo Installing Python dependencies...
pip install -r requirements.txt --quiet

echo Installing Node.js dependencies...
pnpm install --silent

echo ✅ Dependencies installed
echo.

echo 🚀 Starting ZIPZY application...
echo.

echo 📡 Starting Backend API (Port 8000)...
start "ZIPZY Backend" cmd /k "python -m uvicorn app.main_simple:app --reload --host 0.0.0.0 --port 8000"

echo ⏳ Waiting for backend to start...
timeout /t 3 /nobreak >nul

echo 🌐 Starting Frontend (Port 3003)...
start "ZIPZY Frontend" cmd /k "pnpm dev"

echo.
echo ========================================
echo    🎉 ZIPZY is starting up!
echo ========================================
echo.
echo 📍 Access Points:
echo    Frontend: http://localhost:3003
echo    Backend:  http://localhost:8000
echo    API Docs: http://localhost:8000/docs
echo.
echo 🔑 Demo Accounts:
echo    Admin: admin@zipzy.com / Rishabhkapoor@0444
echo    Student: john@student.com / password123
echo.
echo ⏳ Please wait for both servers to fully start...
echo.
pause
