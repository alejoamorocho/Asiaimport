/**
 * Application configuration
 * Centralized configuration for the frontend application
 */

export const APP_CONFIG = {
  // API Configuration
  api: {
    baseUrl: import.meta.env.VITE_API_URL || 'http://localhost:8000',
    timeout: 30000,
    retryAttempts: 3,
  },

  // Authentication Configuration
  auth: {
    tokenKey: 'auth_token',
    refreshTokenKey: 'refresh_token',
    tokenExpiry: 60 * 60 * 1000, // 1 hour
  },

  // UI Configuration
  ui: {
    theme: {
      primary: '#4F46E5',
      secondary: '#6B7280',
      success: '#10B981',
      danger: '#EF4444',
      warning: '#F59E0B',
    },
    pagination: {
      defaultPageSize: 10,
      pageSizeOptions: [10, 20, 50, 100],
    },
    toast: {
      duration: 5000,
      position: 'top-right',
    },
  },

  // Feature Flags
  features: {
    enableNotifications: true,
    enableDarkMode: false,
    enableAnalytics: false,
  },

  // Cache Configuration
  cache: {
    ttl: 5 * 60 * 1000, // 5 minutes
    prefix: 'cosmedical:',
  },
} as const;

// Type for the entire configuration
export type AppConfig = typeof APP_CONFIG;

// Export individual configurations for convenience
export const { api, auth, ui, features, cache } = APP_CONFIG;
