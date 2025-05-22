<template>
	<div class="products-container">
		<div v-for="product in products" :key="product.id" class="product-card">
			<div class="card" style="width: 18rem">
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
					<p v-if="product.stock > 0" class="text-muted">In stock: {{ product.stock }}</p>
					<p v-else class="text-danger">Out of stock</p>
					<button
						@click="addToCart(product)"
						class="float-start btn btn-primary"
						:disabled="loading[product.id] || product.stock === 0"
					>
						<span
							v-if="loading[product.id]"
							class="spinner-border spinner-border-sm"
							role="status"
							aria-hidden="true"
						></span>
						{{ loading[product.id] ? "Adding..." : "Add to Cart" }}
					</button>
					<div class="input-group float-start mb-3" v-if="product.stock > 0">
						<button
							class="btn btn-outline-secondary"
							type="button"
							@click="decrementQuantity(product)"
							:disabled="quantities[product.id] <= 1"
						>
							-
						</button>
						<span class="form-control text-center quantity-display">
							{{ quantities[product.id] }}
						</span>
						<button
							class="btn btn-outline-secondary"
							type="button"
							@click="incrementQuantity(product)"
							:disabled="quantities[product.id] >= product.stock"
						>
							+
						</button>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import api from "@/utils/api";
import { Product } from "@/types/product";
import { useMessageStore } from "@/stores/message";

export default defineComponent({
	name: "ProductPage",
	data() {
		return {
			products: [] as Product[],
			quantities: {} as Record<number, number>,
			loading: {} as Record<number, boolean>,
		};
	},
	setup() {
		const messageStore = useMessageStore();
		return { messageStore };
	},
	mounted() {
		this.getProducts();
	},
	methods: {
		getProducts() {
			api.get("/api/products/").then((response) => {
				this.products = response.data;
				this.products.forEach((product) => {
					this.quantities[product.id] = Math.min(1, product.stock);
					this.loading[product.id] = false;
				});
			});
		},
		incrementQuantity(product: Product) {
			if (this.quantities[product.id] < product.stock) {
				this.quantities[product.id]++;
			}
		},
		decrementQuantity(product: Product) {
			if (this.quantities[product.id] > 1) {
				this.quantities[product.id]--;
			}
		},
		getCsrfToken() {
			const cookieValue = document.cookie
				.split("; ")
				.find((row) => row.startsWith("csrftoken="))
				?.split("=")[1];
			return cookieValue || "";
		},
		async addToCart(product: Product) {
			if (!product || product.stock === 0) return;

			this.loading[product.id] = true;

			try {
				const csrfToken = this.getCsrfToken();
				const response = await api.post(
					`/api/cart/add/${product.id}/`,
					{ quantity: this.quantities[product.id] },
					{
						headers: {
							"X-CSRFToken": csrfToken,
						},
					}
				);

				if (response.data.success) {
					this.messageStore.setMessage(
						response.data.message || "Product added to cart successfully!"
					);
				} else if (response.data.message) {
					this.messageStore.setMessage(response.data.message);
				}
			} catch (error: any) {
				if (error.response?.data?.message) {
					this.messageStore.setMessage(error.response.data.message, true);
				} else {
					this.messageStore.setMessage("Failed to add product to cart");
				}
			} finally {
				this.loading[product.id] = false;
			}
		},
	},
});
</script>

<style scoped>
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

.quantity-display {
	display: flex;
	align-items: center;
	justify-content: center;
	background-color: white;
	border: 1px solid #ced4da;
}
</style>
