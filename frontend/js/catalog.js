import { apiFetch } from './api.js';

export async function fetchCategories() {
  return (await apiFetch('/api/catalog/categories/')) || [];
}

export async function fetchProducts() {
  return (await apiFetch('/api/catalog/products/')) || [];
}

