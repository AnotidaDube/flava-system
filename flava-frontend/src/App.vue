<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>
    <nav class="bg-flava-pink text-white shadow-md">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16 items-center">
          <div class="text-2xl font-extrabold tracking-tight">
            Flava Ice Creams
          </div>
          <div class="hidden md:flex space-x-8">
            <RouterLink to="/" class="hover:text-flava-dark font-medium transition">Home</RouterLink>
            <RouterLink to="/flavors" class="hover:text-flava-dark font-medium transition">Menu</RouterLink>
            <RouterLink to="/join-the-team" class="hover:text-flava-dark font-medium transition">Become a Rep</RouterLink>
            <RouterLink to="/login" class="bg-white text-flava-pink px-4 py-1 rounded-full font-bold hover:bg-gray-100 transition">Rep Login</RouterLink>
          </div>
        </div>
      </div>
    </nav>
  </header>

  <main>
    <RouterView />
  </main>
</template>