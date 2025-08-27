import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { CartItem, Product } from '@/types';

interface CartState {
  items: CartItem[];
  subtotal: number;
  deliveryFee: number;
  tax: number;
  total: number;
  
  addItem: (product: Product, quantity?: number, specialInstructions?: string) => void;
  removeItem: (productId: string) => void;
  updateQuantity: (productId: string, quantity: number) => void;
  updateSpecialInstructions: (productId: string, instructions: string) => void;
  clearCart: () => void;
  calculateTotals: () => void;
}

export const useCartStore = create<CartState>()(
  persist(
    (set, get) => ({
      items: [],
      subtotal: 0,
      deliveryFee: 0,
      tax: 0,
      total: 0,
      
      addItem: (product: Product, quantity = 1, specialInstructions = '') => {
        const { items } = get();
        const existingItem = items.find(item => item.productId === product.id);
        
        if (existingItem) {
          // Update existing item
          const updatedItems = items.map(item =>
            item.productId === product.id
              ? { ...item, quantity: item.quantity + quantity }
              : item
          );
          set({ items: updatedItems });
        } else {
          // Add new item
          const newItem: CartItem = {
            productId: product.id,
            product,
            quantity,
            specialInstructions,
          };
          set({ items: [...items, newItem] });
        }
        
        get().calculateTotals();
      },
      
      removeItem: (productId: string) => {
        const { items } = get();
        const updatedItems = items.filter(item => item.productId !== productId);
        set({ items: updatedItems });
        get().calculateTotals();
      },
      
      updateQuantity: (productId: string, quantity: number) => {
        if (quantity <= 0) {
          get().removeItem(productId);
          return;
        }
        
        const { items } = get();
        const updatedItems = items.map(item =>
          item.productId === productId
            ? { ...item, quantity }
            : item
        );
        set({ items: updatedItems });
        get().calculateTotals();
      },
      
      updateSpecialInstructions: (productId: string, instructions: string) => {
        const { items } = get();
        const updatedItems = items.map(item =>
          item.productId === productId
            ? { ...item, specialInstructions: instructions }
            : item
        );
        set({ items: updatedItems });
      },
      
      clearCart: () => {
        set({ items: [], subtotal: 0, deliveryFee: 0, tax: 0, total: 0 });
      },
      
      calculateTotals: () => {
        const { items } = get();
        const subtotal = items.reduce((sum, item) => sum + (item.product.price * item.quantity), 0);
        const deliveryFee = subtotal > 0 ? 50 : 0; // Free delivery over certain amount
        const tax = subtotal * 0.18; // 18% GST
        const total = subtotal + deliveryFee + tax;
        
        set({ subtotal, deliveryFee, tax, total });
      },
    }),
    {
      name: 'cart-storage',
      partialize: (state) => ({ items: state.items }),
    }
  )
);
