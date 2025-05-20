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
						<form action="" method="post" novalidate="novalidate">
							<input type="hidden" id="x_first_name" name="x_first_name" value="" />
							<input type="hidden" id="x_last_name" name="x_last_name" value="" />
							<input type="hidden" id="x_card_num" name="x_card_num" value="" />
							<input type="hidden" id="x_exp_date" name="x_exp_date" value="" />
							<div class="form-group">
								<label>Payment amount</label>
								<h2>${{ total.toFixed(2) }}</h2>
							</div>
							<div class="form-group has-success">
								<label for="cc-name" class="control-label">Name on card</label>
								<input
									id="cc-name"
									name="cc-name"
									type="text"
									class="form-control cc-name valid"
									data-val="true"
									data-val-required="Please enter the name on card"
									autocomplete="cc-name"
									aria-required="true"
									aria-invalid="false"
									aria-describedby="cc-name-error"
								/>
								<span
									class="help-block field-validation-valid"
									data-valmsg-for="cc-name"
									data-valmsg-replace="true"
								></span>
							</div>
							<div class="form-group">
								<label for="cc-number" class="control-label">Card number</label>
								<input
									id="cc-number"
									name="cc-number"
									type="tel"
									class="form-control cc-number identified visa"
									value=""
									data-val="true"
									data-val-required="Please enter the card number"
									data-val-cc-number="Please enter a valid card number"
									autocomplete="cc-number"
								/>
								<span
									class="help-block"
									data-valmsg-for="cc-number"
									data-valmsg-replace="true"
								></span>
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
											value=""
											data-val="true"
											data-val-required="Please enter the card expiration"
											data-val-cc-exp="Please enter a valid month and year"
											placeholder="MM / YY"
											autocomplete="cc-exp"
										/>
										<span
											class="help-block"
											data-valmsg-for="cc-exp"
											data-valmsg-replace="true"
										></span>
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
											value=""
											data-val="true"
											data-val-required="Please enter the security code"
											data-val-cc-cvc="Please enter a valid security code"
											autocomplete="off"
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
								<button id="payment-button" type="submit" class="btn btn-lg btn-success btn-block">
									<i class="fa fa-lock fa-lg"></i>&nbsp;
									<span id="payment-button-amount">Pay ${{ total.toFixed(2) }}</span>
									<span id="payment-button-sending" style="display: none">Sending…</span>
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

export default defineComponent({
	name: "PaymentPage",
	setup() {
		const loading = ref(true);
		const cartItems = ref<CartItem[]>([]);
		const shipping = ref(5.99);
		const taxRate = 0.008;
		const error = ref<string | null>(null);
		const email = ref("");
		const username = ref("");
		const password = ref("");

		const router = useRouter();

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
		const handlepayment = async () => {
			try {
				const csrfToken = document.cookie
					.split("; ")
					.find((row) => row.startsWith("csrftoken="))
					?.split("=")[1];

				if (!csrfToken) {
					throw new Error("CSRF token not found.");
				}

				const response = await api.post(
					"/api/auth/register/",
					{
						email: email.value,
						username: username.value,
						password: password.value,
					},
					{
						headers: {
							"X-CSRFToken": csrfToken,
						},
					}
				);

				if (response.data.message) {
					router.push("/login");
				}
			} catch (err) {
				if (axios.isAxiosError(err)) {
					error.value = err.response?.data?.error || "Registration failed. Please try again.";
				} else if (err instanceof Error) {
					error.value = err.message;
				} else {
					error.value = "An unexpected error occurred.";
				}
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
		};
	},
});
</script>
