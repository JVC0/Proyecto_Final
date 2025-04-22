<template>
    <div v-if="profile">
        <div class="profile_content">
            <img :src="profile.avatar" class="profile_avatar" alt="avatar">
            <br>
            <div class="profile_username"><span><h1>{{ profile.user.username }}</h1></span></div>
            <br>
            <div class="profile_fullname">{{ profile.user.first_name }} {{ profile.user.last_name }}</div>
            <br>
            <div class="profile_email"><span>{{ profile.user.email }}</span></div>
            <br>
            <button class="btn btn-primary">Ver grupos de productos</button>
            <br>
            <div class="profile_bio"><span>{{ profile.bio }}</span></div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { useRoute } from "vue-router";
import api from "@/utils/api";

interface Profile {
    id: number;
    avatar: string;
    bio: string;
    user: User;
}

interface User {
    id: number;
    first_name: string;
    last_name: string;
    email: string;
    username: string;
}

export default defineComponent({
    name: "ProfilePage",
    data() {
        return {
            profile: null as Profile | null,
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
            api.get(`/api/profile/${username}/`)
                .then((response) => {
                    this.profile = response.data;
                })
                .catch((error) => {
                    console.log(error);
                });
        },}});
</script>

<style scoped>
.profile_content{
    color: rgb(242, 242, 242);
    margin-top: 40px;
    margin-left: 100px;
    margin-right: 100px;
    padding: 8px;
    background-color: rgba(162, 162, 162, 0.534);
}

.profile_avatar {
    border-radius: 50%;
}

.profile_email {
    text-decoration: underline;
}

</style>