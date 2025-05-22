<template>
	<div class="edit-profile">
		<h2>Edit Profile</h2>

		<form @submit.prevent="handleSubmit">
			<!-- User Fields -->
			<div class="form-group">
				<label>First Name</label>
				<input type="text" v-model="form.user.first_name" />
				<p v-if="errors.user_first_name" class="error">{{ errors.user_first_name }}</p>
			</div>

			<div class="form-group">
				<label>Last Name</label>
				<input type="text" v-model="form.user.last_name" />
				<p v-if="errors.user_last_name" class="error">{{ errors.user_last_name }}</p>
			</div>

			<!-- Profile Fields -->
			<div class="form-group">
				<label>Profile Picture</label>
				<input type="file" @change="handleFileChange" accept="image/*" />
				<img v-if="previewImage" :src="previewImage" class="avatar-preview" />
				<p v-if="errors.profile_avatar" class="error">{{ errors.profile_avatar }}</p>
			</div>

			<div class="form-group">
				<label>Bio</label>
				<textarea v-model="form.profile.bio" rows="4"></textarea>
				<p v-if="errors.profile_bio" class="error">{{ errors.profile_bio }}</p>
			</div>

			<button type="submit" :disabled="loading">
				{{ loading ? "Saving..." : "Save Changes" }}
			</button>
		</form>
	</div>
</template>

<script lang="ts">
import { ref, reactive, onMounted } from "vue";
import { useRoute } from "vue-router";
import api from "@/utils/api";
import { useMessageStore } from "@/stores/message";

interface FormData {
	user: {
		first_name: string;
		last_name: string;
	};
	profile: {
		bio: string;
		avatar: File | null;
	};
}

interface Errors {
	[key: string]: string;
}

interface Message {
	text: string;
	type: "success" | "error";
}

export default {
	name: "EditProfile",
	setup() {
		const route = useRoute();
		const form = reactive<FormData>({
			user: {
				first_name: "",
				last_name: "",
			},
			profile: {
				bio: "",
				avatar: null,
			},
		});

		const previewImage = ref("");
		const errors = reactive<Errors>({});
		const loading = ref(false);
		const message = ref<Message | null>(null);
		const messageStore = useMessageStore();
		const fetchProfile = async () => {
			try {
				const username = route.params.username;
				const response = await api.get(`/api/profile/${username}/edit/`);
				form.user.first_name = response.data.data.first_name || "";
				form.user.last_name = response.data.data.last_name || "";
				form.profile.bio = response.data.data.bio || "";
				if (response.data.data.avatar) {
					previewImage.value = response.data.data.avatar;
				}
			} catch (error: any) {
				showMessage("Failed to load profile", "error");
				console.error("Error fetching profile:", error);
			}
		};

		const handleFileChange = (e: Event) => {
			const target = e.target as HTMLInputElement;
			const file = target.files?.[0];
			if (!file) return;

			errors.profile_avatar = "";

			if (!file.type.startsWith("image/")) {
				errors.profile_avatar = "Please select an image file";
				target.value = "";
				return;
			}

			if (file.size > 1024 * 1024 * 2) {
				errors.profile_avatar = "Image must be less than 2MB";
				target.value = "";
				return;
			}

			form.profile.avatar = file;

			const reader = new FileReader();
			reader.onload = (e) => (previewImage.value = e.target?.result as string);
			reader.readAsDataURL(file);
		};

		const handleSubmit = async () => {
			loading.value = true;
			clearErrors();
			message.value = null;

			try {
				const formData = new FormData();

				formData.append("first_name", form.user.first_name);
				formData.append("last_name", form.user.last_name);

				formData.append("bio", form.profile.bio);
				if (form.profile.avatar) {
					formData.append("avatar", form.profile.avatar);
				}

				const csrfToken = document.cookie
					.split("; ")
					.find((row) => row.startsWith("csrftoken="))
					?.split("=")[1];

				const username = route.params.username;
				const response = await api.post(`/api/profile/${username}/edit/`, formData, {
					headers: {
						"Content-Type": "multipart/form-data",
						"X-CSRFToken": csrfToken,
					},
				});

				showMessage("Profile updated successfully!", "success");
				if (response.data.data.avatar) {
					previewImage.value = response.data.data.avatar;
				}
			} catch (error: any) {
				console.error("Error updating profile:", error);
				if (error.response?.data?.errors) {
					Object.assign(errors, error.response.data.errors);
				} else {
					showMessage(error.response?.data?.message || "Failed to update profile", "error");
				}
			} finally {
				loading.value = false;
			}
		};

		const showMessage = (text: string, type: "success" | "error") => {
			message.value = { text, type };
			messageStore.setMessage(text, type === "error");
			setTimeout(() => (message.value = null), 5000);
		};

		const clearErrors = () => {
			Object.keys(errors).forEach((key) => delete errors[key]);
		};
		onMounted(fetchProfile);

		return {
			form,
			previewImage,
			errors,
			loading,
			message,
			handleFileChange,
			handleSubmit,
		};
	},
};
</script>

<style scoped>
.edit-profile {
	max-width: 500px;
	margin: 0 auto;
	padding: 20px;
}
.form-group {
	margin-bottom: 1rem;
}
.avatar-preview {
	display: block;
	max-width: 150px;
	max-height: 150px;
	margin-top: 10px;
	border-radius: 50%;
}
.error {
	color: red;
	font-size: 0.9rem;
}
.message {
	margin-top: 1rem;
	padding: 0.5rem;
}
.message.success {
	color: green;
	background: #f0fff0;
}
.message.error {
	color: red;
	background: #fff0f0;
}
input,
textarea {
	width: 100%;
	padding: 8px;
	border: 1px solid #ddd;
	border-radius: 4px;
	box-sizing: border-box;
}
textarea {
	min-height: 100px;
}
button {
	background-color: #4caf50;
	color: white;
	padding: 10px 15px;
	border: none;
	border-radius: 4px;
	cursor: pointer;
}
button:disabled {
	background-color: #cccccc;
	cursor: not-allowed;
}
</style>
