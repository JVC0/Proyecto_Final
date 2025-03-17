<template>
    <body>
        <div class="form-wrapper">
            <form class="form" @submit.prevent="handleLogin">
                <div id="login-form">
                    <h2>Login</h2>

                    <div class="flex-column">
                        <label>Email </label>
                    </div>
                    <div class="inputForm">
                        <input
                            type="email"
                            class="input"
                            id="email"
                            placeholder="Enter your Email"
                            required
                            v-model="email"
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
                    <button type="submit" id="submit" class="button-submit">
                        Login
                    </button>
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

const email = ref("");
const password = ref("");
const authStore = useAuthStore();

const handleLogin = async () => {
    try {
        await authStore.login(email.value, password.value);
    } catch (error) {
        console.error("Login failed:", error);
    }
};
</script>
<style>
*::after,
*::before {
    padding: 0;
    margin: 0;
    box-sizing: border-box;
}

body {
    background-image: url("https://wallpapercat.com/w/full/8/b/6/854961-1920x1080-desktop-full-hd-kfc-wallpaper-image.jpg");
    background-size: cover;
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

form {
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

form * {
    color: white;
    font-family: "Poppins", sans-serif;
    letter-spacing: 0.5px;
    outline: none;
    border: none;
}

form h3 {
    font-size: 32px;
    font-weight: 500;
    line-height: 42px;
    text-align: center;
}

form label {
    display: block;
    margin-top: 30px;
    font-size: 16px;
    font-weight: 500;
}

input {
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

.button-submit {
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
</style>
