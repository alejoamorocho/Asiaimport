import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { RootState } from '../../store';
import { hideModal } from '../../store/slices/uiSlice';
import { X } from 'lucide-react';

const Modal = () => {
  const dispatch = useDispatch();
  const { modal } = useSelector((state: RootState) => state.ui);

  useEffect(() => {
    const handleEscape = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        dispatch(hideModal());
      }
    };

    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [dispatch]);

  if (!modal.show) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      <div className="flex min-h-screen items-center justify-center p-4">
        {/* Backdrop */}
        <div
          className="fixed inset-0 bg-secondary-900/75 transition-opacity"
          onClick={() => dispatch(hideModal())}
        />

        {/* Modal panel */}
        <div className="relative transform overflow-hidden rounded-lg bg-white shadow-xl transition-all sm:w-full sm:max-w-lg">
          {/* Header */}
          <div className="bg-white px-4 py-5 sm:px-6 border-b border-secondary-200">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-medium text-secondary-900">
                {modal.title}
              </h3>
              <button
                onClick={() => dispatch(hideModal())}
                className="rounded-md bg-white text-secondary-400 hover:text-secondary-500 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"
                aria-label="Cerrar modal"
              >
                <X className="h-6 w-6" />
              </button>
            </div>
          </div>

          {/* Content */}
          <div className="bg-white px-4 py-5 sm:p-6">{modal.content}</div>
        </div>
      </div>
    </div>
  );
};

export default Modal;
