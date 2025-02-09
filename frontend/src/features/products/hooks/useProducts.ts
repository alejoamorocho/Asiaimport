import { useCallback, useState } from 'react';
import { ProductService } from '../services/product.service';
import { Product, ProductFilters } from '../types';
import { PaginatedResponse } from '../../../core/types';
import { useToast } from '../../../core/hooks/useToast';

interface UseProductsState {
  products: Product[];
  loading: boolean;
  error: string | null;
  totalCount: number;
  currentPage: number;
}

export function useProducts(initialFilters?: ProductFilters) {
  const [state, setState] = useState<UseProductsState>({
    products: [],
    loading: false,
    error: null,
    totalCount: 0,
    currentPage: 1,
  });
  const [filters, setFilters] = useState<ProductFilters>(initialFilters || {});
  const toast = useToast();
  const productService = ProductService.getInstance();

  const fetchProducts = useCallback(
    async (page: number = 1) => {
      try {
        setState((prev) => ({ ...prev, loading: true, error: null }));
        const response = await productService.getProducts(page, filters);
        setState({
          products: response.results,
          loading: false,
          error: null,
          totalCount: response.count,
          currentPage: page,
        });
      } catch (error: any) {
        setState((prev) => ({
          ...prev,
          loading: false,
          error: error.message || 'Error fetching products',
        }));
        toast.error('Error fetching products');
      }
    },
    [filters, toast]
  );

  const updateFilters = useCallback(
    (newFilters: ProductFilters) => {
      setFilters(newFilters);
      fetchProducts(1); // Reset to first page when filters change
    },
    [fetchProducts]
  );

  const createProduct = useCallback(
    async (data: CreateProductDTO) => {
      try {
        setState((prev) => ({ ...prev, loading: true, error: null }));
        await productService.createProduct(data);
        toast.success('Product created successfully');
        fetchProducts(state.currentPage);
      } catch (error: any) {
        setState((prev) => ({
          ...prev,
          loading: false,
          error: error.message || 'Error creating product',
        }));
        toast.error('Error creating product');
      }
    },
    [state.currentPage, fetchProducts, toast]
  );

  const updateProduct = useCallback(
    async (id: number, data: UpdateProductDTO) => {
      try {
        setState((prev) => ({ ...prev, loading: true, error: null }));
        await productService.updateProduct(id, data);
        toast.success('Product updated successfully');
        fetchProducts(state.currentPage);
      } catch (error: any) {
        setState((prev) => ({
          ...prev,
          loading: false,
          error: error.message || 'Error updating product',
        }));
        toast.error('Error updating product');
      }
    },
    [state.currentPage, fetchProducts, toast]
  );

  const deleteProduct = useCallback(
    async (id: number) => {
      try {
        setState((prev) => ({ ...prev, loading: true, error: null }));
        await productService.deleteProduct(id);
        toast.success('Product deleted successfully');
        fetchProducts(state.currentPage);
      } catch (error: any) {
        setState((prev) => ({
          ...prev,
          loading: false,
          error: error.message || 'Error deleting product',
        }));
        toast.error('Error deleting product');
      }
    },
    [state.currentPage, fetchProducts, toast]
  );

  return {
    ...state,
    filters,
    updateFilters,
    fetchProducts,
    createProduct,
    updateProduct,
    deleteProduct,
  };
}
