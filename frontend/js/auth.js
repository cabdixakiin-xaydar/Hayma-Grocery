import { apiFetch, saveAuth, clearAuth } from './api.js';

export async function login(username, password) {
  const data = await apiFetch('/api/accounts/login/', {
    method: 'POST',
    body: JSON.stringify({ username, password }),
  });
  if (!data || !data.access) return false;
  saveAuth(data);
  return true;
}

export async function register(payload) {
  const ok = await apiFetch('/api/accounts/register/', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
  return !!ok;
}

export function logout() {
  clearAuth();
}

export function isLoggedIn() {
  try {
    return !!JSON.parse(localStorage.getItem('auth') || '{}').access;
  } catch (_) {
    return false;
  }
}

export function setAuthLink(el) {
  if (!el) return;
  if (isLoggedIn()) {
    el.textContent = 'Profile';
    el.href = '/frontend/profile.html';
  } else {
    el.textContent = 'Login';
    el.href = '/frontend/login.html';
  }
}

