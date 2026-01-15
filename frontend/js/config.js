/**
 * VIT-ChainVote Configuration
 * Automatically detects environment and sets API URL
 */

// Detect if running locally or in production
const isLocalhost = window.location.hostname === 'localhost' ||
    window.location.hostname === '127.0.0.1' ||
    window.location.hostname === '';

// Set API URL based on environment
const API_URL = isLocalhost
    ? 'http://localhost:5000/api'  // Local development
    : 'https://voteapp-7eeh.onrender.com/api';  // Production (update after deployment)

// Export for use in other files
window.CONFIG = {
    API_URL: API_URL,
    IS_PRODUCTION: !isLocalhost
};

console.log(`🔧 Environment: ${isLocalhost ? 'Development' : 'Production'}`);
console.log(`🌐 API URL: ${API_URL}`);

