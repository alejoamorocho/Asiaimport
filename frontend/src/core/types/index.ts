/**
 * Core types used throughout the application
 */

// Entity Types
export interface BaseEntity {
  id: number;
  created_at: string;
  updated_at: string;
}

// Response Types
export interface ApiResponse<T> {
  data: T;
  message?: string;
  status: number;
}

export interface PaginatedResponse<T> {
  results: T[];
  count: number;
  next: string | null;
  previous: string | null;
}

// Error Types
export interface ApiError {
  message: string;
  code: string;
  details?: Record<string, string[]>;
}

// Service Types
export interface ServiceOptions {
  signal?: AbortSignal;
  headers?: Record<string, string>;
}

// Hook Types
export interface QueryConfig {
  enabled?: boolean;
  refetchInterval?: number;
  retry?: boolean | number;
  retryDelay?: number;
}

// Store Types
export interface StoreState {
  loading: boolean;
  error: ApiError | null;
}

// UI Types
export interface DialogProps {
  open: boolean;
  onClose: () => void;
  title: string;
  children: React.ReactNode;
}

export interface ToastOptions {
  duration?: number;
  position?: 'top-right' | 'top-left' | 'bottom-right' | 'bottom-left';
  type?: 'success' | 'error' | 'warning' | 'info';
}
