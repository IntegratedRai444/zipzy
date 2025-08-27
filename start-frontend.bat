@echo off
echo 🚀 Starting ZIPZY Frontend Application...
echo.

echo 📦 Installing dependencies...
cd apps/customer-web
npm install

echo.
echo 🌐 Starting development server...
echo.
echo ✅ Frontend will be available at: http://localhost:3000
echo 📡 API Gateway should be running at: http://localhost:4000
echo.
echo 🎯 Features available:
echo    - Modern landing page with animations
echo    - User authentication (login/register)
echo    - Dashboard with order tracking
echo    - Cart management
echo    - Category browsing
echo    - Responsive design
echo.

npm run dev
