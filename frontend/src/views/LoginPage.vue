<template>
	<body>
		<div class="form-wrapper">
			<form class="login" @submit.prevent="handleLogin">
				<div id="login-form">
					<h2>Login</h2>

					<div class="flex-column">
						<label>Username </label>
					</div>
					<div class="inputForm">
						<input
							type="username"
							class="input"
							id="username"
							placeholder="Enter your username"
							required
							v-model="username"
						/>
					</div>
					<div class="flex-column">
						<label>Password </label>
					</div>
					<div class="inputForm">
						<input
							type="password"
							class="input"
							id="password"
							placeholder="Enter your Password"
							required
							v-model="password"
						/>
					</div>
					<button type="submit" id="submit" class="button-submit">Login</button>
				</div>
				<p>
					Don't have an account?
					<router-link to="/Register">Sign Up</router-link>.
				</p>
			</form>
		</div>
	</body>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useAuthStore } from "@/stores/auth";

const username = ref("");
const password = ref("");
const authStore = useAuthStore();

const handleLogin = async () => {
	await authStore.login(username.value, password.value);
};
</script>
<style>
.login *::after,
.login *::before {
	padding: 0;
	margin: 0;
	box-sizing: border-box;
}

.login {
	height: 520px;
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

.login * {
	color: white;
	font-family: "Poppins", sans-serif;
	letter-spacing: 0.5px;
	outline: none;
	border: none;
}

.login h2 {
	font-size: 32px;
	font-weight: 500;
	line-height: 42px;
	text-align: center;
}

.login label {
	display: block;
	margin-top: 30px;
	font-size: 16px;
	font-weight: 500;
}

.login input {
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

.login .button-submit {
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

body {
	background: linear-gradient(#248a57, #89EA5D);
	width: 100%;
	height: 2000px;
	background-size: cover;
	background-repeat: no-repeat;
}

.background {
	width: 430px;
	height: 520px;
	position: absolute;
	transform: translate(-50%, -50%);
	left: 50%;
	top: 50%;
}

.shape:first-child {
	background: linear-gradient(#1845ad, #23a2f6);
	left: -80px;
	top: -80px;
}

.shape:last-child {
	background: linear-gradient(#ad6018, #f69723);
	left: -30px;
	top: -80px;
}
</style>
