<template>
	<div v-if="product">
		<section class="py-5">
			<div
				class="container bg-light rounded-4 mt-4 position-absolute top-50 start-50 translate-middle"
			>
				<div class="row gx-5">
					<aside class="col-lg-6 p-0">
						<img :src="product.image" :alt="product.name" class="img-fluid" />
					</aside>
					<main class="col-lg-6">
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
							<hr />
							<div class="row mb-4">
								<div class="col-md-4 col-6 mb-3">
									<label for="quantity-input" class="mb-2 d-block">Quantity</label>
									<div class="input-group mb-3" style="width: 170px">
										<button
											class="btn btn-light border border-secondary px-3"
											type="button"
											@click="decrementQuantity"
											data-mdb-ripple-color="dark"
											:disabled="quantity <= 1"
										>
											<i class="bi bi-dash"></i>
										</button>
										<input
											id="quantity-input"
											type="number"
											min="1"
											class="form-control text-center border border-secondary"
											v-model.number="quantity"
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
							<button @click="addToCart" class="btn btn-primary shadow-0" :disabled="loading">
								<template v-if="!loading">
									<i class="me-1 fa fa-shopping-basket"></i> Add to cart
								</template>
								<template v-else>
									<span
										class="spinner-border spinner-border-sm"
										role="status"
										aria-hidden="true"
									></span>
									Adding...
								</template>
							</button>
							<div v-if="message" class="alert alert-success mt-3">
								{{ message }}
							</div>
						</div>
					</main>
				</div>
			</div>
		</section>
	</div>

	<div v-else class="text-center py-5">
		<div class="spinner-border" role="status">
			<span class="visually-hidden">Loading...</span>
		</div>
	</div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { useRoute } from "vue-router";
import api from "@/utils/api";
import type { Product } from "@/types/product";

export default defineComponent({
	name: "ProductDetail",
	data() {
		return {
			product: null as Product | null,
			quantity: 1,
			message: "",
			loading: false,
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
		getCsrfToken(): string {
			const csrfToken = document.cookie
				.split("; ")
				.find((row) => row.startsWith("csrftoken="))
				?.split("=")[1];
			return csrfToken || "";
		},
		async getProduct() {
			const slug = this.route.params.slug;
			const response = await api.get(`/api/products/${slug}/`);
			this.product = response.data;
		},
		incrementQuantity() {
			this.quantity++;
		},
		decrementQuantity() {
			if (this.quantity > 1) {
				this.quantity--;
			}
		},
		async addToCart() {
			if (!this.product) return;

			this.loading = true;
			this.message = "";

			const csrfToken = this.getCsrfToken();
			const response = await api.post(
				`/api/cart/add/${this.product.id}/`,
				{ quantity: this.quantity },
				{
					headers: {
						"X-CSRFToken": csrfToken,
					},
				}
			);

			this.message = response.data.message || `${this.quantity} item(s) added to cart`;
			this.loading = false;
		},
	},
});
</script>

<style>
img {
	width: 600px;
}
.custom-box {
	margin-top: 100px;
}
</style>
