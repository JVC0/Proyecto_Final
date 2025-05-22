<template>
  <nav aria-label="Group management actions">
    <router-link 
      class="btn btn-primary add_button"
      role="button"
      aria-label="Create new group"
      :to="{name: 'AddGroup', params: { username: route.params.username }}">
      Crear un Grupo
    </router-link>
  </nav>

  <div 
    class="groups_content"
    role="region" 
    aria-label="List of user groups"
  >
    <div 
      v-for="productGroup in productGroups" 
      :key="productGroup.id"
      role="article"
      aria-labelledby="`group-${productGroup.id}-title`"
      class="group-card"
    >
      <div class="card" style="width: 18rem">
        <div class="card-body">
          <h5 
            :id="`group-${productGroup.id}-title`" 
            class="card-title"
            tabindex="0"
          >
            {{ productGroup.name }}
          </h5>
          
          <div 
            role="list"
            aria-label="Group products"
          >
            <div 
              v-for="product in productGroup.products" 
              :key="product.id"
              role="listitem"
              :aria-label="product.name"
            >
              {{ product.name }}
            </div>
          </div>

          <router-link
            class="btn btn-primary"
            role="button"
            :aria-label="`View details for group: ${productGroup.name}`"
            :to="{
              name: 'GroupDetail',
              params: { username: route.params.username, id: productGroup.id },
            }"
          >
            Ver Grupo
          </router-link>
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
	flex-wrap: wrap;
	gap: 20px;
	padding: 20px;
	color: rgb(242, 242, 242);
	margin-top: 40px;
	margin-left: 100px;
	margin-right: 100px;
	background-color: rgba(162, 162, 162, 0.534);
}

.add_button {
	margin-left: 700px;
	margin-top: 25px;
}

.card {
	display: flex;
	flex-wrap: wrap;
	margin-top: 40px;
	margin-left: 40px;
}
</style>
