<template>
<div class="background">
        <div class="shape"></div>
        <div class="shape"></div>
    </div>
    <form @submit.prevent="submitForm">
        <h2>CREATE ACCOUNT</h2>
        <label for="email">Email</label>
        <input id="email" type="email" placeholder="Email" v-model="email">
        

        
        <label for="password">Password</label>
        <input id="password" type="password" placeholder="Password"  v-model="password">

        <label for="password2">Password</label>
        <input id="password2" type="password" placeholder="Password"  v-model="password2">

        <button type="submit" id="submit">Create Account</button>
        <div class="notification toast align-items-center text-bg-primary border-0" role="alert" aria-live="assertive" aria-atomic="true">
            
            <div class="d-flex" v-if="errors.length">
                <div class="toast-body" v-for="error in errors" v-bind:key="error">
                
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
            </div>
            <div aria-live="polite" aria-atomic="true" class="d-flex justify-content-center align-items-center w-100">
            </div>

        <!-- <div class="notification toast alert-danger" role="alert" aria-live="assertive" aria-atomic="true" v-if="errors.length">
            <div class="toast-header">
                
                <strong class="me-auto">Bootstrap</strong>
                <small>11 mins ago</small>
                <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
                <div class="toast-body" v-for="error in errors" v-bind:key="error">
                    {{error}}
                </div>
            </div>
        -->
            <hr>
        <div class="form">
            Have an account? <router-link to="/Login">Login Here</router-link>
        </div> 
    </form>
</template>
<script>
import axios from 'axios'

export default{
    name: 'SignUp',
    data(){
        return{
            email:'',
            password:'',
            password2:'',
            errors:[]
        }
    },
    methods:{
        submitForm(){
            this.errors=[]
            if (this.email==''){
                this.errors.push('The email is missing')
            }
            if (this.password==''){
                this.errors.push('The password is missing')
            }
            if (this.password   !== this.password2){
                this.errors.push('The password dosen\'t match')
            }
            if (!this.errors.length){
                const formData ={
                    username: this.username,
                    password: this.password
                }
                axios
                    .post('api/auth/',formData)
                    .then(response=>{
                        
                        this.$router.push('/Login')
                    })
                    .catch(error =>{
                        if(error.response){
                            for (const property in error.response.data){
                                this.errors.push(`${property}: ${error.response.data[property]}`)
                            }
                            console.log(JSON.stringify(error.response.data))
                        }else if (error.message){
                            this.errors.push('Something went wrong.Please try again')
                            console.log(JSON.stringify(error))
                        }
                    })
            }
        }
    }
}
</script>
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
    height: 20px;
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
    height: 620px;
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
}</style>