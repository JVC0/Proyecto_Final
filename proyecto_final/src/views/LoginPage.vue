<template>
<body>
    <div class="form-wrapper">
    <form class="form">
    <div id="login-form">
        <h2>Login</h2>
        
        <div class="flex-column">
            <label>Email </label></div>
            <div class="inputForm">
                <input type="email" class="input" id="email" placeholder="Enter your Email">
            </div>
        <div class="flex-column">
            <label>Password </label></div>
            <div class="inputForm">
                <input type="password" class="input" id="password" placeholder="Enter your Password">
            </div>
        <button type="submit" id="submit" class="button-submit">Login</button>
        </div>
        <p class="p">Don't have an account? <a href="register.html">Sign Up</a>.</p>
    </form>
    </div>
</body>
</template>

<!-- <script>
import axios from 'axios'

export default {
    name: 'LoginPage',
    data() {
        return {
            username: '',
            password: '',
            errors: []
        }
    },

    methods: {
        async submitForm() {
            axios.defaults.headers.common["Authorization"] = ""

            localStorage.removeItem("token")

            const formData = {
                username: this.username,
                password: this.password
            }

            await axios
                .post("/api/v1/token/login/", formData)
                .then(response => {
                    const token = response.data.auth_token

                    this.$store.commit('setToken', token)
                    
                    axios.defaults.headers.common["Authorization"] = "Token " + token

                    localStorage.setItem("token", token)

                    const toPath = this.$route.query.to || '/cart'

                    this.$router.push(toPath)
                })
                .catch(error => {
                    if (error.response) {
                        for (const property in error.response.data) {
                            this.errors.push(`${property}: ${error.response.data[property]}`)
                        }
                    } else {
                        this.errors.push('Something went wrong. Please try again')
                        
                        console.log(JSON.stringify(error))
                    }
                })
        }
    }
}
</script> -->
<style>
*::after, *::before{
    padding: 0;
    margin: 0;
    box-sizing: border-box;
}

body{
    background-image: url('https://wallpapercat.com/w/full/8/b/6/854961-1920x1080-desktop-full-hd-kfc-wallpaper-image.jpg');
    background-size: cover;
}

.background{
    width: 430px;
    height: 520px;
    position: absolute;
    transform: translate(-50%, -50%);
    left: 50%;
    top: 50%;
}

.shape:first-child{
    background: linear-gradient(#1845ad, #23a2f6);
    left: -80px;
    top: -80px;
}

.shape:last-child{
    background: linear-gradient(#ad6018, #f69723);
    left: -30px;
    top: -80px;
} 

form{
    height: 520px;
    width: 400px;
    background-color: rgba(160, 160, 160, 0.3);
    position: absolute;
    transform: translate(-50%, -50%);
    border-radius: 10px;
    top: 50%;
    left: 50%;
    backdrop-filter: blur(10px);
    border: 2px solid rgba(255,255,255,0.1);
    padding: 50px 35px;
    box-shadow: 0 0 40px rgba(8, 7, 16, 0.6);
}

form *{
    color: white;
    font-family: "Poppins", sans-serif;
    letter-spacing: 0.5px;
    outline: none;
    border: none;
}

form h3{
    font-size: 32px;
    font-weight: 500;
    line-height: 42px;
    text-align: center;
}

form label{
    display: block;
    margin-top: 30px;
    font-size: 16px;
    font-weight: 500;
}

input{
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

button{
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