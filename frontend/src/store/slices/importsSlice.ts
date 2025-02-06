import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface Import {
  id: number;
  date: string;
  status: string;
  file_url: string;
}

interface ImportsState {
  items: Import[];
  loading: boolean;
  error: string | null;
}

const initialState: ImportsState = {
  items: [],
  loading: false,
  error: null,
};

const importsSlice = createSlice({
  name: 'imports',
  initialState,
  reducers: {
    setImports: (state, action: PayloadAction<Import[]>) => {
      state.items = action.payload;
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.loading = action.payload;
    },
    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload;
    },
  },
});

export const { setImports, setLoading, setError } = importsSlice.actions;
export default importsSlice.reducer;
