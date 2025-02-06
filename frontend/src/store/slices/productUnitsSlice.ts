import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface ProductUnit {
  id: number;
  name: string;
  abbreviation: string;
}

interface ProductUnitsState {
  items: ProductUnit[];
  loading: boolean;
  error: string | null;
}

const initialState: ProductUnitsState = {
  items: [],
  loading: false,
  error: null,
};

const productUnitsSlice = createSlice({
  name: 'productUnits',
  initialState,
  reducers: {
    setProductUnits: (state, action: PayloadAction<ProductUnit[]>) => {
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

export const { setProductUnits, setLoading, setError } = productUnitsSlice.actions;
export default productUnitsSlice.reducer;
