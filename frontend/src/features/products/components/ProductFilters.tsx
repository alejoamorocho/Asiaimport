import React from 'react';
import {
  Box,
  SimpleGrid,
  Input,
  Select,
  FormControl,
  FormLabel,
  NumberInput,
  NumberInputField,
} from '@chakra-ui/react';
import { ProductFilters as ProductFiltersType } from '../types';
import { useCategories } from '../../categories/hooks/useCategories';

interface ProductFiltersProps {
  filters: ProductFiltersType;
  onFilterChange: (filters: ProductFiltersType) => void;
}

export function ProductFilters({ filters, onFilterChange }: ProductFiltersProps) {
  const { categories } = useCategories();

  const handleChange = (
    field: keyof ProductFiltersType,
    value: string | number
  ) => {
    onFilterChange({
      ...filters,
      [field]: value,
    });
  };

  return (
    <Box p={4} bg="white" borderRadius="md" shadow="sm" mb={6}>
      <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={4}>
        <FormControl>
          <FormLabel>Search</FormLabel>
          <Input
            placeholder="Search products..."
            value={filters.search || ''}
            onChange={(e) => handleChange('search', e.target.value)}
          />
        </FormControl>

        <FormControl>
          <FormLabel>Category</FormLabel>
          <Select
            placeholder="All categories"
            value={filters.category_id || ''}
            onChange={(e) =>
              handleChange('category_id', e.target.value ? Number(e.target.value) : undefined)
            }
          >
            {categories.map((category) => (
              <option key={category.id} value={category.id}>
                {category.name}
              </option>
            ))}
          </Select>
        </FormControl>

        <FormControl>
          <FormLabel>Min Stock</FormLabel>
          <NumberInput
            min={0}
            value={filters.min_stock || ''}
            onChange={(_, value) => handleChange('min_stock', value)}
          >
            <NumberInputField placeholder="Min stock" />
          </NumberInput>
        </FormControl>

        <FormControl>
          <FormLabel>Max Stock</FormLabel>
          <NumberInput
            min={0}
            value={filters.max_stock || ''}
            onChange={(_, value) => handleChange('max_stock', value)}
          >
            <NumberInputField placeholder="Max stock" />
          </NumberInput>
        </FormControl>

        <FormControl>
          <FormLabel>Min Price</FormLabel>
          <NumberInput
            min={0}
            value={filters.min_price || ''}
            onChange={(_, value) => handleChange('min_price', value)}
          >
            <NumberInputField placeholder="Min price" />
          </NumberInput>
        </FormControl>

        <FormControl>
          <FormLabel>Max Price</FormLabel>
          <NumberInput
            min={0}
            value={filters.max_price || ''}
            onChange={(_, value) => handleChange('max_price', value)}
          >
            <NumberInputField placeholder="Max price" />
          </NumberInput>
        </FormControl>
      </SimpleGrid>
    </Box>
  );
}
