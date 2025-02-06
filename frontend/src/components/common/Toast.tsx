import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { RootState } from '../../store';
import { hideToast } from '../../store/slices/uiSlice';
import { CheckCircle, XCircle, AlertCircle, Info, X } from 'lucide-react';

const Toast = () => {
  const dispatch = useDispatch();
  const { toast } = useSelector((state: RootState) => state.ui);

  useEffect(() => {
    if (toast.show) {
      const timer = setTimeout(() => {
        dispatch(hideToast());
      }, 5000);

      return () => clearTimeout(timer);
    }
  }, [toast.show, dispatch]);

  if (!toast.show) return null;

  const icons = {
    success: <CheckCircle className="h-5 w-5 text-green-400" />,
    error: <XCircle className="h-5 w-5 text-red-400" />,
    warning: <AlertCircle className="h-5 w-5 text-yellow-400" />,
    info: <Info className="h-5 w-5 text-primary-400" />,
  };

  const backgrounds = {
    success: 'bg-green-50',
    error: 'bg-red-50',
    warning: 'bg-yellow-50',
    info: 'bg-primary-50',
  };

  const textColors = {
    success: 'text-green-800',
    error: 'text-red-800',
    warning: 'text-yellow-800',
    info: 'text-primary-800',
  };

  return (
    <div className="fixed bottom-4 right-4 z-50">
      <div
        className={`${backgrounds[toast.type]} ${textColors[toast.type]} p-4 rounded-lg shadow-lg max-w-md`}
      >
        <div className="flex items-start">
          <div className="flex-shrink-0">{icons[toast.type]}</div>
          <div className="ml-3 flex-1">
            <p className="text-sm font-medium">{toast.message}</p>
          </div>
          <div className="ml-4 flex-shrink-0">
            <button
              onClick={() => dispatch(hideToast())}
              className="rounded-md bg-white text-secondary-400 hover:text-secondary-500 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"
              aria-label="Cerrar notificación"
            >
              <X className="h-5 w-5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Toast;
