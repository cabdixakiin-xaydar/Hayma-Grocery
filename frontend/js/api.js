const API_BASE = `${window.location.origin.replace(/:\d+$/, '')}:8000`;

function getToken() {
  try {
    return JSON.parse(localStorage.getItem('auth') || '{}').access || null;
  } catch (_) {
    return null;
  }
}

export async function apiFetch(path, options = {}) {
  const headers = Object.assign({ 'Content-Type': 'application/json' }, options.headers || {});
  const token = getToken();
  if (token) headers['Authorization'] = `Bearer ${token}`;

  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers,
    credentials: 'include',
  });
  if (res.status === 204) return null;
  const data = await res.json().catch(() => null);
  if (!res.ok) {
    console.error('API error', res.status, data);
    return null;
  }
  return data;
}

export function saveAuth(auth) {
  localStorage.setItem('auth', JSON.stringify(auth));
}

export function clearAuth() {
  localStorage.removeItem('auth');
}

