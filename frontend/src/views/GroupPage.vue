<template>
    <div v-for="product in products" :key="product.id">
        <div class="card" style="width: 18rem">
            <figure class="image">
                <img
                    v-bind:src="product.image"
                    class="card-img-top"
                    alt="no funciona"
                />
            </figure>
            <div class="card-body">
                <h5 class="card-title">{{ product.name }}</h5>
                <p class="card-text">{{ product.description }}</p>
                <a href="#" class="btn btn-primary">${{ product.price }}</a>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
// import { defineComponent } from "vue";
// import axios from "axios";

// interface ProductGroup {
//     id: number;
//     image: string;
//     name: string;
//     price: number;
//     description: string;
// }

// export default defineComponent({
//     name: "ProductPage",
//     data() {
//         return {
//             products: [] as Product[],
//         };
//     },
//     mounted() {
//         this.getProducts();
//     },
//     methods: {
//         getProducts() {
//             axios
//                 .get("/api/products/")
//                 .then((response) => {
//                     this.products = response.data;
//                 })
//                 .catch((error) => {
//                     console.log(error);
//                 });
//         },
//     },
// });
</script>
