<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const username = ref('')
const password = ref('')
const errorMessage = ref('')
const isLoggingIn = ref(false)

const handleLogin = async () => {
  isLoggingIn.value = true
  errorMessage.value = ''

  try {
    const response = await fetch('https://flava-backend.onrender.com/api/login/',  {
      method: 'POST',
      credentials: 'include', // <-- THIS IS THE CRITICAL FIX
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        username: username.value, 
        password: password.value 
      })
    })

    if (response.ok) {
      const data = await response.json()
      // Optional: Save the username to localStorage so we know who is logged in
      localStorage.setItem('repUsername', data.username)
      
      // Send them directly to their secure dashboard
      router.push('/rep-dashboard')
    } else {
      errorMessage.value = "Invalid username or password. Please try again."
    }
  } catch (error) {
    errorMessage.value = "Could not connect to the Flava server."
  } finally {
    isLoggingIn.value = false
  }
}
</script>

<template>
  <div class="min-h-screen bg-slate-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-md">
      <div class="mx-auto flex items-center justify-center h-16 w-16 rounded-full bg-flava-pink mb-4 shadow-lg">
        <svg class="h-8 w-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path></svg>
      </div>
      <h2 class="text-center text-3xl font-extrabold text-slate-900">
        Rep Portal Login
      </h2>
      <p class="mt-2 text-center text-sm text-slate-600">
        Enter your Flava credentials to access your daily sheet.
      </p>
    </div>

    <div class="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
      <div class="bg-white py-8 px-4 shadow-xl sm:rounded-3xl sm:px-10 border-t-8 border-flava-pink">
        <form class="space-y-6" @submit.prevent="handleLogin">
          <div>
            <label class="block text-sm font-bold text-slate-700">Username</label>
            <div class="mt-1">
              <input v-model="username" type="text" required class="appearance-none block w-full px-4 py-3 border border-slate-300 rounded-xl shadow-sm placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-flava-pink focus:border-flava-pink transition">
            </div>
          </div>

          <div>
            <label class="block text-sm font-bold text-slate-700">Password</label>
            <div class="mt-1">
              <input v-model="password" type="password" required class="appearance-none block w-full px-4 py-3 border border-slate-300 rounded-xl shadow-sm placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-flava-pink focus:border-flava-pink transition">
            </div>
          </div>

          <div v-if="errorMessage" class="text-red-600 text-sm font-bold text-center bg-red-50 py-3 rounded-xl border border-red-100">
            {{ errorMessage }}
          </div>

          <div>
            <button type="submit" :disabled="isLoggingIn" class="w-full flex justify-center py-4 px-4 border border-transparent rounded-xl shadow-md text-lg font-black text-white bg-flava-pink hover:bg-pink-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-flava-pink disabled:opacity-50 transition hover:shadow-xl">
              {{ isLoggingIn ? 'Verifying...' : 'Sign In' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>