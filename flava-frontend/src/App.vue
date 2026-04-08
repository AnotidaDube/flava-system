<script setup>
import { ref } from 'vue'
import { RouterLink, RouterView } from 'vue-router'

// State to track if the mobile menu is open or closed
const isMobileMenuOpen = ref(false)

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}

// Close the menu automatically when a link is clicked
const closeMobileMenu = () => {
  isMobileMenuOpen.value = false
}
</script>

<template>
  <div class="flex flex-col min-h-screen">
    <header>
      <nav class="bg-flava-pink text-white shadow-md relative z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="flex justify-between h-16 items-center">
            <div class="text-2xl font-extrabold tracking-tight">
              Flava Ice Creams
            </div>
            
            <div class="hidden md:flex space-x-8 items-center">
              <RouterLink to="/" class="hover:text-flava-dark font-medium transition">Home</RouterLink>
              <RouterLink to="/flavors" class="hover:text-flava-dark font-medium transition">Menu</RouterLink>
              <RouterLink to="/join-the-team" class="hover:text-flava-dark font-medium transition">Become a Rep</RouterLink>
              <RouterLink to="/login" class="bg-white text-flava-pink px-4 py-1 rounded-full font-bold hover:bg-gray-100 transition shadow-sm">Rep Login</RouterLink>
            </div>

            <div class="md:hidden flex items-center">
              <button @click="toggleMobileMenu" class="text-white hover:text-pink-200 focus:outline-none p-2">
                <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path v-if="!isMobileMenuOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
                  <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
              </button>
            </div>
          </div>
        </div>

        <div v-if="isMobileMenuOpen" class="md:hidden bg-flava-pink border-t border-pink-400 absolute w-full left-0 shadow-2xl pb-4">
          <div class="px-4 pt-2 pb-3 space-y-1 flex flex-col">
            <RouterLink @click="closeMobileMenu" to="/" class="block px-3 py-3 rounded-md font-bold hover:bg-pink-600 transition">Home</RouterLink>
            <RouterLink @click="closeMobileMenu" to="/flavors" class="block px-3 py-3 rounded-md font-bold hover:bg-pink-600 transition">Menu</RouterLink>
            <RouterLink @click="closeMobileMenu" to="/join-the-team" class="block px-3 py-3 rounded-md font-bold hover:bg-pink-600 transition">Become a Rep</RouterLink>
            <div class="pt-4 pb-2">
              <RouterLink @click="closeMobileMenu" to="/login" class="block w-full text-center bg-white text-flava-pink px-4 py-3 rounded-full font-black shadow-md hover:bg-gray-100 transition">Rep Login</RouterLink>
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