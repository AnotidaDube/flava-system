<script setup>
import { ref, onMounted, computed } from 'vue'

// Product Data with fresh, verified, high-quality images of complete cones
const products = [
  { 
    id: 1, 
    name: 'Classic Chocolate', 
    description: 'A complete, generous scoop of rich, velvety chocolate ice cream in a crisp, sweet waffle cone.', 
    theme: 'bg-amber-800',
    lightTheme: 'bg-amber-50',
    image: '/chocolate.webp' //
  },
  { 
    id: 2, 
    name: 'Creamy Caramel', 
    description: 'Smooth vanilla swirled with thick, buttery caramel ribbons, forming a complete scoop in a crunchy cone.', 
    theme: 'bg-orange-500',
    lightTheme: 'bg-orange-50',
    image: '/caramel.webp' //
  }
]

// State
const activeReps = ref([])
const isOrdering = ref(false)
const selectedProduct = ref(null)
const quantity = ref(1)
const userLocation = ref('')
const orderResult = ref(null) 
const matchedRep = ref(null)

// Pull live rep locations from our Django Radar API
const fetchActiveReps = async () => {
  try {
    const response = await fetch('http://localhost:8000/api/radar/')
    if (response.ok) {
      activeReps.value = await response.json()
    }
  } catch (error) {
    console.error("Could not fetch radar data:", error)
  }
}

onMounted(() => {
  fetchActiveReps()
})

// DYNAMIC PRICING MATH
const unitPrice = computed(() => {
  // Bulk pricing drops to $0.37 at 40+ cones, otherwise it's $0.50
  return quantity.value >= 40 ? 0.37 : 0.50
})

const totalCost = computed(() => {
  return (quantity.value * unitPrice.value).toFixed(2)
})

const openOrderModal = (product) => {
  selectedProduct.value = product
  isOrdering.value = true
  quantity.value = 1
  userLocation.value = ''
  orderResult.value = null
}

const cancelOrder = () => {
  isOrdering.value = false
  // Brief delay before resetting the result view for smooth closing
  setTimeout(() => { orderResult.value = null }, 300)
}

const processOrder = () => {
  // 1. BULK ORDER LOGIC (40+ Cones)
  if (quantity.value >= 40) {
    orderResult.value = 'bulk'
    return
  }

  // 2. RETAIL ORDER LOGIC (< 40 Cones)
  if (!userLocation.value.trim()) {
    alert("Please tell us your location so we can find a rep near you!")
    return
  }

  // Search our active radar for a rep in the user's area (case insensitive)
  const foundRep = activeReps.value.find(rep => 
    rep.area.toLowerCase().includes(userLocation.value.toLowerCase().trim())
  )

  if (foundRep) {
    matchedRep.value = foundRep
    orderResult.value = 'rep_found'
  } else {
    orderResult.value = 'no_rep'
  }
}
</script>

<template>
  <div class="min-h-screen bg-white">
    <div class="bg-flava-pink py-16 px-4 text-center">
      <h1 class="text-4xl md:text-5xl font-black text-white mb-4">Our Flavors</h1>
      <p class="text-pink-100 text-lg max-w-2xl mx-auto font-medium">
        Made fresh daily. Grab a quick treat from a rep near you, or order in bulk for your next big event!
      </p>
    </div>

    <div class="max-w-5xl mx-auto py-16 px-4 sm:px-6 lg:px-8">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-10">
        
        <div v-for="product in products" :key="product.id" :class="[product.lightTheme, 'rounded-3xl p-6 border border-slate-100 shadow-sm hover:shadow-xl transition flex flex-col justify-between relative overflow-hidden']">
          
          <div class="relative z-10">
            <div class="w-full h-72 mb-6 rounded-2xl overflow-hidden shadow-md bg-slate-100 flex items-center justify-center">
              <img :src="product.image" :alt="product.name" class="w-full h-full object-cover hover:scale-105 transition duration-500">
            </div>
            
            <h2 class="text-3xl font-black text-slate-900 mb-3">{{ product.name }}</h2>
            <p class="text-slate-600 font-medium mb-6 text-lg leading-relaxed">{{ product.description }}</p>
            
            <div class="flex items-center gap-4 mb-8">
              <div class="text-2xl font-black text-slate-900">$0.50 <span class="text-sm text-slate-500 font-normal">/ single</span></div>
              <div class="h-8 w-px bg-slate-300"></div>
              <div class="text-lg font-bold text-green-600">$0.37 <span class="text-sm text-green-600/70 font-normal">/ bulk (40+)</span></div>
            </div>
          </div>
          
          <button @click="openOrderModal(product)" :class="[product.theme, 'relative z-10 w-full py-4 rounded-xl text-white font-bold text-lg shadow-md hover:opacity-90 transition transform hover:-translate-y-1']">
            Order {{ product.name }}
          </button>
        </div>

      </div>
    </div>

    <div v-if="isOrdering" class="fixed inset-0 bg-slate-900 bg-opacity-75 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-3xl shadow-2xl max-w-lg w-full overflow-hidden animate-fade-in-up max-h-[90vh] overflow-y-auto">
        
        <div :class="[selectedProduct.theme, 'px-6 py-4 flex justify-between items-center text-white sticky top-0 z-20']">
          <h3 class="font-bold text-xl">Order {{ selectedProduct.name }}</h3>
          <button @click="cancelOrder" class="text-white hover:bg-white hover:bg-opacity-20 rounded-full w-8 h-8 flex items-center justify-center transition">&times;</button>
        </div>

        <div class="p-8">
          <div v-if="!orderResult" class="space-y-6">
            <div>
              <label class="block text-sm font-bold text-slate-700 mb-2">How many cones?</label>
              <input v-model="quantity" type="number" min="1" class="w-full px-4 py-3 text-lg rounded-xl border border-slate-300 focus:ring-2 focus:ring-flava-pink focus:border-flava-pink transition">
              
              <p v-if="quantity >= 40" class="text-green-600 text-sm font-bold mt-2 flex items-center gap-1 animate-fade-in">
                <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"></path></svg>
                Wholesale volume unlocked! Price dropped to $0.37/cone.
              </p>
              <p v-else class="text-slate-500 text-sm font-medium mt-2">
                Price: $0.50/cone. Add {{ 40 - quantity }} more to unlock bulk pricing!
              </p>
            </div>

            <div v-if="quantity < 40" class="animate-fade-in">
              <label class="block text-sm font-bold text-slate-700 mb-2">What is your current area/suburb?</label>
              <input v-model="userLocation" type="text" placeholder="e.g., Mkoba 6" class="w-full px-4 py-3 text-lg rounded-xl border border-slate-300 focus:ring-2 focus:ring-flava-pink focus:border-flava-pink transition">
            </div>

            <div class="bg-slate-50 p-4 rounded-xl border border-slate-100 flex justify-between items-center">
              <span class="font-bold text-slate-500">Estimated Total:</span>
              <span class="text-2xl font-black text-slate-900">${{ totalCost }}</span>
            </div>

            <button @click="processOrder" class="w-full bg-flava-pink text-white font-black text-lg py-4 rounded-xl hover:bg-pink-600 transition shadow-lg">
              {{ quantity >= 40 ? 'Place Wholesale Order' : 'Find My Ice Cream' }}
            </button>
          </div>

          <div v-if="orderResult === 'bulk'" class="text-center space-y-6 animate-fade-in">
            <div class="w-20 h-20 bg-green-100 text-green-600 rounded-full flex items-center justify-center text-4xl mx-auto mb-2">🏭</div>
            <h3 class="text-2xl font-black text-slate-900">Wholesale Order Started</h3>
            <p class="text-slate-600">You are ordering <strong>{{ quantity }} cones</strong> at our bulk rate of $0.37/cone (Total: ${{ totalCost }}).</p>
            
            <div class="bg-slate-50 p-6 rounded-2xl border border-slate-200 text-left space-y-4">
              <div>
                <p class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">Step 1: Call the Manager</p>
                <p class="text-xl font-black text-slate-900">0776 561 335</p>
              </div>
              <div>
                <p class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">Step 2: Collect at Factory</p>
                <p class="text-slate-800 font-medium">Mkoba road via Bristol<br>Next to Delta</p>
              </div>
            </div>
          </div>

          <div v-if="orderResult === 'rep_found'" class="text-center space-y-6 animate-fade-in">
            <div class="w-20 h-20 bg-flava-pink text-white rounded-full flex items-center justify-center text-4xl mx-auto mb-2">🏃</div>
            <h3 class="text-2xl font-black text-slate-900">We found a rep near you!</h3>
            <p class="text-slate-600"><strong>{{ matchedRep.name }}</strong> is currently selling in <strong>{{ matchedRep.area }}</strong>.</p>
            
            <div class="bg-slate-50 p-6 rounded-2xl border border-slate-200 text-left">
               <p class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">Call to get your ice cream:</p>
               <p class="text-2xl font-black text-slate-900 mb-4">{{ matchedRep.phone }}</p>
               
               <a v-if="matchedRep.hasWhatsapp" :href="`https://wa.me/263${matchedRep.phone.substring(1)}`" target="_blank" class="block w-full text-center bg-green-500 text-white font-bold py-3 rounded-xl hover:bg-green-600 transition">
                 Message on WhatsApp
               </a>
            </div>
          </div>

          <div v-if="orderResult === 'no_rep'" class="text-center space-y-6 animate-fade-in">
            <div class="w-20 h-20 bg-slate-100 text-slate-400 rounded-full flex items-center justify-center text-4xl mx-auto mb-2">📍</div>
            <h3 class="text-2xl font-black text-slate-900">No Reps Nearby</h3>
            <p class="text-slate-600">We don't have any reps actively working in <strong>{{ userLocation }}</strong> at this exact moment.</p>
            
            <div class="bg-amber-50 p-6 rounded-2xl border border-amber-200 text-left">
              <p class="font-bold text-amber-900 mb-2">Want to pick it up directly?</p>
              <p class="text-amber-800 text-sm mb-4">You can buy your {{ quantity }} cones directly from our dispatch office!</p>
              <p class="font-black text-slate-900">Mkoba road via Bristol<br>Next to Delta</p>
              <p class="text-sm font-bold text-slate-500 mt-2">Call: 0776 561 335</p>
            </div>
          </div>

        </div>
      </div>
    </div>

  </div>
</template>

<style>
/* Smooth animations for the modal display and transitions */
.animate-fade-in-up { animation: fadeInUp 0.3s ease-out; }
.animate-fade-in { animation: fadeIn 0.3s ease-out; }
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
</style>