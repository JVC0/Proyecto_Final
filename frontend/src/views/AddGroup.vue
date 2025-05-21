<template>
        <form @submit.prevent="addGroupHandler">
                <h2>Add a Group</h2>
                <label for="name">Name</label>
                <input
                        id="name"
                        type="name"
                        placeholder="Name"
                        required
                        v-model="name"
                />
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
                                        <p class="product_price">${{ product.price }}</p>
                                </div>
                        </div>
                </div>
        </div>
                <button type="submit" id="submit" class="button-submit">
                        Create Group
                </button>
        </form>
        <p v-if="error" class="error">{{ error }}</p>
</template>

<script lang="ts">
import { ref } from "vue";
import api from "@/utils/api";
import { useRouter } from "vue-router";
import { useCartStore } from "@/stores/cart";
import axios from "axios";

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

export default {
        name: "AddGroup",

        data() {
                return {
                        products: [] as Product[],
                        quantities: {} as Record<number, number>,
                };
        },
        mounted() {
                this.getProducts();
        },

        setup() {
                const name = ref("");
                const productsToAdd = ref("");
                const error = ref("");
                const router = useRouter();
                const cartStore = useCartStore();

                const addGroupHandler = async () => {
                        try {
                                const csrfToken = document.cookie
                                        .split("; ")
                                        .find((row) => row.startsWith("csrftoken="))
                                        ?.split("=")[1];

                                if (!csrfToken) {
                                        throw new Error("CSRF token not found.");
                                }

                                const response = await api.post(
                                        "/api/profile/groups/add",
                                        {
                                                name: name.value,
                                                productsToAdd: productsToAdd.value,
                                        },
                                        {
                                                headers: {
                                                        "X-CSRFToken": csrfToken,
                                                },
                                        }
                                );

                                if (response.data.message) {
                                        router.push("/login");
                                }
                        } catch (err) {
                                if (axios.isAxiosError(err)) {
                                        error.value =
                                                err.response?.data?.error ||
                                                "Group creation failed. Please try again.";
                                } else if (err instanceof Error) {
                                        error.value = err.message;
                                } else {
                                        error.value = "An unexpected error occurred.";
                                }
                        }
                };

                return {
                        name,
                        productsToAdd,
                        error,
                        addGroupHandler,
                        cartStore ,
                };
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
        }},
};

</script>

<style>
*::after,
*::before {
        padding: 0;
        margin: 0;

}

body {
        background-image: url("https://wallpapercat.com/w/full/8/b/6/854961-1920x1080-desktop-full-hd-kfc-wallpaper-image.jpg");
        background-size: cover;
}

form {
        height: 80%;
        width: 95%;

        position: absolute;




}

form * {
        color: white;
        font-family: "Poppins", sans-serif;
        letter-spacing: 0.5px;
        outline: none;
        border: none;
}

form h3 {
        font-size: 32px;
        font-weight: 500;
        line-height: 42px;
        text-align: center;
}

form label {
        display: block;
        margin-top: 30px;
        font-size: 16px;
        font-weight: 500;
}

input {
        display: block;
        height: 50px;
        width: 100%;
        background-color: rgba(255, 255, 255, 0.0713);
        border-radius: 3px;
        padding: 0 10px;
        margin-top: 8px;
        font-size: 14px;
        font-weight: 300;
}

.button-submit {
        margin-top: 30px;
        width: 100%;
        background-color: white;
        padding: 15px 10px;
        font-size: 18px;
        font-weight: 500;
        cursor: pointer;
        color: black;
        border-radius: 5px;
}
.error {
        color: red;
}

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
.product_price {
        color: black
}
</style>
