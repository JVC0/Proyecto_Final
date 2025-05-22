<template>
  <div class="products-container" role="list">
    <article 
      v-for="product in products" 
      :key="product.id" 
      class="product-card"
      role="listitem"
    >
      <div class="card" style="width: 18rem">
        <figure class="image" role="img" :aria-label="'Image of ' + product.name">
          <img 
            :src="product.image" 
            class="card-img-top product_image" 
            :alt="'Product image: ' + product.name" 
          />
        </figure>
        <div class="card-body">
          <h5 class="card-title">
            <router-link 
              :to="{ name: 'ProductDetail', params: { slug: product.slug } }"
              :aria-label="'View details for ' + product.name"
            >
              {{ product.name }}
            </router-link>
          </h5>
          <span 
            class="badge rounded-pill" 
            :aria-label="'Category: ' + product.category.name"
          >
            {{ product.category.name }}
          </span>
          <p class="form-label">${{ product.price }}</p>
          <div 
            role="status" 
            aria-live="polite"
            :aria-label="product.stock > 0 ? 'In stock' : 'Out of stock'"
          >
            <p v-if="product.stock > 0" class="text-muted">
              In stock: {{ product.stock }}
            </p>
            <p v-else class="text-danger">Out of stock</p>
          </div>
          <button
            @click="addToCart(product)"
            class="float-start btn btn-primary"
            :disabled="loading[product.id] || product.stock === 0"
            :aria-disabled="loading[product.id] || product.stock === 0"
            :aria-busy="loading[product.id]"
          >
            <span
              v-if="loading[product.id]"
              class="spinner-border spinner-border-sm"
              role="status"
              aria-hidden="true"
              aria-label="Adding to cart..."
            ></span>
            {{ loading[product.id] ? "Adding..." : "Add to Cart" }}
          </button>
          <div 
            class="input-group float-start mb-3" 
            v-if="product.stock > 0"
            role="group"
            aria-label="Quantity controls"
          >
            <button
              class="btn btn-outline-secondary"
              type="button"
              @click="decrementQuantity(product)"
              :disabled="quantities[product.id] <= 1"
              aria-label="Decrease quantity"
              :aria-describedby="'quantity-' + product.id"
            >
              -
            </button>
            <span 
              class="form-control text-center quantity-display"
              :id="'quantity-' + product.id"
              aria-live="polite"
            >
              {{ quantities[product.id] }}
            </span>
            <button
              class="btn btn-outline-secondary"
              type="button"
              @click="incrementQuantity(product)"
              :disabled="quantities[product.id] >= product.stock"
              aria-label="Increase quantity"
              :aria-describedby="'quantity-' + product.id"
            >
              +
            </button>
          </div>
        </div>
      </div>
    </article>
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

.product_image {
	height: 200px;
}

</style>
