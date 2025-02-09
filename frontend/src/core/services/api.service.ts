import axios, { AxiosInstance, AxiosRequestConfig } from 'axios';
import { api as apiConfig } from '../config';
import { ApiResponse, ServiceOptions } from '../types';

/**
 * Base API service that handles common API operations
 */
export class ApiService {
  private static instance: ApiService;
  private api: AxiosInstance;

  private constructor() {
    this.api = axios.create({
      baseURL: apiConfig.baseUrl,
      timeout: apiConfig.timeout,
    });

    this.setupInterceptors();
  }

  public static getInstance(): ApiService {
    if (!ApiService.instance) {
      ApiService.instance = new ApiService();
    }
    return ApiService.instance;
  }

  private setupInterceptors(): void {
    // Request interceptor
    this.api.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('auth_token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor
    this.api.interceptors.response.use(
      (response) => response,
      async (error) => {
        if (error.response?.status === 401) {
          // Handle token refresh here
          const refreshToken = localStorage.getItem('refresh_token');
          if (refreshToken) {
            try {
              const response = await this.post<{ token: string }>(
                '/auth/refresh',
                { refresh_token: refreshToken }
              );
              localStorage.setItem('auth_token', response.data.token);
              error.config.headers.Authorization = `Bearer ${response.data.token}`;
              return this.api.request(error.config);
            } catch (refreshError) {
              // If refresh fails, logout user
              localStorage.clear();
              window.location.href = '/login';
              return Promise.reject(refreshError);
            }
          }
        }
        return Promise.reject(error);
      }
    );
  }

  public async get<T>(
    url: string,
    config?: AxiosRequestConfig,
    options?: ServiceOptions
  ): Promise<ApiResponse<T>> {
    const response = await this.api.get<T>(url, {
      ...config,
      signal: options?.signal,
      headers: options?.headers,
    });
    return {
      data: response.data,
      status: response.status,
      message: response.statusText,
    };
  }

  public async post<T>(
    url: string,
    data?: any,
    config?: AxiosRequestConfig,
    options?: ServiceOptions
  ): Promise<ApiResponse<T>> {
    const response = await this.api.post<T>(url, data, {
      ...config,
      signal: options?.signal,
      headers: options?.headers,
    });
    return {
      data: response.data,
      status: response.status,
      message: response.statusText,
    };
  }

  public async put<T>(
    url: string,
    data?: any,
    config?: AxiosRequestConfig,
    options?: ServiceOptions
  ): Promise<ApiResponse<T>> {
    const response = await this.api.put<T>(url, data, {
      ...config,
      signal: options?.signal,
      headers: options?.headers,
    });
    return {
      data: response.data,
      status: response.status,
      message: response.statusText,
    };
  }

  public async delete<T>(
    url: string,
    config?: AxiosRequestConfig,
    options?: ServiceOptions
  ): Promise<ApiResponse<T>> {
    const response = await this.api.delete<T>(url, {
      ...config,
      signal: options?.signal,
      headers: options?.headers,
    });
    return {
      data: response.data,
      status: response.status,
      message: response.statusText,
    };
  }
}
