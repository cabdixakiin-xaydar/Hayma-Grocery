import { apiFetch } from './api.js';

export async function fetchOrders() {
  return (await apiFetch('/api/orders/')) || [];
}

export async function placeOrder({ shipping_address, payment_method, coupon }) {
  // In a simple flow, client sends items based on cart not needed here if backend creates from cart.
  // For now, send empty items; in real flow, backend would read cart and compute totals.
  const payload = { shipping_address, payment_method, items: [] };
  const res = await apiFetch('/api/orders/', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
  return !!res;
}

