<template>
	<div class="background">
		<div class="shape" aria-hidden="true"></div>
		<div class="shape" aria-hidden="true"></div>
	</div>
	<main class="container">
		<form class="register" @submit.prevent="handleRegister">
			<h2 class="register-title">CREATE ACCOUNT</h2>
			<div class="form-group">
				<label for="email" class="sr-only">Email</label>
				<input
					id="email"
					type="email"
					placeholder="Email"
					required
					v-model="email"
					aria-required="true"
					autocomplete="email"
					class="form-input"
				/>
			</div>
			<div class="form-group">
				<label for="username" class="sr-only">Username</label>
				<input
					v-model="username"
					type="text"
					placeholder="Username"
					id="username"
					required
					aria-required="true"
					autocomplete="username"
					class="form-input"
				/>
			</div>

			<div class="form-group">
				<label for="password" class="sr-only">Password</label>
				<input
					id="password"
					type="password"
					placeholder="Password"
					required
					v-model="password"
					aria-required="true"
					autocomplete="new-password"
					class="form-input"
					aria-describedby="password-requirements"
				/>
			</div>

			<button type="submit" class="button-submit">Create Account</button>

			<div class="login-redirect">
				<p>
					Already have an account?
					<router-link to="/login" class="login-link">Login here</router-link>.
				</p>
			</div>
		</form>
	</main>
</template>

<script lang="ts">
import { ref } from "vue";
import api from "@/utils/api";
import { useRouter } from "vue-router";
import { useMessageStore } from "@/stores/message";

export default {
	name: "RegisterPage",
	setup() {
		const email = ref("");
		const username = ref("");
		const password = ref("");
		const router = useRouter();
		const messageStore = useMessageStore();

		const handleRegister = async () => {
			try {
				const csrfToken = document.cookie
					.split("; ")
					.find((row) => row.startsWith("csrftoken="))
					?.split("=")[1];

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

				if (response.data.success) {
					messageStore.setMessage(response.data.message || "Registration successful!");
					router.push("/login");
				} else if (response.data.message) {
					messageStore.setMessage(response.data.message);
					router.push("/login");
				}
			} catch (error: any) {
				if (error.response?.data?.message) {
					messageStore.setMessage(error.response.data.message);
				} else {
					messageStore.setMessage("Registration failed. Please try again.", true);
				}
			}
		};

		return {
			email,
			username,
			password,
			handleRegister,
		};
	},
};
</script>
<style>
.register *::after,
.register *::before {
	padding: 0;
	margin: 0;
	box-sizing: border-box;
}

.register {
	height: 560px;
	width: 400px;
	background-color: rgba(160, 160, 160, 0.3);
	position: absolute;
	transform: translate(-50%, -50%);
	border-radius: 10px;
	top: 50%;
	left: 50%;
	backdrop-filter: blur(10px);
	border: 2px solid rgba(255, 255, 255, 0.1);
	padding: 50px 35px;
	box-shadow: 0 0 40px rgba(8, 7, 16, 0.6);
}

.register * {
	color: white;
	font-family: "Poppins", sans-serif;
	letter-spacing: 0.5px;
	outline: none;
	border: none;
}

.register h2 {
	font-size: 32px;
	font-weight: 500;
	line-height: 42px;
	text-align: center;
}

.register label {
	display: block;
	margin-top: 30px;
	font-size: 16px;
	font-weight: 500;
}

.register input {
	display: block;
	height: 50px;
	width: 100%;
	background-color: rgba(255, 255, 255, 0.0713);
	border-radius: 3px;
	padding: 0 10px;
	margin-top: 8px;
	font-size: 14px;
	font-weight: 300;
}

.register .button-submit {
	margin-top: 30px;
	width: 100%;
	background-color: white;
	padding: 15px 10px;
	font-size: 18px;
	font-weight: 500;
	cursor: pointer;
	color: black;
	border-radius: 5px;
}

.register .error {
	color: red;
}

.background {
	width: 430px;
	height: 520px;
	position: absolute;
	transform: translate(-50%, -50%);
	left: 50%;
	top: 50%;
}

.background .shape:first-child {
	background: linear-gradient(#1845ad, #23a2f6);
	left: -80px;
	top: -80px;
}

.background .shape:last-child {
	background: linear-gradient(#ad6018, #f69723);
	left: -30px;
	top: -80px;
}
</style>
