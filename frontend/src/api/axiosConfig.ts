/// <reference types="vite/client" />

import axios from 'axios';
import { store } from '../store';
import { logout } from '../store/slices/authSlice';
import { showToast } from '../store/slices/uiSlice';
import { getAuthToken, setAuthToken } from '../utils/auth';

const baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

export const axiosInstance = axios.create({
  baseURL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
axiosInstance.interceptors.request.use(
  (config) => {
    const token = getAuthToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
axiosInstance.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    const originalRequest = error.config;

    // Handle token refresh
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refreshToken');
        if (!refreshToken) {
          throw new Error('No refresh token available');
        }

        const response = await axios.post(`${baseURL}/token/refresh/`, {
          refresh: refreshToken,
        });

        const { access } = response.data;
        setAuthToken(access);

        originalRequest.headers.Authorization = `Bearer ${access}`;
        return axiosInstance(originalRequest);
      } catch (refreshError) {
        store.dispatch(logout());
        store.dispatch(
          showToast({
            message: 'Your session has expired. Please log in again.',
            type: 'error',
          })
        );
        return Promise.reject(refreshError);
      }
    }

    // Handle other errors
    let errorMessage = 'An error occurred';
    if (error.response?.data?.detail) {
      errorMessage = error.response.data.detail;
    } else if (error.response?.data?.message) {
      errorMessage = error.response.data.message;
    } else if (error.message) {
      errorMessage = error.message;
    }

    store.dispatch(
      showToast({
        message: errorMessage,
        type: 'error',
      })
    );

    return Promise.reject(error);
  }
);

export default axiosInstance;
