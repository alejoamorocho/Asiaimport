import React from 'react';
import { Box, Button, Flex, Heading, useDisclosure } from '@chakra-ui/react';
import { AddIcon } from '@chakra-ui/icons';
import { ProductList } from '../components/ProductList';
import { ProductFilters } from '../components/ProductFilters';
import { CreateProductModal } from '../components/CreateProductModal';
import { useProducts } from '../hooks/useProducts';
import { useProductFilters } from '../hooks/useProductFilters';

export default function Products() {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const { filters, updateFilters } = useProductFilters();
  const {
    products,
    loading,
    error,
    totalCount,
    currentPage,
    fetchProducts,
    createProduct,
  } = useProducts(filters);

  const handleCreateProduct = async (data: CreateProductDTO) => {
    await createProduct(data);
    onClose();
  };

  return (
    <Box>
      <Flex justify="space-between" align="center" mb={6}>
        <Heading size="lg">Products</Heading>
        <Button
          leftIcon={<AddIcon />}
          colorScheme="blue"
          onClick={onOpen}
        >
          Add Product
        </Button>
      </Flex>

      <ProductFilters
        filters={filters}
        onFilterChange={updateFilters}
      />

      <ProductList
        products={products}
        loading={loading}
        error={error}
        currentPage={currentPage}
        totalItems={totalCount}
        onPageChange={fetchProducts}
      />

      <CreateProductModal
        isOpen={isOpen}
        onClose={onClose}
        onSubmit={handleCreateProduct}
      />
    </Box>
  );
}
