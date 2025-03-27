<template>
    <div class="cart-page">
        <h1 class="title">Your Cart</h1>

        <div v-if="cartStore.items.length > 0">
            <table class="table">
                <thead>
                    <tr>
                        <th>Product</th>
                        <th>Price</th>
                        <th>Quantity</th>
                        <th>Total</th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                    <CartItem
                        v-for="item in cartStore.items"
                        :key="item.product.id"
                        :item="item"
                        @item-removed="handleItemRemoved"
                    />
                </tbody>
            </table>

            <div class="cart-summary">
                <p>Total: ${{ cartStore.cartTotalPrice.toFixed(2) }}</p>
            </div>
        </div>

        <div v-else>
            <p>Your cart is empty</p>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { useCartStore } from "@/stores/cart";
import CartItem from "@/components/CartItem.vue";
import type { CartItem as CartItemType } from "@/stores/cart";

export default defineComponent({
    name: "CartPage",
    components: {
        CartItem,
    },
    setup() {
        const cartStore = useCartStore();

        const handleItemRemoved = (item: CartItemType) => {
            console.log("Item removed:", item);
        };

        return {
            cartStore,
            handleItemRemoved,
        };
    },
});
</script>
