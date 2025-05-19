<template>
	<div class="groups_content">
		<div v-for="productGroup in productGroups" :key="productGroup.id">
			<div class="card" style="width: 18rem">
				<div class="card-body">
					<h5 class="card-title">{{ productGroup.name }}</h5>
					<div v-for="product in productGroup.products" :key="product.id">
						{{ product.name }}
					</div>
					<button class="btn btn-primary">Ver grupo</button>
				</div>
			</div>
		</div>
	</div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { useRoute } from "vue-router";
import api from "@/utils/api";

import { ProductGroup } from "@/types/productgroup";

export default defineComponent({
	name: "GroupPage",
	data() {
		return {
			productGroups: null as ProductGroup[] | null,
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
			api
				.get(`/api/profile/${username}/groups/`)
				.then((response) => {
					this.productGroups = response.data;
				})
				.catch((error) => {
					console.log(error);
				});
		},
	},
});
</script>

<style scoped>
.groups_content {
	display: flex;
	flex-direction: row;
}

.card {
	display: flex;
	flex-wrap: wrap;
	margin-top: 40px;
	margin-left: 40px;
}
</style>
