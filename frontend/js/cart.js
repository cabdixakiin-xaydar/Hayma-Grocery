import { apiFetch } from './api.js';

export async function getCart() {
  return await apiFetch('/api/cart/');
}

export async function addToCart(productId, quantity = 1) {
  return await apiFetch('/api/cart/items/', {
    method: 'POST',
    body: JSON.stringify({ product_id: productId, quantity }),
  });
}

export async function updateCartItem(productId, quantity) {
  return await apiFetch('/api/cart/items/', {
    method: 'PUT',
    body: JSON.stringify({ product_id: productId, quantity }),
  });
}

export async function removeFromCart(productId) {
  return await apiFetch('/api/cart/items/', {
    method: 'DELETE',
    body: JSON.stringify({ product_id: productId }),
  });
}

