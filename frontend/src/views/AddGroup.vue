<template>
  <div class="groups_content" role="main" aria-labelledby="formHeading">
    <form @submit.prevent="addGroupHandler" role="form" aria-label="Group creation form">
      <h2 id="formHeading">Add a Group</h2>
      
      <div class="form-group">
        <label for="name">Name</label>
        <input 
          id="name" 
          type="text"
          placeholder="Name" 
          required 
          v-model="name"
          aria-required="true"
          aria-describedby="nameDescription"
        >
        <span id="nameDescription" class="visually-hidden">Enter group name</span>
      </div>

      <div 
        class="products-container" 
        role="list" 
        aria-label="List of available products"
      >
        <div 
          v-for="product in products" 
          :key="product.id" 
          class="product-card"
          role="listitem"
          :aria-labelledby="`product-${product.id}-title`"
        >
          <div class="card" style="width: 18rem">
            <figure class="image">
              <img 
                :src="product.image" 
                class="card-img-top custom_img" 
                :alt="product.name"
                role="img"
                aria-hidden="true"
              >
            </figure>
            <div class="card-body">
              <h5 
                class="card-title"
                :id="`product-${product.id}-title`"
              >
                <router-link 
                  :to="{ name: 'ProductDetail', params: { slug: product.slug } }"
                  :aria-label="`View details for ${product.name}`"
                >
                  {{ product.name }}
                </router-link>
              </h5>
              
              <span 
                class="badge rounded-pill" 
                :aria-label="`Category: ${product.category.name}`"
              >
                {{ product.category.name }}
              </span>
              
              <p 
                class="product_price" 
                aria-label="Price"
                :aria-valuetext="`$${product.price}`"
              >
                ${{ product.price }}
              </p>
              
              <div class="form-check">
                <input
                  class="checkbox"
                  type="checkbox"
                  :id="`product-${product.id}-checkbox`"
                  v-model="selectedProducts"
                  :value="product.id"
                  :aria-label="`Select ${product.name} for group`"
                >
                <label 
                  :for="`product-${product.id}-checkbox`"
                  class="visually-hidden"
                >
                  Select {{ product.name }}
                </label>
              </div>
            </div>
          </div>
        </div>
      </div>

      <button 
        type="submit" 
        class="button-submit"
        aria-label="Create new group"
      >
        Create Group
      </button>
    </form>

    <p 
      v-if="error" 
      class="error"
      role="alert"
      aria-live="assertive"
    >
      {{ error }}
    </p>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import api from "@/utils/api";
import { useRouter } from "vue-router";
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

export default defineComponent({
	name: "AddGroup",
	setup() {
		const name = ref("");
		const selectedProducts = ref<number[]>([]);
		const error = ref("");
		const router = useRouter();
		const products = ref<Product[]>([]);

		onMounted(async () => {
			try {
				const response = await api.get("/api/products/");
				products.value = response.data;
				const saved = localStorage.getItem("selectedProducts");
				if (saved) {
					selectedProducts.value = JSON.parse(saved);
				}
			} catch (err) {
				console.error("Error cargando productos:", err);
			}
		});

		const addGroupHandler = async () => {
			try {
				const csrfToken = document.cookie
					.split("; ")
					.find((row) => row.startsWith("csrftoken="))
					?.split("=")[1];

				if (!csrfToken) {
					throw new Error("CSRF token not found.");
				}

				localStorage.setItem("selectedProducts", JSON.stringify(selectedProducts.value));

				await api.post(
					"/api/profile/groups/add/",
					{
						name: name.value,
						products: selectedProducts.value,
					},
					{
						headers: {
							"X-CSRFToken": csrfToken,
						},
					}
				);

				localStorage.removeItem("selectedProducts");
				selectedProducts.value = [];
				name.value = "";
				router.push({
					name: "GroupPage",
					params: { username: router.currentRoute.value.params.username },
				});
			} catch (err) {
				if (axios.isAxiosError(err)) {
					error.value = err.response?.data?.error || "Error creando el grupo. Inténtalo de nuevo.";
				} else {
					error.value = "Error inesperado.";
				}
			}
		};
		return {
			name,
			selectedProducts,
			error,
			products,
			addGroupHandler,
		};
	},
});
</script>

<style>
.register *::after,
.register *::before {
	padding: 0;
	margin: 0;
	box-sizing: border-box;
}

.register {
	height: 560px;
	width: 400px;
	background-color: rgba(160, 160, 160, 0.3);
	position: absolute;
	transform: translate(-50%, -50%);
	border-radius: 10px;
	top: 50%;
	left: 50%;
	backdrop-filter: blur(10px);
	border: 2px solid rgba(255, 255, 255, 0.1);
	padding: 50px 35px;
	box-shadow: 0 0 40px rgba(8, 7, 16, 0.6);
}

.register * {
	color: white;
	font-family: "Poppins", sans-serif;
	letter-spacing: 0.5px;
	outline: none;
	border: none;
}

.register h2 {
	font-size: 32px;
	font-weight: 500;
	line-height: 42px;
	text-align: center;
}

.register label {
	display: block;
	margin-top: 30px;
	font-size: 16px;
	font-weight: 500;
}

.register input {
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

.register .button-submit {
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

.register .error {
	color: red;
}

.background {
	width: 430px;
	height: 520px;
	position: absolute;
	transform: translate(-50%, -50%);
	left: 50%;
	top: 50%;
}

.background .shape:first-child {
	background: linear-gradient(#1845ad, #23a2f6);
	left: -80px;
	top: -80px;
}

.background .shape:last-child {
	background: linear-gradient(#ad6018, #f69723);
	left: -30px;
	top: -80px;
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

.badge {
	background-color: rgb(166, 3, 184);
}
.product_price {
	color: black;
}

.custom_img {
	height: 200px;
}

.groups_content {
	display: flex;
	flex-wrap: wrap;
	gap: 20px;
	padding: 20px;
	color: rgb(242, 242, 242);
	margin-top: 40px;
	margin-left: 100px;
	margin-right: 100px;
	background-color: rgba(162, 162, 162, 0.534);
}

.checkbox {
	top: 0;
	right: 0;
	position: absolute;
	width: 25px;
	height: 25px;
}

</style>
