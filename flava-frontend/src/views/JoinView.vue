<script setup>
import { ref } from 'vue'

const formData = ref({
  fullName: '',
  idNumber: '',
  phone: '',
  email: '', // Added email field
  age: '',
  maritalStatus: 'Single',
  agreedToTerms: false
})

const isSubmitting = ref(false)
const isSuccess = ref(false)
const errorMessage = ref('')

const submitApplication = async () => {
  if (!formData.value.agreedToTerms) {
    errorMessage.value = "You must agree to the Terms and Conditions to apply."
    return
  }

  isSubmitting.value = true
  errorMessage.value = ''

  try {
    const response = await fetch('http://localhost:8000/api/apply/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData.value)
    })

    if (response.ok) {
      isSuccess.value = true
    } else {
      errorMessage.value = "Something went wrong. Please try again."
    }
  } catch (error) {
    errorMessage.value = "Could not connect to the server."
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <div class="min-h-screen bg-slate-50 py-16 px-4 sm:px-6 lg:px-8">
    <div class="max-w-3xl mx-auto">
      
      <div class="text-center mb-12">
        <h1 class="text-4xl font-extrabold text-slate-900 tracking-tight">Join Flava Frills Nation</h1>
        <p class="mt-4 text-lg text-slate-500">Be your own boss. Make cash daily. Spread the joy.</p>
      </div>

      <div v-if="isSuccess" class="bg-white rounded-3xl shadow-xl p-10 text-center border-t-8 border-green-500">
        <div class="mx-auto flex items-center justify-center h-16 w-16 rounded-full bg-green-100 mb-6">
          <svg class="h-8 w-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
        </div>
        <h2 class="text-3xl font-bold text-slate-900 mb-4">Application Received!</h2>
        <p class="text-lg text-slate-600 mb-6">Thank you for applying. Please read your next steps carefully below.</p>
        
        <div class="bg-slate-50 p-6 rounded-2xl border border-slate-200 inline-block text-left w-full">
          <p class="font-bold text-slate-800 uppercase text-sm mb-2 text-center">Next Step: Mandatory Verification</p>
          <p class="text-slate-600 text-center mb-4">You must come in person to complete your registration.</p>
          
          <div class="bg-white border border-slate-200 p-6 rounded-xl text-center shadow-sm">
            <p class="text-slate-500 text-sm uppercase tracking-wide font-bold mb-1">Office Location</p>
            <p class="font-black text-flava-pink text-2xl">Mkoba road via Bristol next to Delta</p>
            <p class="font-bold text-slate-700 text-lg mt-1">Gweru</p>
            <p class="text-red-600 text-sm mt-4 border-t border-slate-100 pt-4"><strong>CRITICAL:</strong> You must bring a physical copy of your National ID!</p>
          </div>
        </div>
      </div>

      <div v-else class="bg-white rounded-3xl shadow-2xl overflow-hidden">
        <div class="bg-flava-dark px-8 py-6">
          <h2 class="text-2xl font-bold text-white">Official Rep Application</h2>
        </div>
        
        <form @submit.prevent="submitApplication" class="p-8 space-y-8">
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label class="block text-sm font-bold text-slate-700 mb-2">Full Name</label>
              <input v-model="formData.fullName" type="text" required class="w-full px-4 py-3 rounded-xl border border-slate-300 focus:ring-2 focus:ring-flava-pink focus:border-flava-pink transition">
            </div>
            <div>
              <label class="block text-sm font-bold text-slate-700 mb-2">National ID Number</label>
              <input v-model="formData.idNumber" type="text" required class="w-full px-4 py-3 rounded-xl border border-slate-300 focus:ring-2 focus:ring-flava-pink focus:border-flava-pink transition">
            </div>
            <div>
              <label class="block text-sm font-bold text-slate-700 mb-2">Phone Number</label>
              <input v-model="formData.phone" type="tel" required class="w-full px-4 py-3 rounded-xl border border-slate-300 focus:ring-2 focus:ring-flava-pink focus:border-flava-pink transition">
            </div>
            <div>
              <label class="block text-sm font-bold text-slate-700 mb-2">Email <span class="text-slate-400 font-normal">(Optional)</span></label>
              <input v-model="formData.email" type="email" class="w-full px-4 py-3 rounded-xl border border-slate-300 focus:ring-2 focus:ring-flava-pink focus:border-flava-pink transition placeholder-slate-400" placeholder="If you have one">
            </div>
            <div>
              <label class="block text-sm font-bold text-slate-700 mb-2">Age</label>
              <input v-model="formData.age" type="number" required class="w-full px-4 py-3 rounded-xl border border-slate-300 focus:ring-2 focus:ring-flava-pink focus:border-flava-pink transition">
            </div>
            <div>
              <label class="block text-sm font-bold text-slate-700 mb-2">Marital Status</label>
              <select v-model="formData.maritalStatus" class="w-full px-4 py-3 rounded-xl border border-slate-300 focus:ring-2 focus:ring-flava-pink focus:border-flava-pink transition">
                <option value="Single">Single</option>
                <option value="Married">Married</option>
                <option value="Other">Other</option>
              </select>
            </div>
          </div>

          <div class="bg-red-50 border border-red-100 rounded-2xl p-6">
            <h3 class="font-bold text-red-800 mb-3 uppercase tracking-wide text-sm">Flava Rep Terms & Conditions</h3>
            <ul class="list-disc pl-5 text-sm text-red-700 space-y-2 mb-6">
              <li><strong>Security Deposit:</strong> A mandatory $1.00 deduction applies to daily commissions until a $100.00 security threshold is met.</li>
              <li><strong>Attendance:</strong> Representatives must report to the dispatch office daily, excluding approved off days.</li>
              <li><strong>Liability:</strong> Representatives assume full financial responsibility for all inventory and equipment (carts, ice packs, ice creams) from dispatch to settlement. Damaged or melted stock must be paid for in full.</li>
            </ul>
            
            <label class="flex items-start gap-3 cursor-pointer">
              <input v-model="formData.agreedToTerms" type="checkbox" class="mt-1 h-5 w-5 rounded border-red-300 text-flava-pink focus:ring-flava-pink cursor-pointer">
              <span class="text-sm font-bold text-red-900">I have read and agree to accept full financial liability under the Flava Terms & Conditions.</span>
            </label>
          </div>

          <div v-if="errorMessage" class="text-red-600 font-bold text-center">
            {{ errorMessage }}
          </div>

          <button type="submit" :disabled="isSubmitting" class="w-full py-4 px-6 rounded-xl text-white font-black text-lg bg-flava-pink hover:bg-pink-600 hover:shadow-lg transition disabled:opacity-50">
            {{ isSubmitting ? 'Submitting Application...' : 'Submit Application' }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>