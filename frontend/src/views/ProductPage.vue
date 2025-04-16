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
                    <h5 class="card-title">
                        <router-link :to="{ name: 'ProductDetail', params: { slug: product.slug }}">{{ product.name }}</router-link>
                    </h5>
                    <span class="badge rounded-pill ">{{product.category.name}}</span>
                    <p>${{ product.price }}</p>
                    <button @click="addToCart(product)" class=" float-start btn btn-primary">
                        Add to Cart
                    </button>
                    <div class="input-group float-start mb-3">
                        <button
                            class="btn btn-outline-secondary"
                            type="button"
                            @click="decrementQuantity(product)"
                            :disabled="quantities[product.id] <= 1"
                        >
                            -
                        </button>
                        <input
                            type="number"
                            class="form-control text-center"
                            v-model.number="quantities[product.id]"
                            min="1"
                            @change="validateQuantity(product)"
                        >
                        <button
                            class="btn btn-outline-secondary"
                            type="button"
                            @click="incrementQuantity(product)"
                        >
                            +
                        </button>
                    </div>
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
    slug: string;
    price: number;
    description: string;
    category: Category;
}

interface Category {
    id: number;
    name: string;
    description: string;
}

export default defineComponent({
    name: "ProductPage",
    data() {
        return {
            products: [] as Product[],
            quantities: {} as Record<number, number>,
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
                    this.products.forEach(product => {
                        this.quantities[product.id] = 1;
                    });
                })
                .catch((error) => {
                    console.log(error);
                });
        },
        incrementQuantity(product: Product) {
            this.quantities[product.id]++;
        },
        decrementQuantity(product: Product) {
            if (this.quantities[product.id] > 1) {
                this.quantities[product.id]--;
            }
        },
        validateQuantity(product: Product) {
        const quantity = this.quantities[product.id];
        if (isNaN(quantity) || quantity < 1) {
        this.quantities[product.id] = 1;
        }
    },
        addToCart(product: Product) {
            this.cartStore.addToCart({
                product: {
                    id: product.id,
                    name: product.name,
                    price: product.price,
                    get_absolute_url: `/api/products/${product.slug}`,
                },
                quantity: this.quantities[product.id],
            });
        },
    },
});
</script>

<style scoped>
input[type="number"]::-webkit-inner-spin-button,
input[type="number"]::-webkit-outer-spin-button {
    -webkit-appearance: none;
    margin: 0;
}
.products-container {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    padding: 20px;
}
.product-card {
    margin-bottom: 20px;
}
.input-group {
    width: 120px;
    margin: 0 auto 15px;
}

.badge{
    background-color: rgb(166, 3, 184);
}
</style>