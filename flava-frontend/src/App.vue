<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div class="flex flex-col min-h-screen">
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

    <main class="flex-grow">
      <RouterView />
    </main>

    <footer class="bg-slate-900 py-6 text-center text-slate-400 text-sm mt-auto border-t border-slate-800">
      <p>
        System Developed by 
        <a href="http://kaelination.netlify.app/" target="_blank" rel="noopener noreferrer" class="text-flava-pink font-bold hover:text-pink-400 transition hover:underline">
          pyBouyZW (Anotida Dube)
        </a>
      </p>
    </footer>
  </div>
</template>