// FrontEnd/js/api.js
const API_BASE_URL = "http://127.0.0.1:3000/api";

// Helper to get the token from local storage
function getToken() {
    return localStorage.getItem('authToken');
}

// Helper to save token
function saveToken(token) {
    localStorage.setItem('authToken', token);
}

// Helper to remove token (logout)
function logout() {
    localStorage.removeItem('authToken');
    window.location.href = 'login.html';
}

// Helper to check if user is authenticated
function checkAuth() {
    if (!getToken()) {
        window.location.href = 'login.html';
    }
}