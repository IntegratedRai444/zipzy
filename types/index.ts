// User Types
export interface User {
  id: string;
  email: string;
  name: string;
  role: 'customer' | 'admin' | 'partner';
  phone?: string;
  avatar?: string;
  addresses: Address[];
  createdAt: string;
  updatedAt: string;
}

export interface Address {
  id: string;
  type: 'home' | 'work' | 'other';
  address: string;
  city: string;
  state: string;
  zipCode: string;
  isDefault: boolean;
  coordinates?: {
    lat: number;
    lng: number;
  };
}

// Product Types
export interface Product {
  id: string;
  name: string;
  description: string;
  price: number;
  originalPrice?: number;
  category: string;
  subcategory?: string;
  images: string[];
  stock: number;
  isAvailable: boolean;
  vendor: Vendor;
  rating: number;
  reviewCount: number;
  tags: string[];
  createdAt: string;
  updatedAt: string;
}

export interface Vendor {
  id: string;
  name: string;
  description: string;
  logo: string;
  rating: number;
  deliveryTime: string;
  minimumOrder: number;
  isOpen: boolean;
  categories: string[];
  address: Address;
}

// Order Types
export interface Order {
  id: string;
  userId: string;
  items: OrderItem[];
  total: number;
  subtotal: number;
  deliveryFee: number;
  tax: number;
  status: OrderStatus;
  paymentStatus: PaymentStatus;
  deliveryAddress: Address;
  deliveryInstructions?: string;
  estimatedDelivery: string;
  actualDelivery?: string;
  partner?: DeliveryPartner;
  tracking: TrackingInfo;
  createdAt: string;
  updatedAt: string;
}

export interface OrderItem {
  productId: string;
  product: Product;
  quantity: number;
  price: number;
  total: number;
  specialInstructions?: string;
}

export type OrderStatus = 
  | 'pending'
  | 'confirmed'
  | 'preparing'
  | 'ready'
  | 'picked_up'
  | 'in_transit'
  | 'delivered'
  | 'cancelled';

export type PaymentStatus = 
  | 'pending'
  | 'paid'
  | 'failed'
  | 'refunded';

// Payment Types
export interface Payment {
  id: string;
  orderId: string;
  amount: number;
  method: PaymentMethod;
  status: PaymentStatus;
  transactionId?: string;
  gateway: 'stripe' | 'razorpay' | 'upi';
  metadata?: Record<string, any>;
  createdAt: string;
}

export type PaymentMethod = 
  | 'card'
  | 'upi'
  | 'wallet'
  | 'cod'
  | 'net_banking';

// Delivery Types
export interface DeliveryPartner {
  id: string;
  name: string;
  phone: string;
  avatar?: string;
  rating: number;
  isOnline: boolean;
  currentLocation?: {
    lat: number;
    lng: number;
  };
  vehicle: {
    type: 'bike' | 'scooter' | 'car';
    number: string;
  };
}

export interface TrackingInfo {
  currentStatus: OrderStatus;
  estimatedDelivery: string;
  currentLocation?: {
    lat: number;
    lng: number;
  };
  route: {
    lat: number;
    lng: number;
  }[];
  updates: TrackingUpdate[];
}

export interface TrackingUpdate {
  status: OrderStatus;
  message: string;
  timestamp: string;
  location?: {
    lat: number;
    lng: number;
  };
}

// Cart Types
export interface CartItem {
  productId: string;
  product: Product;
  quantity: number;
  specialInstructions?: string;
}

export interface Cart {
  items: CartItem[];
  subtotal: number;
  deliveryFee: number;
  tax: number;
  total: number;
}

// Notification Types
export interface Notification {
  id: string;
  userId: string;
  type: 'order' | 'payment' | 'delivery' | 'promo' | 'system';
  title: string;
  message: string;
  isRead: boolean;
  data?: Record<string, any>;
  createdAt: string;
}

// Analytics Types
export interface Analytics {
  totalOrders: number;
  totalRevenue: number;
  averageOrderValue: number;
  topProducts: Product[];
  recentOrders: Order[];
  revenueByDay: {
    date: string;
    revenue: number;
  }[];
}

// API Response Types
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

export interface PaginatedResponse<T> {
  data: T[];
  pagination: {
    page: number;
    limit: number;
    total: number;
    totalPages: number;
  };
}
