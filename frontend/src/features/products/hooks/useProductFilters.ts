import { useState, useCallback } from 'react';
import { ProductFilters } from '../types';
import { useSearchParams } from 'react-router-dom';

export function useProductFilters(initialFilters: ProductFilters = {}) {
  const [searchParams, setSearchParams] = useSearchParams();
  const [filters, setFilters] = useState<ProductFilters>(() => {
    // Initialize filters from URL params
    const params = Object.fromEntries(searchParams.entries());
    return {
      ...initialFilters,
      search: params.search || '',
      category_id: params.category_id ? Number(params.category_id) : undefined,
      min_stock: params.min_stock ? Number(params.min_stock) : undefined,
      max_stock: params.max_stock ? Number(params.max_stock) : undefined,
      min_price: params.min_price ? Number(params.min_price) : undefined,
      max_price: params.max_price ? Number(params.max_price) : undefined,
    };
  });

  const updateFilters = useCallback(
    (newFilters: ProductFilters) => {
      setFilters(newFilters);

      // Update URL params
      const params = new URLSearchParams();
      Object.entries(newFilters).forEach(([key, value]) => {
        if (value !== undefined && value !== '') {
          params.set(key, String(value));
        }
      });
      setSearchParams(params);
    },
    [setSearchParams]
  );

  const resetFilters = useCallback(() => {
    setFilters({});
    setSearchParams({});
  }, [setSearchParams]);

  return {
    filters,
    updateFilters,
    resetFilters,
  };
}
