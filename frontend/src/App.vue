<template>
	<nav class="navbar navbar-expand-lg custom_navbar">
		<div class="container-fluid">
			<router-link to="/" class="navbar-brand active">
				<strong>Home</strong>
			</router-link>
			<button
				class="navbar-toggler"
				type="button"
				data-bs-toggle="collapse"
				data-bs-target="#navbarNav"
				aria-controls="navbarNav"
				aria-expanded="false"
				aria-label="Toggle navigation"
			>
				<span class="navbar-toggler-icon"></span>
			</button>
			<div class="collapse navbar-collapse" id="navbarNav">
				<ul class="navbar-nav ms-auto">
					<li class="nav-item mt-2 me-2">
						<router-link to="/Cart">
							<i class="bi bi-cart4 custom-cart"></i>
						</router-link>
					</li>
					<li class="nav-item mt-2 me-2">
						<router-link :to="{ name: 'RecipeList' } ">
							Ver Recetas
						</router-link>
					</li>
					<li class="nav-item">
						<template v-if="isAuthenticated">
							<div class="d-inline-flex align-items-center">
								<span class="navbar-text mb-0 me-2">
									Hi there
									<router-link
										:to="{ name: 'ProfilePage', params: { username: authStore.user?.username } }"
									>
										{{ authStore.user?.username }}!
									</router-link>
								</span>
								<button class="btn btn-outline-danger" @click="handleLogout">Logout</button>
							</div>
						</template>
						<template v-else>
							<div class="d-inline-flex align-items-center">
								<span class="navbar-text mb-0 me-2"> You are not logged in. </span>
								<router-link to="/login" class="btn btn-outline-primary"> Login </router-link>
							</div>
						</template>
					</li>
				</ul>
			</div>
		</div>
	</nav>
	<div
		v-if="messageStore.message"
		class="global-message"
		:class="messageStore.isError ? 'bg-danger' : 'bg-success'"
	>
		<span>{{ messageStore.message }}</span>
		<button @click="messageStore.clearMessage()" aria-label="Close">
			<i class="bi bi-x-lg"></i>
		</button>
	</div>

	<router-view />
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useAuthStore } from "@/stores/auth";
import { useMessageStore } from "@/stores/message";

const messageStore = useMessageStore();
const authStore = useAuthStore();

const isAuthenticated = computed(() => {
	return authStore.isAuthenticated;
});

const handleLogout = () => {
	authStore.logout();
};
</script>

<style>
.custom-cart {
	margin-top: 100px;
}
.global-message {
	position: fixed;
	top: 100px;
	left: 50%;
	transform: translateX(-50%);
	padding: 1rem 2rem;
	text-align: center;
	z-index: 1000;
	border-radius: 10px;
	white-space: nowrap;
	box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
	display: flex;
	align-items: center;
	gap: 0.5rem;
}

.global-message button {
	margin-left: 1rem;
	background: transparent;
	border: none;
	cursor: pointer;
	display: flex;
	padding: 0;
	opacity: 0.7;
	transition: opacity 0.2s;
	color: inherit;
	font-size: 1.1rem;
}

.custom_navbar {
	background-color: rgb(15, 67, 41);
}

</style>
