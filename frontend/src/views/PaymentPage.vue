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
							<input type="hidden" id="x_first_name" required name="x_first_name" value="" />
							<input type="hidden" id="x_last_name" required name="x_last_name" value="" />
							<input type="hidden" id="x_card_num" required name="x_card_num" value="" />
							<input type="hidden" id="x_exp_date" required name="x_exp_date" value="" />

							<div class="form-group">
								<label>Payment amount</label>
								<h2>${{ total.toFixed(2) }}</h2>
							</div>

							<div class="form-group">
								<label for="cc-name" class="control-label">Name on card</label>
								<input
									id="cc-name"
									name="cc-name"
									type="text"
									class="form-control cc-name"
									:class="{ 'is-invalid': errors.nameOnCard }"
									autocomplete="cc-name"
									v-model="nameOnCard"
									required
								/>
							</div>

							<div class="form-group">
								<label for="cc-number" class="control-label">Card number</label>
								<input
									id="cc-number"
									name="cc-number"
									type="tel"
									class="form-control cc-number"
									:class="{ 'is-invalid': errors.cardNumber }"
									autocomplete="cc-number"
									v-model="cardNumber"
									@input="formatCardNumber"
									required
								/>
								<div v-if="errors.cardNumber" class="invalid-feedback">
									{{ errors.cardNumber }}
								</div>
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
											:class="{ 'is-invalid': errors.cardExpiry }"
											placeholder="MM / YY"
											autocomplete="cc-exp"
											v-model="cardExpiry"
											@input="formatExpiry"
											required
										/>
										<div v-if="errors.cardExpiry" class="invalid-feedback">
											{{ errors.cardExpiry }}
										</div>
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
											:class="{ 'is-invalid': errors.cardCvc }"
											autocomplete="off"
											v-model="cardCvc"
											@input="limitCvcLength"
											maxlength="3"
											required
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
										<div v-if="errors.cardCvc" class="invalid-feedback">
											{{ errors.cardCvc }}
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
import { useMessageStore } from "@/stores/message";

export default defineComponent({
	name: "PaymentPage",
	setup() {
		const router = useRouter();
		const messageStore = useMessageStore();
		const loading = ref(true);
		const isProcessing = ref(false);
		const cartItems = ref<CartItem[]>([]);
		const shipping = ref(5.99);
		const taxRate = 0.008;

		const nameOnCard = ref("");
		const cardNumber = ref("");
		const cardExpiry = ref("");
		const cardCvc = ref("");

		const errors = ref({
			nameOnCard: "",
			cardNumber: "",
			cardExpiry: "",
			cardCvc: "",
		});

		const clearErrors = () => {
			errors.value = {
				nameOnCard: "",
				cardNumber: "",
				cardExpiry: "",
				cardCvc: "",
			};
		};

		const formatExpiry = (e: Event) => {
			const input = e.target as HTMLInputElement;
			let value = input.value.replace(/\D/g, "");

			if (value.length > 2) {
				value = value.substring(0, 2) + "/" + value.substring(2, 4);
			}

			input.value = value;
			cardExpiry.value = value;
		};

		const formatCardNumber = (e: Event) => {
			const input = e.target as HTMLInputElement;
			let value = input.value.replace(/\D/g, "");

			if (value.length > 16) {
				value = value.substring(0, 16);
			}

			const formattedValue = value.replace(/(\d{4})(?=\d)/g, "$1-");
			input.value = formattedValue;
			cardNumber.value = value;
		};

		const limitCvcLength = (e: Event) => {
			const input = e.target as HTMLInputElement;
			let value = input.value.replace(/\D/g, "");
			if (value.length > 3) {
				value = value.substring(0, 3);
			}
			input.value = value;
			cardCvc.value = value;
		};

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

		const validateForm = () => {
			let isValid = true;
			clearErrors();

			if (!nameOnCard.value.trim()) {
				errors.value.nameOnCard = "Name on card is required";
				isValid = false;
			}

			const rawCardNumber = cardNumber.value.replace(/\D/g, "");
			if (!rawCardNumber || rawCardNumber.length !== 16) {
				errors.value.cardNumber = "Please enter a valid 16-digit card number";
				isValid = false;
			}

			const expParts = cardExpiry.value.split("/");
			if (
				!cardExpiry.value ||
				expParts.length !== 2 ||
				expParts[0].length !== 2 ||
				expParts[1].length !== 2
			) {
				errors.value.cardExpiry = "Please enter a valid expiration date (MM/YY)";
				isValid = false;
			}

			if (!cardCvc.value || cardCvc.value.length !== 3) {
				errors.value.cardCvc = "Please enter a valid 3-digit security code";
				isValid = false;
			}

			return isValid;
		};

		const fetchCartItems = async () => {
			loading.value = true;
			try {
				const response = await api.get("/api/cart/");
				cartItems.value = response.data.items || [];
			} catch (error: any) {
				messageStore.setMessage(error.response?.data?.message || "Failed to load cart items", true);
			} finally {
				loading.value = false;
			}
		};

		const handlePayment = async () => {
			if (isProcessing.value) return;

			if (!validateForm()) {
				const errorMessages = Object.values(errors.value)
					.filter((msg) => msg)
					.join(". ");
				if (errorMessages) {
					messageStore.setMessage(errorMessages, true);
				}
				return;
			}

			isProcessing.value = true;

			try {
				const csrfToken = document.cookie
					.split("; ")
					.find((row) => row.startsWith("csrftoken="))
					?.split("=")[1];

				const response = await api.post(
					"/api/cart/payment/",
					{
						card_number: cardNumber.value.replace(/\D/g, ""),
						exp_date: cardExpiry.value.replace(/\D/g, ""),
						cvc: cardCvc.value,
						name_on_card: nameOnCard.value,
					},
					{
						headers: {
							"X-CSRFToken": csrfToken,
						},
					}
				);

				if (response.data.message === "Payment successful") {
					messageStore.setMessage(response.data.message);
					router.push("/");
				} else {
					messageStore.setMessage(response.data.message, true);
				}
			} catch (error: any) {
				messageStore.setMessage(
					error.response?.data?.message || "Payment failed. Please try again.",
					true
				);
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
			nameOnCard,
			cardNumber,
			cardExpiry,
			cardCvc,
			errors,
			formatExpiry,
			formatCardNumber,
			limitCvcLength,
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
.alert-danger {
	margin-top: 20px;
	margin-bottom: 20px;
}
</style>
