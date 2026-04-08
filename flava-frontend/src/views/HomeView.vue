<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'

// We start with an empty array. No more hardcoding!
const activeReps = ref([])
const isLoading = ref(true)

const fetchLiveRadar = async () => {
  try {
    const response = await fetch('http://localhost:8000/api/radar/')
    activeReps.value = await response.json()
  } catch (error) {
    console.error("Failed to load radar:", error)
  } finally {
    isLoading.value = false
  }
}

// Fetch the data the moment the page loads
onMounted(() => {
  fetchLiveRadar()
})
</script>

<template>
  <div class="bg-slate-50 min-h-screen font-sans">
    
    <section class="relative h-[80vh] flex items-center justify-center overflow-hidden">
      <div class="absolute inset-0 z-0">
        <img class="w-full h-full object-cover" src="https://images.unsplash.com/photo-1501443762994-82bd5dace89a?auto=format&fit=crop&w=2000&q=80" alt="Flava Hero">
        <div class="absolute inset-0 bg-gradient-to-b from-black/60 to-flava-dark/90"></div>
      </div>
      
      <div class="relative z-10 text-center px-4">
        <span class="text-flava-pink font-bold tracking-widest uppercase text-sm mb-4 block">Handcrafted in Gweru</span>
        <h1 class="text-6xl md:text-8xl font-black text-white mb-6">
          FLAVA FRILLS<span class="text-transparent bg-clip-text bg-gradient-to-r from-flava-pink to-pink-400">NATION</span>
        </h1>
        <p class="text-xl text-gray-200 max-w-2xl mx-auto mb-10 leading-relaxed">
          From our state-of-the-art production floor to your front door. Experience the premium taste that everyone is talking about.
        </p>
        <div class="flex flex-col sm:flex-row justify-center gap-4">
          <RouterLink to="/flavors" class="bg-flava-pink text-white px-10 py-4 rounded-full font-bold text-lg hover:scale-105 transition shadow-2xl">Explore Flavors</RouterLink>
          <RouterLink to="/join-the-team" class="bg-white/10 backdrop-blur-md border-2 border-white/30 text-white px-10 py-4 rounded-full font-bold text-lg hover:bg-white/20 transition">Join the Team</RouterLink>
        </div>
      </div>
    </section>

    <section class="max-w-7xl mx-auto px-4 -mt-20 relative z-20 mb-24">
      <div class="bg-white rounded-[2.5rem] shadow-2xl p-8 md:p-12 border-b-8 border-flava-pink">
        <div class="flex flex-col md:flex-row justify-between items-end mb-12 gap-6">
          <div>
            <h2 class="text-4xl font-black text-slate-900 mb-2">Flava Frills Radar 📍</h2>
            <p class="text-slate-500 text-lg">Our uniformed reps are currently active in these areas.</p>
          </div>
          <div class="bg-green-50 px-6 py-3 rounded-2xl flex items-center gap-3">
            <span class="flex h-3 w-3 relative">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
              <span class="relative inline-flex rounded-full h-3 w-3 bg-green-500"></span>
            </span>
            <span class="text-green-700 font-bold uppercase tracking-wider text-sm">Live System Active</span>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div v-for="rep in activeReps" :key="rep.id" class="group bg-slate-50 rounded-3xl p-8 border border-slate-100 hover:border-flava-pink hover:bg-white transition-all duration-300 shadow-sm hover:shadow-xl">
            <div class="flex items-center gap-4 mb-6">
              <img :src="rep.avatar" class="w-16 h-16 rounded-2xl object-cover ring-4 ring-white shadow-md" />
              <div>
                <h3 class="text-xl font-bold text-slate-900">{{ rep.name }}</h3>
                <p class="text-flava-pink font-bold text-sm">{{ rep.cartNumber }}</p>
              </div>
            </div>
            
            <div class="bg-white rounded-2xl p-4 mb-8 shadow-inner">
              <p class="text-xs text-slate-400 uppercase font-black tracking-widest mb-1">Current Sector</p>
              <p class="text-xl font-bold text-slate-800">{{ rep.area }}</p>
            </div>

            <div class="space-y-3">
              <a v-if="rep.hasWhatsapp" :href="`https://wa.me/${rep.phone.replace('+', '')}`" class="w-full py-4 bg-[#25D366] text-white rounded-2xl font-black text-center block hover:opacity-90 shadow-lg">WHATSAPP ME</a>
              <a v-else :href="`sms:${rep.phone}`" class="w-full py-4 bg-sky-500 text-white rounded-2xl font-black text-center block hover:opacity-90 shadow-lg">SEND SMS</a>
              <a :href="`tel:${rep.phone}`" class="w-full py-4 border-2 border-slate-200 text-slate-600 rounded-2xl font-black text-center block hover:bg-slate-100 transition">CALL DIRECT</a>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="max-w-7xl mx-auto px-4 space-y-32">
      
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
        <div class="order-2 lg:order-1">
          <span class="text-flava-pink font-black uppercase tracking-widest text-sm italic">The Kitchen</span>
          <h2 class="text-5xl font-black text-slate-900 mt-4 mb-6 leading-tight">Handcrafted Excellence in Every Batch.</h2>
          <p class="text-slate-500 text-lg leading-relaxed mb-8">
            Our production team follows strict international health protocols. We don't just make ice cream; we engineer moments of joy using the finest ingredients and a high-tech cooling chain.
          </p>
          <div class="flex items-center gap-4 p-4 bg-white rounded-2xl shadow-sm border border-slate-100">
            <div class="h-12 w-12 bg-pink-100 rounded-xl flex items-center justify-center text-flava-pink">
              <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20"><path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z"></path><path fill-rule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h.01a1 1 0 100-2H10zm3 0a1 1 0 000 2h.01a1 1 0 100-2H13zm-6 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h.01a1 1 0 100-2H10zm3 0a1 1 0 000 2h.01a1 1 0 100-2H13z" clip-rule="evenodd"></path></svg>
            </div>
            <p class="font-bold text-slate-700 italic">"Cleanliness is our culture." — Production Lead</p>
          </div>
        </div>
        <div class="order-1 lg:order-2 grid grid-cols-2 gap-4">
          <img class="rounded-3xl shadow-xl hover:scale-105 transition duration-500" src="https://images.unsplash.com/photo-1563805042-7684c019e1cb?auto=format&fit=crop&w=600&q=80" alt="Production Team">
          <img class="rounded-3xl shadow-xl mt-12 hover:scale-105 transition duration-500" src="https://images.unsplash.com/photo-1553177595-4de2bb0842b9?auto=format&fit=crop&w=600&q=80" alt="Stocked Ice Cream">
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
        <div class="grid grid-cols-2 gap-4">
          <img class="rounded-3xl shadow-xl hover:scale-105 transition duration-500" src="https://images.unsplash.com/photo-1560008511-11c63416e52d?auto=format&fit=crop&w=600&q=80" alt="Loaded Carts">
          <img class="rounded-3xl shadow-xl mt-12 hover:scale-105 transition duration-500" src="https://images.unsplash.com/photo-1580915411954-282cb1b0d780?auto=format&fit=crop&w=600&q=80" alt="Uniformed Reps">
        </div>
        <div>
          <span class="text-flava-pink font-black uppercase tracking-widest text-sm italic">The Dispatch</span>
          <h2 class="text-5xl font-black text-slate-900 mt-4 mb-6 leading-tight">Ready for the Streets.</h2>
          <p class="text-slate-500 text-lg leading-relaxed mb-8">
            Every morning, our reps suit up in their crisp Flava Frills uniforms. Carts are inspected, stocked with freshly frozen units and sub-zero ice packs, ensuring that the last scoop is as cold as the first.
          </p>
          <div class="grid grid-cols-2 gap-6">
            <div class="p-6 bg-white rounded-2xl border border-slate-100 shadow-sm">
              <p class="text-3xl font-black text-flava-pink">50+</p>
              <p class="text-slate-500 font-bold text-sm uppercase">Active Carts</p>
            </div>
            <div class="p-6 bg-white rounded-2xl border border-slate-100 shadow-sm">
              <p class="text-3xl font-black text-flava-pink">100%</p>
              <p class="text-slate-500 font-bold text-sm uppercase">Cold Chain Verified</p>
            </div>
          </div>
        </div>
      </div>

    </section>

    <footer class="mt-32 py-20 bg-flava-dark text-white text-center">
      <h2 class="text-4xl font-black mb-8 italic italic">Want the Flava Frills Ice Creams at your event?</h2>
      <button class="bg-flava-pink px-12 py-5 rounded-full font-black text-xl hover:shadow-[0_0_30px_rgba(255,71,126,0.4)] transition">Book a Cart Now</button>
    </footer>

  </div>
</template>

<style scoped>
/* No extra CSS needed! Tailwind handles it all. */
</style>