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
								<span :class="product.stock > 0 ? 'text-success' : 'text-danger'">
									{{ product.stock > 0 ? `In stock (${product.stock} available)` : "Out of stock" }}
								</span>
							</div>
							<div class="mb-3">
								<span class="h5">${{ product.price }}</span>
								<span class="text-muted">/per item</span>
							</div>
							<p>
								{{ product.description }}
							</p>
							<hr />
							<div class="row mb-4" v-if="product.stock > 0">
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
										<span class="form-control text-center border border-secondary quantity-display">
											{{ quantity }}
										</span>
										<button
											class="btn btn-light border border-secondary px-3"
											type="button"
											@click="incrementQuantity"
											data-mdb-ripple-color="dark"
											:disabled="quantity >= product.stock"
										>
											<i class="bi bi-plus"></i>
										</button>
									</div>
								</div>
							</div>
							<button
								@click="addToCart"
								class="btn btn-primary shadow-0"
								:disabled="loading || product.stock === 0 || quantity > product.stock"
							>
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
							<div v-if="message" class="alert mt-3" :class="messageType">
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

interface ProductDetailData {
	product: Product | null;
	quantity: number;
	loading: boolean;
	message: string;
	messageType: string;
}

export default defineComponent({
	name: "ProductDetail",
	data(): ProductDetailData {
		return {
			product: null,
			quantity: 1,
			loading: false,
			message: "",
			messageType: "alert-success",
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
			try {
				const slug = this.route.params.slug;
				const response = await api.get(`/api/products/${slug}/`);
				this.product = response.data;
				if (this.product) {
					this.quantity = Math.min(1, this.product.stock);
				}
			} catch (error) {
				console.error("Error fetching product:", error);
			}
		},
		incrementQuantity() {
			if (this.product && this.quantity < this.product.stock) {
				this.quantity++;
			}
		},
		decrementQuantity() {
			if (this.quantity > 1) {
				this.quantity--;
			}
		},
		async addToCart() {
			if (!this.product || this.product.stock === 0 || this.quantity > this.product.stock) return;

			this.loading = true;
			this.message = "";
			this.messageType = "alert-success";

			try {
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
				setTimeout(() => {
					this.message = "";
				}, 3000);
			} catch (error) {
				console.error("Error adding to cart:", error);
				this.message = "Failed to add product to cart";
				this.messageType = "alert-danger";
			} finally {
				this.loading = false;
			}
		},
	},
	watch: {
		"product.stock"(newStock) {
			if (this.quantity > newStock) {
				this.quantity = Math.max(1, Math.min(this.quantity, newStock));
			}
		},
	},
});
</script>

<style scoped>
img {
	width: 600px;
	max-height: 600px;
	object-fit: contain;
}
.custom-box {
	margin-top: 100px;
}
.quantity-display {
	display: flex;
	align-items: center;
	justify-content: center;
	background-color: white;
}
.alert-success {
	background-color: #d1e7dd;
	color: #0f5132;
}
.alert-danger {
	background-color: #f8d7da;
	color: #842029;
}
</style>
