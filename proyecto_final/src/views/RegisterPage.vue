<template>
    <div class="background">
        <div class="shape"></div>
        <div class="shape"></div>
    </div>
    <form @submit.prevent="handleRegister">
        <h2>CREATE ACCOUNT</h2>
        <label for="email">Email</label>
        <input
            id="email"
            type="email"
            placeholder="Email"
            required
            v-model="email"
        />
        <label for="username">Username:</label>
        <input
            v-model="username"
            type="text"
            placeholder="Username"
            id="username"
            required
        />
        <label for="password">Password</label>
        <input
            id="password"
            type="password"
            placeholder="Password"
            required
            v-model="password"
        />

        <button type="submit" id="submit" class="button-submit">
            Create Account
        </button>

        <div class="form">
            <p>
                Already have an account?
                <router-link to="/login">Login here</router-link>.
            </p>
        </div>
    </form>
    <p v-if="error" class="error">{{ error }}</p>
</template>

<script lang="ts">
import { ref } from "vue";
import api from "@/utils/api";
import { useRouter } from "vue-router";
import axios from "axios"; // Import axios for type checking

export default {
    name: "RegisterPage",
    setup() {
        const email = ref("");
        const username = ref("");
        const password = ref("");
        const error = ref("");
        const router = useRouter();

        const handleRegister = async () => {
            try {
                // Get the CSRF token from the cookie
                const csrfToken = document.cookie
                    .split("; ")
                    .find((row) => row.startsWith("csrftoken="))
                    ?.split("=")[1];

                if (!csrfToken) {
                    throw new Error("CSRF token not found.");
                }

                // Include the CSRF token in the request headers
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
                // Type guard to check if err is an AxiosError
                if (axios.isAxiosError(err)) {
                    error.value =
                        err.response?.data?.error ||
                        "Registration failed. Please try again.";
                } else if (err instanceof Error) {
                    // Handle other types of errors
                    error.value = err.message;
                } else {
                    // Handle unknown errors
                    error.value = "An unexpected error occurred.";
                }
            }
        };

        return {
            email,
            username,
            password,
            error,
            handleRegister,
        };
    },
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
.error {
    color: red;
}
</style>
