@echo off
echo 🚀 Starting ZIPZY Platform - Phase 2
echo.
echo 📁 Project Structure:
echo    🗄️ database/ - Database schema and Supabase setup
echo    🔧 backend/zipzy-server - Real backend server
echo    📱 frontend/zipzy-unified - Unified frontend app
echo.
echo 🎯 Phase 2 Features:
echo    ✅ Real Database Integration (Supabase)
echo    ✅ Complete Backend API Server
echo    ✅ Authentication & Authorization
echo    ✅ User Management
echo    ✅ Product & Order Management
echo    ✅ Payment Integration Ready
echo    ✅ Real-time Features Ready
echo.
echo 📊 Setting up database...
echo.
echo 🔧 Installing Supabase CLI...
npm install -g supabase

echo.
echo 🗄️ Starting Supabase services...
cd database\supabase
supabase start

echo.
echo 📊 Creating database schema...
supabase db reset

echo.
echo 🌱 Seeding database with sample data...
supabase db reset --db-url postgresql://postgres:postgres@127.0.0.1:54322/postgres

echo.
echo 🔧 Setting up backend server...
cd ..\..\backend\zipzy-server

echo.
echo 📦 Installing backend dependencies...
npm install

echo.
echo 🌐 Starting backend server...
npm run dev

echo.
echo ✅ Phase 2 Setup Complete!
echo.
echo 🌐 Supabase Studio: http://localhost:54323
echo 🔌 Backend API: http://localhost:5000
echo 📱 Frontend App: http://localhost:3000
echo.
echo 🎯 Available Features:
echo    - Real database with sample data
echo    - Complete backend API
echo    - User authentication system
echo    - Role-based access control
echo    - Product catalog management
echo    - Order processing system
echo    - Payment gateway integration
echo    - Real-time notifications
echo.
echo 🔐 Demo Credentials:
echo    Customer: customer@zipzy.com / password123
echo    Admin: admin@zipzy.com / password123
echo    Partner: partner@zipzy.com / password123
echo.
pause
