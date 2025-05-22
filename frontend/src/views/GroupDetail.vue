<template>
	<div v-if="groupDetail">
		<div class="group_content">
			<h1>{{ groupDetail.name }}</h1>
			<div class="products_container">
				<div v-for="product in groupDetail.products" :key="product.id" class="product-card">
					<div class="card">
						<figure class="image">
							<img :src="product.image" class="card-img-top" :alt="product.name" />
						</figure>
						<div class="card-body">
							<h5 class="card-title">
								<router-link :to="{ name: 'ProductDetail', params: { slug: product.slug } }">{{
									product.name
								}}</router-link>
							</h5>
							<span class="badge rounded-pill">{{ product.category.name }}</span>
							<p>${{ product.price }}</p>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { useRoute } from "vue-router";
import api from "@/utils/api";

interface ProductGroup {
	id: number;
	name: string;
	products: Product[];
}

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
	name: "GroupDetail",
	data() {
		return {
			groupDetail: null as ProductGroup | null,
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
			const username = this.route.params.username;
			const id = this.route.params.id;
			console.log(id);
			api
				.get(`/api/profile/${username}/groups/${id}`)
				.then((response) => {
					this.groupDetail = response.data;
				})
				.catch((error) => {
					console.log(error);
				});
		},
	},
});
</script>

<style>
.card {
	width: 300px;
}
.group_content {
	color: rgb(242, 242, 242);
	margin-top: 40px;
	margin-left: 100px;
	margin-right: 100px;
	padding: 8px;
	background-color: rgba(162, 162, 162, 0.534);
}

.badge {
	background-color: rgb(166, 3, 184);
}

.products_container {
	display: flex;
	flex-wrap: wrap;
	gap: 20px;
	padding: 20px;
}

.product-card {
	margin-bottom: 20px;
}
</style>
