import { useCallback } from 'react';
import { toast, ToastOptions as ToastifyOptions } from 'react-toastify';
import { ToastOptions } from '../types';
import { ui } from '../config';

/**
 * Custom hook for managing toast notifications
 */
export function useToast() {
  const showToast = useCallback(
    (message: string, options?: ToastOptions) => {
      const toastOptions: ToastifyOptions = {
        position: options?.position || ui.toast.position,
        autoClose: options?.duration || ui.toast.duration,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
      };

      switch (options?.type) {
        case 'success':
          toast.success(message, toastOptions);
          break;
        case 'error':
          toast.error(message, toastOptions);
          break;
        case 'warning':
          toast.warning(message, toastOptions);
          break;
        case 'info':
        default:
          toast.info(message, toastOptions);
          break;
      }
    },
    []
  );

  return {
    success: (message: string, options?: Omit<ToastOptions, 'type'>) =>
      showToast(message, { ...options, type: 'success' }),
    error: (message: string, options?: Omit<ToastOptions, 'type'>) =>
      showToast(message, { ...options, type: 'error' }),
    warning: (message: string, options?: Omit<ToastOptions, 'type'>) =>
      showToast(message, { ...options, type: 'warning' }),
    info: (message: string, options?: Omit<ToastOptions, 'type'>) =>
      showToast(message, { ...options, type: 'info' }),
  };
}
