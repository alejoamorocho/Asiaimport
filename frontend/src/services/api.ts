import axios from 'axios';
import { Product } from '../types/models';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const auth = {
  login: async (username: string, password: string) => {
    const response = await api.post('/auth/login/', { username, password });
    return response.data;
  },
  logout: async () => {
    localStorage.removeItem('token');
  },
};

export const products = {
  list: async (): Promise<Product[]> => {
    const response = await api.get('/products/');
    return response.data;
  },
  create: async (data: Omit<Product, 'id'>): Promise<Product> => {
    const response = await api.post('/products/', data);
    return response.data;
  },
  update: async (id: number, data: Partial<Omit<Product, 'id'>>): Promise<Product> => {
    const response = await api.put(`/products/${id}/`, data);
    return response.data;
  },
  delete: async (id: number): Promise<void> => {
    await api.delete(`/products/${id}/`);
  },
  getById: async (id: number): Promise<Product> => {
    const response = await api.get(`/products/${id}/`);
    return response.data;
  },
};

export const categories = {
  list: async () => {
    const response = await api.get('/categories/');
    return response.data;
  },
  create: async (data: { name: string; description: string }) => {
    const response = await api.post('/categories/', data);
    return response.data;
  },
};

export default api;
