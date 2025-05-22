<template>
	<form class="register" @submit.prevent="recipeCreatorHandler">
		<h2>Add a Recipe</h2>
        <label for="name">Name</label>
        <input id="name" type="name" placeholder="Name" required v-model="name"/>
        <label for="description">Description</label>
        <input id="description" type="description" placeholder="Description" required v-model="description"/>
        <label for="productGroup">Product Group</label>
        <select id="productGroup" v-model="productGroupId" required v-if="productGroups">
            <option class="group_names" v-for="group in productGroups" :key="group.id" :value="group.id">
                {{ group.name }}
            </option>
        </select>
		<button type="submit" id="submit" class="button-submit">Create Recipe</button>
	</form>
</template>

<script lang="ts">
import { ref, defineComponent, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import api from "@/utils/api";
import { useMessageStore } from "@/stores/message";
import { ProductGroup } from "@/types/productgroup";

export default defineComponent({
	name: "AddRecipe",
	setup() {
		const route = useRoute();
		const router = useRouter();
		const messageStore = useMessageStore();
		const authStore = useAuthStore()
        
		const name = ref("");
		const description = ref("");
		const productGroupId = ref<number | null>(null);
		const productGroups = ref<ProductGroup[] | null>(null);

		// Obtener grupos de productos
		onMounted(async () => {
			try {
				const username = authStore.user?.username;
				const response = await api.get(`/api/profile/${username}/groups/`);
				productGroups.value = response.data;
			} catch (error) {
				console.error("Error fetching groups:", error);
			}
		});

		const recipeCreatorHandler = async () => {
			try {
				const csrfToken = document.cookie
					.split("; ")
					.find((row) => row.startsWith("csrftoken="))
					?.split("=")[1];

				const response = await api.post(
					"/api/recipes/add/",
					{
						name: name.value,
						description: description.value,
						product_group: productGroupId.value, // Asegurar que el nombre del campo coincide con tu API
					},
					{
						headers: {
							"X-CSRFToken": csrfToken,
						},
					}
				);

				if (response.data.success) {
					messageStore.setMessage(response.data.message || "¡Receta creada con éxito!");
				}
			} catch (error: any) {
				messageStore.setMessage(error.response?.data?.message || "Error al crear la receta");
			}
		};

		return {
			name,
			description,
			productGroupId,
			productGroups,
			recipeCreatorHandler,
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

.group_names {
	color: black;
}
</style>
