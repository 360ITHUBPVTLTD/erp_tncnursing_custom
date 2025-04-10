
<template>
  <div class="min-h-screen bg-gradient-to-b from-blue-50 to-white flex items-center justify-center p-4">
    <div class="bg-white rounded-xl shadow-lg w-full max-w-lg p-8 border border-gray-100">
      <!-- Loading Overlay -->
      <div v-if="loading" class="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center z-10 backdrop-blur-sm transition-all duration-300">
        <div class="bg-white p-8 rounded-xl shadow-2xl text-center max-w-sm mx-4 transform transition-all duration-300 scale-100">
          <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mb-6"></div>
          <p class="text-lg font-medium text-gray-700">Loading your score card...</p>
          <p class="text-sm text-gray-500 mt-2">This may take a few moments</p>
        </div>
      </div>
      
      <!-- Header with Logo -->
      <div class="flex flex-col items-center mb-8">
        <div class="text-blue-600 mb-4 transform hover:scale-105 transition-transform duration-300">
          <img src="../assets/TNC 1.png" alt="TNC Logo" class="h-20 w-20">
        </div>
        <h1 class="text-3xl font-bold text-center text-blue-700 mb-2">Student Score Card</h1>
        <div class="w-16 h-1 bg-blue-600 rounded-full mb-4"></div>
        <p class="text-center text-gray-600 max-w-md">
          Enter your mobile number to view your performance in NORCET 8.0
        </p>
      </div>
      
      <!-- Error Alert -->
      <div v-if="error" 
           class="bg-red-50 border-l-4 border-red-500 text-red-700 p-4 rounded-md mb-6 animate-fadeIn"
           role="alert">
        <div class="flex items-start">
          <div class="flex-shrink-0">
            <svg class="h-5 w-5 text-red-500" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
            </svg>
          </div>
          <div class="ml-3">
            <p class="text-sm font-medium">{{ error }}</p>
          </div>
          <button @click="error = ''" class="ml-auto text-red-500 hover:text-red-700">
            <svg class="h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
            </svg>
          </button>
        </div>
      </div>
      
      <!-- Mobile Number Input -->
      <div class="mb-8">
        <label for="mobileNumber" class="block text-gray-700 font-medium mb-2">Mobile Number</label>
        <div class="relative">
          <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
              <path d="M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.548.773a11.037 11.037 0 006.105 6.105l.774-1.548a1 1 0 011.059-.54l4.435.74a1 1 0 01.836.986V17a1 1 0 01-1 1h-2C7.82 18 2 12.18 2 5V3z" />
            </svg>
          </div>
          <input 
            type="text" 
            id="mobileNumber" 
            v-model="mobileNumber" 
            placeholder="Enter your 10-digit mobile number" 
            autocomplete="off"
            class="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200"
            :class="{ 'border-red-500 ring-1 ring-red-500': validationError }"
            @input="validateMobileNumber"
            maxlength="10"
          >
        </div>
        <p v-if="validationError" class="mt-2 text-sm text-red-600 flex items-center animate-fadeIn">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
          </svg>
          {{ validationError }}
        </p>
        <p v-else class="mt-2 text-xs text-gray-500">
          We'll use this to retrieve your score card
        </p>
      </div>
      
      <!-- Download Button -->
      <button 
        @click="downloadPdf" 
        type="button"
        class="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-3.5 px-4 rounded-lg transition duration-300 flex justify-center items-center shadow-md hover:shadow-lg transform hover:-translate-y-0.5"
        :disabled="loading || !!validationError || !mobileNumber"
        :class="{ 'opacity-60 cursor-not-allowed': loading || !!validationError || !mobileNumber }"
      >
        <svg v-if="!loading" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clip-rule="evenodd" />
        </svg>
        <span v-if="!loading" class="font-semibold">Download Score Card</span>
        <span v-else class="inline-block h-5 w-5 rounded-full border-2 border-white border-t-transparent animate-spin mr-2"></span>
      </button>
      
      <!-- Help Text -->
      <!-- <div class="mt-6 text-center">
        <p class="text-sm text-gray-500">
          Having trouble? Contact support at 
          <a href="mailto:support@tnc.com" class="text-blue-600 hover:underline">support@tnc.com</a>
        </p>
      </div> -->
    </div>
    
    <!-- Footer -->
    <div class="absolute bottom-4 text-center w-full">
      <p class="text-gray-500 text-sm">
        © 2025 TNC | Developed by 
        <a href="https://360ithub.com" target="_blank" class="text-blue-600 hover:underline font-medium">360ITHUB</a>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { scoreCardService } from '@/services/scoreCardService';

const mobileNumber = ref('');
const loading = ref(false);
const error = ref('');
const validationError = ref('');

// Input validation
const validateMobileNumber = () => {
  validationError.value = '';
  
  if (!mobileNumber.value) {
    validationError.value = 'Mobile number is required';
    return false;
  }
  
  // Check if input contains only digits
  if (!/^\d*$/.test(mobileNumber.value)) {
    validationError.value = 'Please enter numbers only';
    // Remove non-digit characters
    mobileNumber.value = mobileNumber.value.replace(/\D/g, '');
    return false;
  }
  
  // Check length
  if (mobileNumber.value.length !== 10) {
    validationError.value = 'Mobile number must be 10 digits';
    return false;
  }
  
  return true;
};

const downloadPdf = async () => {
  // Clear previous errors
  error.value = '';
  
  // Validate input again before proceeding
  if (!validateMobileNumber()) {
    return;
  }
  
  try {
    loading.value = true;
    console.log('Downloading PDF for mobile number:', mobileNumber.value);
    
    // Method 1: Get URL and open in new tab
    const pdfUrl = await scoreCardService.getScoreCardPdfUrl(mobileNumber.value);
    console.log('PDF URL received:', pdfUrl);
    
    // Ensure we have a URL before opening
    if (pdfUrl) {
      window.open(pdfUrl, '_blank');
    } else {
      throw new Error('No PDF URL returned from server');
    }
  } catch (err) {
    console.error('PDF download error:', err);
    error.value = err.message || 'Failed to download score card. Please try again.';
  } finally {
    loading.value = false;
  }
};

// Debugging helper
onMounted(() => {
  console.log('Student Score Card component mounted');
});
</script>

<style scoped>
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}

.animate-fadeIn {
  animation: fadeIn 0.3s ease-out forwards;
}
</style>
