<template>
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
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
                    <li class="nav-item">
                        <template v-if="isAuthenticated">
                            <div class="d-inline-flex align-items-center">
                                <span class="navbar-text mb-0 me-2">
                                    Hi there {{ authStore.user?.username }}! You
                                    are logged in.
                                </span>
                                <button
                                    class="btn btn-outline-danger"
                                    @click="handleLogout"
                                >
                                    Logout
                                </button>
                            </div>
                        </template>
                        <template v-else>
                            <div class="d-inline-flex align-items-center">
                                <span class="navbar-text mb-0 me-2">
                                    You are not logged in.
                                </span>
                                <router-link
                                    to="/login"
                                    class="btn btn-outline-primary"
                                >
                                    Login
                                </router-link>
                            </div>
                        </template>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
    <router-view />
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useAuthStore } from "@/stores/auth";

const authStore = useAuthStore();

const isAuthenticated = computed(() => authStore.isAuthenticated);

const handleLogout = () => {
    authStore.logout();
};
</script>

<style>
/* Your existing styles here */
</style>
