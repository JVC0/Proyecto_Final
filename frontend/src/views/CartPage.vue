<template>
	<div class="container py-5">
		<h1 class="mb-5">Your Shopping Cart</h1>
		<div v-if="loading" class="text-center">
			<div class="spinner-border text-primary" role="status">
				<span class="visually-hidden">Loading...</span>
			</div>
		</div>
		<div v-else class="row">
			<div class="col-lg-8">
				<div class="card custom-card mb-4">
					<div class="card-body">
						<div v-for="(item, index) in cartItems" :key="item.id" class="row cart-item mb-3">
							<div class="col-md-3 mb-2">
								<img :src="item.product.image" :alt="item.product.name" class="img-fluid rounded" />
							</div>
							<div class="col-md-5">
								<h5 class="card-title">{{ item.product.name }}</h5>
								<p class="badge rounded-pill">{{ item.product.category.name }}</p>
							</div>
							<div class="col-md-2 text-end">
								<p class="fw-bold">${{ (item.product.price * item.quantity).toFixed(2) }}</p>
								<button class="btn btn-sm btn-outline-danger" @click="removeItem(item.id)">
									<i class="bi bi-trash"></i>
								</button>
							</div>
							<hr v-if="index < cartItems.length - 1" />
						</div>
						<div v-if="cartItems.length === 0" class="text-center py-4">
							<p>Your cart is empty</p>
						</div>
					</div>
				</div>
				<div class="text-start mb-4">
					<router-link class="btn btn-primary" to="/">
						<i class="bi bi-arrow-left me-2"></i>Continue Shopping
					</router-link>
				</div>
			</div>
			<div class="col-lg-4">
				<div class="card cart-summary">
					<div class="card-body">
						<h5 class="card-title mb-4">Order Summary</h5>
						<div class="d-flex justify-content-between mb-3">
							<span>Subtotal</span>
							<span>${{ subtotal.toFixed(2) }}</span>
						</div>
						<div class="d-flex justify-content-between mb-3">
							<span>Shipping</span>
							<span>${{ shipping.toFixed(2) }}</span>
						</div>
						<div class="d-flex justify-content-between mb-3">
							<span>Tax</span>
							<span>${{ tax.toFixed(2) }}</span>
						</div>
						<hr />
						<div class="d-flex justify-content-between mb-4">
							<strong>Total</strong>
							<strong>${{ total.toFixed(2) }}</strong>
						</div>
						<router-link class="btn btn-primary w-100" to="/Cart/payment">
							Proceed to Checkout
						</router-link>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, onMounted } from "vue";
import api from "@/utils/api";
import { CartItem } from "@/types/cartitem";

export default defineComponent({
	name: "CartPage",
	setup() {
		const loading = ref(true);
		const cartItems = ref<CartItem[]>([]);
		const shipping = ref(5.99);
		const taxRate = 0.008;
		const error = ref<string | null>(null);

		const subtotal = computed(() => {
			return cartItems.value.reduce((total: number, item: CartItem) => {
				return total + item.product.price * item.quantity;
			}, 0);
		});

		const tax = computed(() => {
			return subtotal.value * taxRate;
		});

		const total = computed(() => {
			return subtotal.value + tax.value + shipping.value;
		});

		const fetchCartItems = async () => {
			loading.value = true;
			error.value = null;
			try {
				const response = await api.get("/api/cart/");
				cartItems.value = response.data.items || [];
				console.log("Cart Items:", cartItems.value);
			} catch (err) {
				error.value = "Failed to load cart items. Please try again.";
				console.error("Error fetching cart items:", err);
			} finally {
				loading.value = false;
			}
		};

		const getCsrfToken = () => {
			const cookieValue = document.cookie
				.split("; ")
				.find((row) => row.startsWith("csrftoken="))
				?.split("=")[1];
			return cookieValue || "";
		};

		const removeItem = async (itemId: number) => {
			try {
				const csrfToken = getCsrfToken();
				await api.delete(`/api/cart/remove/${itemId}/`, {
					headers: {
						"X-CSRFToken": csrfToken,
					},
				});
				await fetchCartItems();
			} catch (err) {
				error.value = "Failed to remove item. Please try again.";
				console.error("Error removing item:", err);
			}
		};

		onMounted(() => {
			fetchCartItems();
		});

		return {
			loading,
			cartItems,
			subtotal,
			shipping,
			tax,
			total,
			error,
			removeItem,
		};
	},
});
</script>

<style scoped>
.cart-item img {
	max-width: 100px;
	height: auto;
}

.quantity-input {
	width: 50px;
}

.cart-summary {
	background-color: #f8f9fa;
	border-radius: 10px;
}
.custom-card {
	width: 100%;
}
</style>
