import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface UIState {
  isLoading: boolean;
  toast: {
    show: boolean;
    message: string;
    type: 'success' | 'error' | 'info' | 'warning';
  };
  modal: {
    show: boolean;
    title: string;
    content: React.ReactNode | null;
  };
}

const initialState: UIState = {
  isLoading: false,
  toast: {
    show: false,
    message: '',
    type: 'info',
  },
  modal: {
    show: false,
    title: '',
    content: null,
  },
};

const uiSlice = createSlice({
  name: 'ui',
  initialState,
  reducers: {
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.isLoading = action.payload;
    },
    showToast: (state, action: PayloadAction<{ message: string; type: 'success' | 'error' | 'info' | 'warning' }>) => {
      state.toast = {
        show: true,
        message: action.payload.message,
        type: action.payload.type,
      };
    },
    hideToast: (state) => {
      state.toast = {
        ...state.toast,
        show: false,
      };
    },
    showModal: (state, action: PayloadAction<{ title: string; content: React.ReactNode }>) => {
      state.modal = {
        show: true,
        title: action.payload.title,
        content: action.payload.content,
      };
    },
    hideModal: (state) => {
      state.modal = {
        ...state.modal,
        show: false,
      };
    },
  },
});

export const { setLoading, showToast, hideToast, showModal, hideModal } = uiSlice.actions;

export default uiSlice.reducer;
