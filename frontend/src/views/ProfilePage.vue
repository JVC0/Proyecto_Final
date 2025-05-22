<template>
  <div v-if="profile" role="main" aria-live="polite">
    <div class="profile_content">
      <img 
        :src="profile.avatar" 
        class="profile_avatar" 
        role="img"
        :alt="`User avatar for ${profile.user.username}`"
        aria-labelledby="username"
      >
      <br aria-hidden="true">
      
      <div class="profile_username" id="username">
        <h1 tabindex="0">{{ profile.user.username }}</h1>
      </div>
      <br aria-hidden="true">
      
      <div class="profile_fullname" aria-label="Full name">
        {{ profile.user.first_name }} {{ profile.user.last_name }}
      </div>
      <br aria-hidden="true">
      
      <div class="profile_email" aria-label="Email address">
        <span>{{ profile.user.email }}</span>
      </div>
      
      <div class="profile_bio" aria-label="Biography">
        <span>Bio: {{ profile.bio }}</span>
      </div>
      <br aria-hidden="true">
      
      <div class="row" role="navigation" aria-label="Profile actions">
        <router-link
          class="btn btn-primary col-5 custom_btn"
          role="button"
          :aria-label="`View groups created by ${profile.user.username}`"
          :to="{ name: 'GroupPage', params: { username: profile.user.username } }"
        >
          View Groups
        </router-link>
        
        <div class="col-2" aria-hidden="true"></div>
        
        <router-link
          class="btn btn-primary add_button col-5 custom_btn"
          role="button"
          :aria-label="`Edit profile for ${profile.user.username}`"
          :to="{ name: 'EditProfilePage', params: { username: route.params.username } }"
        >
          Edit Profile
        </router-link>
      </div>
      
      <div class="row mt-3">
        <button 
          class="btn btn-danger col-12 custom_btn"
          aria-label="Delete profile"
          @click="showDeleteModal = true"
        >
          Delete Profile
        </button>
      </div>
    </div>

    <div 
      v-if="showDeleteModal" 
      class="modal-overlay"
      role="dialog"
      aria-modal="true"
      aria-labelledby="dialogHeading"
    >
      <div class="modal-content">
        <h3 id="dialogHeading" tabindex="0">Confirm action</h3>
        <p aria-live="assertive">
          Are you sure you want to permanently delete your profile? This action cannot be undone.
        </p>

        <p id="confirmationInstruction">
          To confirm, please write your username: 
        </p>
        <input
          v-model="confirmationText"
          type="text"
          :placeholder="'Write ' + profile.user.username"
          class="form-control mb-3"
          aria-labelledby="confirmationInstruction"
          aria-required="true"
        >

        <div class="modal-buttons" role="group" aria-label="Confirmation buttons">
          <button
            class="btn btn-danger"
            @click="deleteProfile"
            :disabled="confirmationText !== profile.user.username"
            aria-describedby="confirmationError"
          >
            Delete
          </button>
          <button 
            class="btn btn-secondary" 
            @click="showDeleteModal = false"
            aria-label="Cancel profile deletion"
          >
            Cancel
          </button>
        </div>

        <div 
          v-if="deleteMessage" 
          role="alert"
          aria-live="assertive"
          class="alert mt-3" 
          :class="deleteMessageClass"
        >
          {{ deleteMessage }}
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { useRoute, useRouter } from "vue-router";
import api from "@/utils/api";
import { Profile } from "@/types/profile";
import { useAuthStore } from "@/stores/auth";

export default defineComponent({
	name: "ProfilePage",
	data() {
		return {
			profile: null as Profile | null,
			showDeleteModal: false,
			confirmationText: "",
			deleteMessage: "",
			deleteMessageClass: "",
		};
	},
	setup() {
		const route = useRoute();
		const router = useRouter();
		const authStore = useAuthStore();
		return { route, router, authStore };
	},
	mounted() {
		this.getProfile();
	},
	methods: {
		getProfile() {
			const username = this.route.params.username;
			api
				.get(`/api/profile/${username}/`)
				.then((response) => {
					this.profile = response.data;
				})
				.catch((error) => {
					console.log(error);
				});
		},
		async deleteProfile() {
			if (this.confirmationText !== this.profile?.user.username) {
				return;
			}

			try {
				const username = this.route.params.username;
				const csrfToken = this.getCsrfToken();

				if (!csrfToken) {
					throw new Error("CSRF token not found");
				}

				const response = await api.delete(`/api/profile/${username}/delete/`, {
					headers: {
						"X-CSRFToken": csrfToken,
					},
				});

				this.deleteMessage = "Perfil eliminado correctamente. Cerrando sesión...";
				this.deleteMessageClass = "alert-success";

				await this.authStore.logout();

				setTimeout(() => {
					this.router.push("/");
				}, 1000);
			} catch (error: any) {
				this.deleteMessage = error.response?.data?.error || "Error al eliminar el perfil";
				this.deleteMessageClass = "alert-danger";
				console.error(error);
			}
		},
		getCsrfToken(): string | null {
			const cookieValue = document.cookie
				.split("; ")
				.find((row) => row.startsWith("csrftoken="))
				?.split("=")[1];
			return cookieValue || null;
		},
	},
});
</script>

<style scoped>
.profile_content {
	color: rgb(242, 242, 242);
	margin-top: 40px;
	margin-left: 100px;
	margin-right: 100px;
	padding: 8px;
	background-color: rgba(162, 162, 162, 0.534);
}

.profile_avatar {
	border-radius: 50%;
	height: 300px;
	width: 300px;
}

.profile_email {
	text-decoration: underline;
}

/* Modal styles */
.modal-overlay {
	position: fixed;
	top: 0;
	left: 0;
	right: 0;
	bottom: 0;
	background-color: rgba(0, 0, 0, 0.7);
	display: flex;
	justify-content: center;
	align-items: center;
	z-index: 1000;
}

.modal-content {
	background-color: white;
	padding: 20px;
	border-radius: 5px;
	max-width: 500px;
	width: 90%;
	color: black;
}

.modal-buttons {
	display: flex;
	gap: 10px;
}

.alert {
	padding: 10px;
	border-radius: 4px;
}

.alert-success {
	background-color: #d4edda;
	color: #155724;
}

.alert-danger {
	background-color: #f8d7da;
	color: #721c24;
}

.form-control {
	margin-bottom: 10px;
}

.btn-danger {
	background-color: #dc3545;
	border-color: #dc3545;
}
</style>
