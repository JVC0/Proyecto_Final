<template>
    <div v-if="recipe">
        <div class="recipe_content">
			<div class="recipeTitle">
				<span>
                    <h1>{{ recipe.name }}</h1>
                </span>
			</div>
            <h4>
                Creado por:
            </h4>
            <div class="recipe_user"> {{ recipe.user.username }}</div>
            <br>
            <h4>Descripción: </h4>
            <div class="recipe_description">
                <span>{{ recipe.description }}</span>
            </div>
            <h4>Productos:</h4>
            <div class="product_content">
                <div v-for="product in recipe.product_group.products" :key="product.id">
                    <div class="card">
                        <figure class="product_image">
                        <img :src="product.image" class="card-img-top" :alt="product.name" />
                        </figure>
                        <div class="card-body">
                        <h5 class="card-title">
                            <router-link :to="{ name: 'ProductDetail', params: { slug: product.slug } }">{{ product.name }}</router-link>
                        </h5>
                        <span class="badge rounded-pill">{{ product.category.name }}</span>
                    </div>
                </div>
            </div>
            <br>
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
	name: "RecipeDetail",
	data() {
		return {
			recipe: null as Recipe | null,
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
            const id = this.route.params.id;
			api
				.get(`/api/recipes/${id}`)
				.then((response) => {
					this.recipe = response.data;
				})
				.catch((error) => {
					console.log(error);
				});
		},
	},
});
</script>

<style>
.recipe_content {
	color: rgb(242, 242, 242);
	margin-top: 40px;
	margin-left: 100px;
	margin-right: 100px;
	padding: 8px;
	background-color: rgba(162, 162, 162, 0.534);
}

.product_content {
    display: flex;
	flex-wrap: wrap;
	gap: 20px;
	padding: 20px;
}

.product_image {
    width: 150px;
    height: 150px;
}

.card {
    width: 150px;
}
</style>