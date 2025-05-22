<template>
	<router-link class="btn btn-primary add_button" :to="{name: 'AddRecipe', params: { username: route.params.username },}">
		Crear un Grupo
	</router-link>
        <div class="recipes_container">
            <div v-for="recipe in recipes" :key="recipe.id" class="product-card">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">
                            {{ recipe.name }}
                        </h5>
                        <router-link
						class="btn btn-primary"
						:to="{
							name: 'RecipeDetail',
							params: { id: recipe.id },
						}"
					>
						Ver Receta</router-link
					>
                    </div>
                </div>
            </div>
        </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { useRoute } from "vue-router";
import api from "@/utils/api";

import { Recipe } from "@/types/recipe";

export default defineComponent({
	name: "RecipeList",
	data() {
		return {
			recipes: null as Recipe | null,
		};
	},
	setup() {
		const route = useRoute();
		return { route };
	},
	mounted() {
		this.getProduct();
	},
	methods: {
		getProduct() {
			api
				.get(`/api/recipes/`)
				.then((response) => {
					this.recipes = response.data;
				})
				.catch((error) => {
					console.log(error);
				});
		},
	},
});
</script>

<style scoped>
.recipes_container {
	display: flex;
	flex-wrap: wrap;
	gap: 20px;
	padding: 20px;
}

.card {
	display: flex;
	flex-wrap: wrap;
	margin-top: 40px;
	margin-left: 40px;
}

.add_button {
	margin-left: 700px;
	margin-top: 25px;
}
</style>
