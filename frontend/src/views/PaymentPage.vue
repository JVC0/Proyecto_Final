<template>
	<div class="container py-3">
		<div class="row">
			<div class="col-12 col-sm-8 col-md-6 mx-auto">
				<div id="pay-invoice" class="card">
					<div class="card-body">
						<div class="card-title">
							<h2 class="text-center">Pay Invoice</h2>
						</div>
						<hr />
						<form @submit.prevent="handlePayment" method="post">
							<input type="hidden" id="x_first_name" name="x_first_name" value="" />
							<input type="hidden" id="x_last_name" name="x_last_name" value="" />
							<input type="hidden" id="x_card_num" name="x_card_num" value="" />
							<input type="hidden" id="x_exp_date" name="x_exp_date" value="" />

							<div class="form-group">
								<label>Payment amount</label>
								<h2>${{ total.toFixed(2) }}</h2>
							</div>

							<div v-if="error" class="alert alert-danger">{{ error }}</div>

							<div class="form-group">
								<label for="cc-name" class="control-label">Name on card</label>
								<input
									id="cc-name"
									name="cc-name"
									type="text"
									class="form-control cc-name"
									autocomplete="cc-name"
									v-model="nameOnCard"
								/>
							</div>

							<div class="form-group">
								<label for="cc-number" class="control-label">Card number</label>
								<input
									id="cc-number"
									name="cc-number"
									type="tel"
									class="form-control cc-number"
									autocomplete="cc-number"
									v-model="cardNumber"
								/>
							</div>

							<div class="row">
								<div class="col-6">
									<div class="form-group">
										<label for="cc-exp" class="control-label">Expiration</label>
										<input
											id="cc-exp"
											name="cc-exp"
											type="tel"
											class="form-control cc-exp"
											placeholder="MM / YY"
											autocomplete="cc-exp"
											v-model="cardExpiry"
										/>
									</div>
								</div>
								<div class="col-6">
									<label for="x_card_code" class="control-label">Security code</label>
									<div class="input-group">
										<input
											id="x_card_code"
											name="x_card_code"
											type="tel"
											class="form-control cc-cvc"
											autocomplete="off"
											v-model="cardCvc"
										/>
										<div class="input-group-addon">
											<span
												class="fa fa-question-circle fa-lg"
												data-toggle="popover"
												data-container="body"
												data-html="true"
												data-title="Security Code"
												data-content="<div class='text-center one-card'>The 3 digit code on back of the card..<div class='visa-mc-cvc-preview'></div></div>"
												data-trigger="hover"
											></span>
										</div>
									</div>
								</div>
							</div>

							<div>
								<button
									id="payment-button"
									type="submit"
									class="btn btn-lg btn-success btn-block"
									:disabled="isProcessing"
								>
									<i class="fa fa-lock fa-lg"></i>&nbsp;
									<span id="payment-button-amount" v-if="!isProcessing"
										>Pay ${{ total.toFixed(2) }}</span
									>
									<span id="payment-button-sending" v-else>
										<span
											class="spinner-border spinner-border-sm"
											role="status"
											aria-hidden="true"
										></span>
										Processing...
									</span>
								</button>
							</div>
						</form>
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
import { useRouter } from "vue-router";
import axios from "axios";

export default defineComponent({
	name: "PaymentPage",
	setup() {
		const router = useRouter();
		const loading = ref(true);
		const isProcessing = ref(false);
		const cartItems = ref<CartItem[]>([]);
		const shipping = ref(5.99);
		const taxRate = 0.008;
		const error = ref<string | null>(null);

		const nameOnCard = ref("");
		const cardNumber = ref("");
		const cardExpiry = ref("");
		const cardCvc = ref("");

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
			} catch (err) {
				error.value = "Failed to load cart items. Please try again.";
				console.error("Error fetching cart items:", err);
			} finally {
				loading.value = false;
			}
		};

		const handlePayment = async () => {
			if (isProcessing.value) return;

			error.value = null;
			isProcessing.value = true;

			try {
				const csrfToken = document.cookie
					.split("; ")
					.find((row) => row.startsWith("csrftoken="))
					?.split("=")[1];

				if (!csrfToken) {
					throw new Error("CSRF token not found.");
				}

				const response = await api.post(
					"/api/cart/payment/",
					{
						name_on_card: nameOnCard.value,
						card_number: cardNumber.value,
						card_expiry: cardExpiry.value,
						card_cvc: cardCvc.value,
						amount: total.value,
					},
					{
						headers: {
							"X-CSRFToken": csrfToken,
						},
					}
				);

				if (response.data.message) {
					router.push("/");
				}
			} catch (err) {
				if (axios.isAxiosError(err)) {
					error.value = err.response?.data?.error || "Payment failed. Please try again.";
				} else if (err instanceof Error) {
					error.value = err.message;
				} else {
					error.value = "An unexpected error occurred.";
				}
				console.error("Payment error:", err);
			} finally {
				isProcessing.value = false;
			}
		};

		onMounted(() => {
			fetchCartItems();
		});

		return {
			loading,
			isProcessing,
			cartItems,
			subtotal,
			shipping,
			tax,
			total,
			error,
			nameOnCard,
			cardNumber,
			cardExpiry,
			cardCvc,
			handlePayment,
		};
	},
});
</script>

<style scoped>
#payment-button {
	position: relative;
}
#payment-button:disabled {
	opacity: 0.8;
}
</style>
