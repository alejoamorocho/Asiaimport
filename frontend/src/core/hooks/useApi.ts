import { useCallback, useState } from 'react';
import { ApiService } from '../services/api.service';
import { ApiError, ApiResponse, QueryConfig, ServiceOptions } from '../types';

interface UseApiState<T> {
  data: T | null;
  loading: boolean;
  error: ApiError | null;
}

interface UseApiResponse<T> extends UseApiState<T> {
  execute: (options?: ServiceOptions) => Promise<void>;
  reset: () => void;
}

/**
 * Custom hook for making API calls with built-in state management
 */
export function useApi<T>(
  method: 'get' | 'post' | 'put' | 'delete',
  url: string,
  body?: any,
  config?: QueryConfig
): UseApiResponse<T> {
  const [state, setState] = useState<UseApiState<T>>({
    data: null,
    loading: false,
    error: null,
  });

  const apiService = ApiService.getInstance();

  const reset = useCallback(() => {
    setState({
      data: null,
      loading: false,
      error: null,
    });
  }, []);

  const execute = useCallback(
    async (options?: ServiceOptions) => {
      try {
        setState((prev) => ({ ...prev, loading: true, error: null }));

        let response: ApiResponse<T>;

        switch (method) {
          case 'get':
            response = await apiService.get<T>(url, undefined, options);
            break;
          case 'post':
            response = await apiService.post<T>(url, body, undefined, options);
            break;
          case 'put':
            response = await apiService.put<T>(url, body, undefined, options);
            break;
          case 'delete':
            response = await apiService.delete<T>(url, undefined, options);
            break;
        }

        setState({
          data: response.data,
          loading: false,
          error: null,
        });
      } catch (error: any) {
        setState({
          data: null,
          loading: false,
          error: {
            message: error.response?.data?.message || 'An error occurred',
            code: error.response?.status?.toString() || '500',
            details: error.response?.data?.details,
          },
        });

        if (config?.retry && error.response?.status !== 401) {
          const retryCount = typeof config.retry === 'number' ? config.retry : 3;
          const retryDelay = config.retryDelay || 1000;

          for (let i = 0; i < retryCount; i++) {
            await new Promise((resolve) => setTimeout(resolve, retryDelay));
            try {
              const retryResponse = await execute(options);
              return retryResponse;
            } catch {
              continue;
            }
          }
        }
      }
    },
    [apiService, method, url, body, config]
  );

  return {
    ...state,
    execute,
    reset,
  };
}
