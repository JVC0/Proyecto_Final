<template>
    <div v-if="product">
        <section class="py-5">
            <div class="container bg-light rounded-4 mt-4 position-absolute top-50 start-50 translate-middle">
                <div class="row gx-5">
                    <aside class="col-lg-6 p-0">
                            <img
                                :src="product.image"
                                :alt="product.name"
                            />
                    </aside>
                    <main class="col-lg-6 ">
                        <div class="ps-lg-3">
                            <h4 class="title text-dark mt-4">
                                {{ product.name }}
                            </h4>
                            <div class="d-flex flex-row my-3">
                            <span class="text-success">In stock</span>
                            </div>
                            <div class="mb-3">
                                <span class="h5">${{ product.price }}</span>
                                <span class="text-muted">/per item</span>
                            </div>
                            <p>
                                {{ product.description }}
                            </p>
                            <hr/>
                            <div class="row mb-4">
                                <div class="col-md-4 col-6 mb-3">
                                    <label for="quantity-input" class="mb-2 d-block">Quantity</label>
                                    <div class="input-group mb-3" style="width: 170px">
                                        <button
                                            class="btn btn-light border border-secondary px-3"
                                            type="button"
                                            @click="decrementQuantity"
                                            data-mdb-ripple-color="dark"
                                        >
                                            <i class="bi bi-dash"></i>
                                        </button>
                                        <input
                                            id="quantity-input"
                                            type="text"
                                            class="form-control text-center border border-secondary"
                                            v-model.number="quantity"
                                            @change="validateQuantity"
                                            aria-label="Quantity"
                                        />
                                        <button
                                            class="btn btn-light border border-secondary px-3"
                                            type="button"
                                            @click="incrementQuantity"
                                            data-mdb-ripple-color="dark"
                                        >
                                            <i class="bi bi-plus"></i>
                                        </button>
                                    </div>
                                </div>
                            </div>
                            <button @click="addToCart" class="btn btn-primary shadow-0">
                                <i class="me-1 fa fa-shopping-basket"></i> Add to cart
                            </button>
                        </div>
                    </main>
                </div>
            </div>
        </section>
    </div>

    <div v-else class="text-center py-5">
        <output class="spinner-border" aria-live="polite" aria-busy="true">
            Loading product information...
        </output>
    </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { useCartStore } from "@/stores/cart";
import { useRoute } from "vue-router";
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
    name: "ProductDetail",
    data() {
        return {
            product: null as Product | null,
            quantity: 1,
        };
    },
    setup() {
        const cartStore = useCartStore();
        const route = useRoute();
        return { cartStore, route };
    },
    mounted() {
        this.getProduct();
    },
    methods: {
        getProduct() {
            const slug = this.route.params.slug;
            api.get(`/api/products/${slug}/`)
                .then((response) => {
                    this.product = response.data;
                })
                .catch((error) => {
                    console.log(error);
                });
        },
        incrementQuantity() {
            this.quantity++;
        },
        decrementQuantity() {
            if (this.quantity > 1) {
                this.quantity--;
            }
        },
        validateQuantity() {
            if (isNaN(this.quantity) || this.quantity < 1) {
                this.quantity = 1;
            }
        },
        addToCart() {
            if (this.product) {
                this.cartStore.addToCart({
                    product: {
                        id: this.product.id,
                        name: this.product.name,
                        price: this.product.price,
                        get_absolute_url: `/api/products/${this.product.slug}/`,
                    },
                    quantity: this.quantity,
                });
            }
        },
    },
});
</script>

<style>
img{
    width:600px
}
.custom-box{
    margin-top: 100px;
}

</style>
