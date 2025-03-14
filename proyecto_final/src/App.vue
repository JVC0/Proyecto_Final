<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary">
  <div class="container-fluid">
    <router-link to="/" class="navbar-brand active"><strong>Home</strong></router-link>
    
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav">
        <li class="nav-item">
          <router-link to="/Login" class="nav-link">Log in</router-link>
        </li>
        <li class="nav-item">
          <router-link to="/Signup" class="nav-link">Sign up</router-link>
        </li>
        <li class="nav-item">
          <router-link to="/" class="nav-link">Log in</router-link>
        </li>
        
      </ul>
    </div>
  </div>
</nav>
  <router-view/>
</template>
<script>


</script>
<style>
@import '../node_modules/bootstrap/';


</style>
