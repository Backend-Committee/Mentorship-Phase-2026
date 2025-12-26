// FrontEnd/js/auth.js
const API_BASE =
  (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1")
    ? "http://localhost:3000/api"
    : `${window.location.origin}/api`;

export function getToken() {
  return localStorage.getItem("token");
}

export function getUser() {
  try { return JSON.parse(localStorage.getItem("user") || "null"); }
  catch { return null; }
}

export function logout() {
  localStorage.removeItem("token");
  localStorage.removeItem("user");
}

export function requireLogin(redirectTo = "./login.html") {
  const token = getToken();
  if (!token) window.location.href = redirectTo;
}
