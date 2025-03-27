import { defineStore } from "pinia";

export interface Product {
    id: number;
    name: string;
    price: number;
    get_absolute_url: string;
    image?: string;
    description?: string;
}

export interface CartItem {
    product: Product;
    quantity: number;
}

interface CartState {
    items: CartItem[];
    isAuthenticated: boolean;
    token: string;
    isLoading: boolean;
}

export const useCartStore = defineStore("cart", {
    state: (): CartState => ({
        items: [],
        isAuthenticated: false,
        token: "",
        isLoading: false,
    }),

    getters: {
        cartTotalLength(state): number {
            return state.items.reduce((acc, item) => acc + item.quantity, 0);
        },
        cartTotalPrice(state): number {
            return state.items.reduce(
                (acc, item) => acc + item.product.price * item.quantity,
                0
            );
        },
    },

    actions: {
        initializeCart() {
            const cartData = localStorage.getItem("cart");
            if (cartData) {
                this.items = JSON.parse(cartData).items;
            }
        },

        addToCart(item: CartItem) {
            const existingItem = this.items.find(
                (i) => i.product.id === item.product.id
            );

            if (existingItem) {
                existingItem.quantity += item.quantity;
            } else {
                this.items.push(item);
            }
            this.saveCart();
        },

        removeFromCart(item: CartItem) {
            this.items = this.items.filter(
                (i) => i.product.id !== item.product.id
            );
            this.saveCart();
        },

        incrementQuantity(item: CartItem) {
            const cartItem = this.items.find(
                (i) => i.product.id === item.product.id
            );
            if (cartItem) {
                cartItem.quantity += 1;
                this.saveCart();
            }
        },

        decrementQuantity(item: CartItem) {
            const cartItem = this.items.find(
                (i) => i.product.id === item.product.id
            );
            if (cartItem) {
                cartItem.quantity -= 1;
                if (cartItem.quantity <= 0) {
                    this.removeFromCart(item);
                } else {
                    this.saveCart();
                }
            }
        },

        saveCart() {
            localStorage.setItem("cart", JSON.stringify({ items: this.items }));
        },

        clearCart() {
            this.items = [];
            this.saveCart();
        },
    },
});
