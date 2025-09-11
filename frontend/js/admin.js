import { apiFetch } from './api.js';

export async function adminListProducts() {
  return (await apiFetch('/api/catalog/products/')) || [];
}

export async function adminCreateProduct(payload) {
  return await apiFetch('/api/catalog/products/', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export async function adminDeleteProduct(id) {
  return await apiFetch(`/api/catalog/products/${id}/`, { method: 'DELETE' });
}

