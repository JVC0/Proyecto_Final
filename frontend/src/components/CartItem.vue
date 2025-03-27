<template>
    <tr v-if="item && item.product">
        <td>
            <router-link :to="item.product.get_absolute_url">
                {{ item.product.name }}
            </router-link>
        </td>
        <td>${{ item.product.price.toFixed(2) }}</td>
        <td>
            <button
                class="btn btn-sm btn-outline-secondary"
                @click="decrementQuantity"
                :disabled="item.quantity <= 1"
            >
                -
            </button>
            <span class="mx-2">{{ item.quantity }}</span>
            <button
                class="btn btn-sm btn-outline-secondary"
                @click="incrementQuantity"
            >
                +
            </button>
        </td>
        <td>${{ getItemTotal(item).toFixed(2) }}</td>
        <td>
            <button class="btn btn-danger btn-sm" @click="removeFromCart">
                <i class="bi bi-trash"></i>
            </button>
        </td>
    </tr>
</template>

<script lang="ts">
import { defineComponent, PropType } from "vue";
import { useCartStore } from "@/stores/cart";
import type { CartItem } from "@/stores/cart";

export default defineComponent({
    name: "CartItem",
    props: {
        item: {
            type: Object as PropType<CartItem>,
            required: true,
            validator: (value: CartItem) => {
                return !!value?.product && typeof value.quantity === "number";
            },
        },
    },
    emits: ["itemRemoved"],
    setup(props, { emit }) {
        const cartStore = useCartStore();

        const getItemTotal = (item: CartItem) => {
            if (!item?.product) return 0;
            return item.product.price * item.quantity;
        };

        const incrementQuantity = () => {
            if (props.item?.product?.id) {
                cartStore.incrementQuantity(props.item);
            }
        };

        const decrementQuantity = () => {
            if (props.item?.product?.id) {
                cartStore.decrementQuantity(props.item);
            }
        };

        const removeFromCart = () => {
            if (props.item?.product?.id) {
                cartStore.removeFromCart(props.item);
                emit("itemRemoved", props.item);
            }
        };

        return {
            getItemTotal,
            incrementQuantity,
            decrementQuantity,
            removeFromCart,
        };
    },
});
</script>

<style scoped>
.btn-sm {
    padding: 0.25rem 0.5rem;
    font-size: 0.875rem;
}
</style>
