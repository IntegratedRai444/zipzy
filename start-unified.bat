@echo off
echo 🚀 Starting ZIPZY Unified Platform...
echo.

echo 📁 Project Structure:
echo    📱 frontend/zipzy-unified - Unified Next.js application
echo    🔧 backend/ - Backend services
echo    🗄️ database/ - Database files
echo    🔗 integration/ - Third-party integrations
echo.

echo 🎯 Unified Application Features:
echo    ✅ Single app for all user types (Customer, Admin, Partner)
echo    ✅ Role-based authentication and routing
echo    ✅ Shared components and navigation
echo    ✅ Real-time features (WebSocket ready)
echo    ✅ Payment integration ready
echo    ✅ Database integration ready
echo    ✅ Maps integration ready
echo.

echo 📦 Installing dependencies...
cd frontend\zipzy-unified
npm install
echo.

echo 🌐 Starting development server...
echo.
echo ✅ Unified app will be available at: http://localhost:3000
echo.
echo 🎯 Available Features:
echo    - Landing page with animations
echo    - Role-based authentication (Customer/Admin/Partner)
echo    - Unified dashboard with role-specific views
echo    - Shopping cart management
echo    - Order tracking
echo    - Real-time notifications
echo    - Responsive design
echo.
echo 🔐 Login Credentials (Demo):
echo    Customer: customer@zipzy.com / password123
echo    Admin: admin@zipzy.com / password123
echo    Partner: partner@zipzy.com / password123
echo.

npm run dev
