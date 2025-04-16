<template>
    <p>Holaaaa :D</p>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import api from "@/utils/api";

interface Profile {
    id: number;
    avatar: string;
    bio: string;
    user: User;
}

interface User {
    id: number;
    first_name: string;
    last_name: string;
    email: string;
    username: string;
}

export default defineComponent({
    name: "ProductPage",
    data() {
        profile[] as Profile[]
    },
    setup() {},
    mounted() {},
    methods: {
        getProfile() {
            api.get("/api/profile/")
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
    }
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