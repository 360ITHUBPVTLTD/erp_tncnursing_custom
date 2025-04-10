// src/services/scoreCardService.js

import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_FRAPPE_API_URL || '/api';

// Create axios instance with common configuration
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  },
  withCredentials: true // Important for cookie-based authentication with Frappe
});

export const scoreCardService = {
  /**
   * Get PDF download URL for student score card
   * @param {string} mobileNumber - Student's 10-digit mobile number
   * @returns {Promise<string>} - Promise resolving to PDF URL
   */
  async getScoreCardPdfUrl(mobileNumber) {
    try {
      const response = await apiClient.get('/method/tnc_frappe_custom_app.result_sharing.download_result_by_mobile_no', {
        params: { mobile_no: mobileNumber }
      });
      
      // Check for valid response format
      if (response.data && response.data.message && response.data.message.pdf_url) {
        return response.data.message.pdf_url;
      } else if (response.data && response.data.message) {
        // Sometimes Frappe returns the result directly in message
        if (typeof response.data.message === 'string' && response.data.message.includes('http')) {
          return response.data.message;
        }
        // Or it might return an object with a different structure
        if (typeof response.data.message === 'object') {
          // Try to find a URL-like property
          for (const key in response.data.message) {
            if (typeof response.data.message[key] === 'string' && 
                response.data.message[key].includes('http')) {
              return response.data.message[key];
            }
          }
        }
        throw new Error('Could not find PDF URL in server response');
      } else {
        throw new Error('Invalid response format from server');
      }
    } catch (error) {
      // Enhanced error handling using backend message
      if (error.response) {
        // Extract message from response if available
        const backendMessage = error.response.data?.message?.message || 
                             error.response.data?.message || 
                             'An error occurred';
        throw new Error(backendMessage);
      } else if (error.request) {
        // Request made but no response received
        throw new Error('No response received from server. Please check your connection.');
      } else {
        // Error in setting up the request
        throw new Error(`Request setup error: ${error.message}`);
      }
    }
  },
  
  /**
   * Download the PDF directly
   * @param {string} mobileNumber - Student's 10-digit mobile number
   * @returns {Promise<Blob>} - Promise resolving to PDF Blob
   */
  async downloadScoreCardPdf(mobileNumber) {
    try {
      const response = await apiClient.get('/method/tnc_frappe_custom_app.result_sharing.download_result_by_mobile_no', {
        params: { mobile_number: mobileNumber },
        responseType: 'blob'
      });
      
      return response.data;
    } catch (error) {
      // Enhanced error handling using backend message
      if (error.response) {
        // Extract message from response if available
        const backendMessage = error.response.data?.message?.message || 
                             error.response.data?.message || 
                             'An error occurred';
        throw new Error(backendMessage);
      } else if (error.request) {
        throw new Error('No response received from server. Please check your connection.');
      } else {
        throw new Error(`Request setup error: ${error.message}`);
      }
    }
  }
};

export default scoreCardService;