<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const isLoading = ref(true)
const fetchError = ref(false)

// Dashboard State
const profile = ref({
  name: '',
  securityDeposit: 0.00,
  status: 'No Active Shift',
  unitsTaken: 0,
  rate: 0.37
})

// Settlement Calculator State
const returnCount = ref(0)
const cashIn = ref(0)

// Dynamic Math
const expectedCash = computed(() => {
  const sold = profile.value.unitsTaken - (returnCount.value || 0)
  return sold > 0 ? (sold * profile.value.rate).toFixed(2) : '0.00'
})

const discrepancy = computed(() => {
  return ((cashIn.value || 0) - expectedCash.value).toFixed(2)
})

const fetchDashboardData = async () => {
  try {
    const response = await fetch('http://localhost:8000/api/my-dashboard/', {
      credentials: 'include' // CRITICAL: This sends the secure login cookie to Django
    })

    if (response.status === 401) {
      // Not logged in? Kick them to the login screen immediately
      router.push('/login')
      return
    }

    if (!response.ok) throw new Error("Server error")

    const data = await response.json()
    profile.value.name = data.name
    profile.value.securityDeposit = data.securityDepositBalance
    profile.value.status = data.today.status
    profile.value.unitsTaken = data.today.unitsTaken
    profile.value.rate = data.today.wholesaleRate

  } catch (error) {
    console.error("Dashboard Error:", error)
    fetchError.value = true
  } finally {
    isLoading.value = false
  }
}

const handleLogout = () => {
  router.push('/login')
}

onMounted(() => {
  fetchDashboardData()
})
</script>

<template>
  <div class="min-h-screen bg-slate-50 py-10 px-4 sm:px-6 lg:px-8">
    <div class="max-w-4xl mx-auto space-y-6">
      
      <div v-if="isLoading" class="text-center py-20 text-slate-500 font-bold animate-pulse">
        Securely loading your profile...
      </div>
      <div v-else-if="fetchError" class="bg-red-50 text-red-600 p-6 rounded-2xl text-center font-bold border border-red-100">
        Connection lost. Please refresh the page.
      </div>

      <div v-else class="space-y-6">
        <div class="bg-white rounded-3xl shadow-sm border border-slate-200 overflow-hidden flex flex-col md:flex-row justify-between items-center p-8">
          <div>
            <h1 class="text-3xl font-black text-slate-900 capitalize">Welcome back, {{ profile.name }}</h1>
            <div class="flex items-center gap-3 mt-2">
              <span class="text-sm font-bold text-slate-500 uppercase tracking-wider">Shift Status:</span>
              <span v-if="profile.status === 'Active'" class="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm font-bold flex items-center gap-2">
                <span class="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span> Active in Field
              </span>
              <span v-else class="px-3 py-1 bg-slate-100 text-slate-600 rounded-full text-sm font-bold">
                {{ profile.status }}
              </span>
            </div>
          </div>
          
          <div class="mt-6 md:mt-0 text-right bg-slate-50 p-4 rounded-2xl border border-slate-100">
            <p class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">Security Deposit</p>
            <p class="text-4xl font-black text-green-500">${{ profile.securityDeposit.toFixed(2) }}</p>
            <p class="text-xs text-slate-500 mt-1 font-medium">Auto-capped at $100.00</p>
          </div>
        </div>

        <div class="bg-white rounded-3xl shadow-xl overflow-hidden border border-slate-200">
          <div class="bg-slate-900 px-8 py-5 flex justify-between items-center">
            <h2 class="text-xl font-bold text-white">End of Day Settlement Preview</h2>
            <button @click="handleLogout" class="text-sm text-slate-400 hover:text-white transition">Sign Out</button>
          </div>

          <div class="p-8 grid grid-cols-1 md:grid-cols-2 gap-10">
            <div class="space-y-6">
              <h3 class="text-sm font-bold text-slate-400 uppercase tracking-wider border-b border-slate-100 pb-2">Morning Dispatch</h3>
              
              <div class="flex justify-between items-center bg-slate-50 p-4 rounded-xl border border-slate-100">
                <span class="font-medium text-slate-600">Total Units Taken:</span>
                <span class="text-2xl font-black text-slate-900">{{ profile.unitsTaken }}</span>
              </div>
              
              <div class="flex justify-between items-center bg-slate-50 p-4 rounded-xl border border-slate-100">
                <span class="font-medium text-slate-600">Company Rate:</span>
                <span class="text-xl font-black text-slate-900">${{ profile.rate }} <span class="text-sm font-normal text-slate-500">/ unit</span></span>
              </div>
            </div>

            <div class="space-y-6">
              <h3 class="text-sm font-bold text-slate-400 uppercase tracking-wider border-b border-slate-100 pb-2">Evening Return Form</h3>
              
              <div>
                <label class="block text-sm font-bold text-slate-700 mb-2">Unsold Ice Creams Returned</label>
                <input v-model="returnCount" type="number" min="0" :disabled="profile.status !== 'Active'" class="w-full px-4 py-3 text-lg rounded-xl border border-slate-300 focus:ring-2 focus:ring-flava-pink focus:border-flava-pink transition disabled:bg-slate-100">
              </div>

              <div>
                <label class="block text-sm font-bold text-slate-700 mb-2">Total Cash Handed In</label>
                <div class="relative">
                  <span class="absolute inset-y-0 left-0 pl-4 flex items-center text-slate-500 font-bold">$</span>
                  <input v-model="cashIn" type="number" step="0.01" min="0" :disabled="profile.status !== 'Active'" class="w-full pl-8 pr-4 py-3 text-lg rounded-xl border border-slate-300 focus:ring-2 focus:ring-flava-pink focus:border-flava-pink transition disabled:bg-slate-100">
                </div>
              </div>
            </div>
          </div>

          <div class="bg-slate-50 p-8 border-t border-slate-200 grid grid-cols-1 md:grid-cols-2 gap-6 items-center">
            <div>
              <p class="text-sm font-medium text-slate-500">Expected Company Revenue</p>
              <p class="text-3xl font-black text-slate-900">${{ expectedCash }}</p>
              <p class="text-xs text-slate-400 mt-1">({{ profile.unitsTaken - returnCount }} sold × ${{ profile.rate }})</p>
            </div>
            
            <div class="text-right p-4 rounded-xl" :class="discrepancy < 0 ? 'bg-red-100 text-red-700 border border-red-200' : 'bg-green-100 text-green-700 border border-green-200'">
              <p class="text-sm font-bold uppercase tracking-wider">Cash Discrepancy</p>
              <p class="text-3xl font-black mb-1">${{ discrepancy }}</p>
              <p v-if="discrepancy < 0" class="text-xs font-bold">Shortfall! You owe the company.</p>
              <p v-else-if="discrepancy > 0" class="text-xs font-bold">Over, but expected matches.</p>
              <p v-else class="text-xs font-bold">Perfectly balanced.</p>
            </div>
          </div>
          
        </div>
      </div>
      
    </div>
  </div>
</template>