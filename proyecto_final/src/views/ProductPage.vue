<template>
    <div class="products-container">
        <div v-for="product in products" :key="product.id" class="product-card">
            <div class="card" style="width: 18rem">
                <figure class="image">
                    <img
                        :src="product.image"
                        class="card-img-top"
                        :alt="product.name"
                    />
                </figure>
                <div class="card-body">
                    <h5 class="card-title">{{ product.name }}</h5>
                    <p class="card-text">{{ product.description }}</p>
                    <p>${{ product.price }}</p>
                    <button @click="addToCart(product)" class="btn btn-primary">
                        Add to Cart
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { useCartStore } from "@/stores/cart";
import api from "@/utils/api";

interface Product {
    id: number;
    image: string;
    name: string;
    price: number;
    description: string;
}

export default defineComponent({
    name: "ProductPage",
    data() {
        return {
            products: [] as Product[],
        };
    },
    setup() {
        const cartStore = useCartStore();
        return { cartStore };
    },
    mounted() {
        this.getProducts();
    },
    methods: {
        getProducts() {
            api.get("/api/products/")
                .then((response) => {
                    this.products = response.data;
                })
                .catch((error) => {
                    console.log(error);
                });
        },
        addToCart(product: Product) {
            this.cartStore.addToCart({
                product: {
                    id: product.id,
                    name: product.name,
                    price: product.price,
                    get_absolute_url: `/products/${product.id}`, // Add this URL
                    // Add any other required product properties
                },
                quantity: 1, // Default quantity when adding to cart
            });
        },
    },
});
</script>

<style scoped>
.products-container {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    padding: 20px;
}
.product-card {
    margin-bottom: 20px;
}
</style>
