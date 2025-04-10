<!-- <template>
  <div class="max-w-3xl py-12 mx-auto">
    <h2 class="font-bold text-lg text-gray-600 mb-4">
      Welcome {{ session.user }}!
    </h2>

    <Button theme="gray" variant="solid" icon-left="code" @click="ping.fetch" :loading="ping.loading">
      Click to send 'ping' request
    </Button>
    <div>
      {{ ping.data }}
    </div>
    <pre>{{ ping }}</pre>

    <div class="flex flex-row space-x-2 mt-4">
      <Button @click="showDialog = true">Open Dialog</Button>
      <Button @click="session.logout.submit()">Logout</Button>
    </div> -->

    <!-- Dialog -->
    <!-- <Dialog title="Title" v-model="showDialog"> Dialog content </Dialog>
  </div>
</template> -->

<!-- <script setup>
import { ref } from 'vue'
import { Dialog } from 'frappe-ui'
import { createResource } from 'frappe-ui'
import { session } from '../data/session'

const ping = createResource({
  url: 'ping',
  auto: true,
})

const showDialog = ref(false)
</script> -->



<template>
  <div class="min-h-screen bg-blue-50 flex items-center justify-center p-4">
    <div class="bg-white rounded-lg shadow-md w-full max-w-lg p-8">
      <!-- Loading Overlay -->
      <div v-if="loading" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-10">
        <div class="bg-white p-6 rounded-lg shadow-xl text-center">
          <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mb-4"></div>
          <p>Loading your score card...</p>
        </div>
      </div>
      
      <div class="flex justify-center mb-6">
        <div class="text-blue-600">
          <img src="../assets/TNC 1.png" alt="Logo" class="h-16 w-16">
        </div>
      </div>
      
      <h1 class="text-3xl font-bold text-center text-blue-600 mb-4">Student Score Card</h1>
      
      <p class="text-center text-gray-700 mb-6">
        Enter your mobile number to view your performance in NORCET 8.0
      </p>
      
      <!-- Error Alert -->
      <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
        <strong class="font-bold">Error! </strong>
        <span class="block sm:inline"> {{ error }}</span>
      </div>
      
      <div class="mb-6">
        <label for="mobileNumber" class="block text-gray-700 font-medium mb-2">Mobile Number</label>
        <input 
          type="text" 
          id="mobileNumber" 
          v-model="mobileNumber" 
          placeholder="Enter your 10-digit mobile number" 
          class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          :class="{ 'border-red-500': validationError }"
          @input="validateMobileNumber"
          maxlength="10"
        >
        <p v-if="validationError" class="mt-1 text-sm text-red-600">{{ validationError }}</p>
      </div>
      
      <button 
        @click="downloadPdf" 
        type="button"
        class="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 px-4 rounded-md transition duration-300 flex justify-center items-center"
        :disabled="loading || !!validationError || !mobileNumber"
        :class="{ 'opacity-50 cursor-not-allowed': loading || !!validationError || !mobileNumber }"
      >
        <span v-if="!loading">Download PDF</span>
        <span v-else class="inline-block h-4 w-4 rounded-full border-2 border-white border-t-transparent animate-spin mr-2"></span>
      </button>
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
// /method/tnc_frappe_custom_app.result_sharing.download_result_by_mobile_no
</script>