import React from 'react';
import { Table } from '../../../shared/components/Table/Table';
import { Product } from '../types';
import { Box, Button, Image, Tag } from '@chakra-ui/react';
import { useNavigate } from 'react-router-dom';

interface ProductListProps {
  products: Product[];
  loading: boolean;
  error: string | null;
  currentPage: number;
  totalItems: number;
  onPageChange: (page: number) => void;
}

export function ProductList({
  products,
  loading,
  error,
  currentPage,
  totalItems,
  onPageChange,
}: ProductListProps) {
  const navigate = useNavigate();

  const columns = [
    {
      header: 'Image',
      accessor: (product: Product) => (
        <Box boxSize="50px">
          <Image
            src={product.image_url || '/placeholder.png'}
            alt={product.name}
            objectFit="cover"
            borderRadius="md"
          />
        </Box>
      ),
      width: '80px',
    },
    {
      header: 'Name',
      accessor: 'name',
    },
    {
      header: 'SKU',
      accessor: 'sku',
    },
    {
      header: 'Stock',
      accessor: (product: Product) => (
        <Tag
          colorScheme={product.stock <= product.stock_threshold ? 'red' : 'green'}
        >
          {product.stock}
        </Tag>
      ),
    },
    {
      header: 'Price',
      accessor: (product: Product) =>
        new Intl.NumberFormat('en-US', {
          style: 'currency',
          currency: 'USD',
        }).format(product.price),
    },
    {
      header: 'Actions',
      accessor: (product: Product) => (
        <Button
          size="sm"
          colorScheme="blue"
          onClick={() => navigate(`/products/${product.id}`)}
        >
          View
        </Button>
      ),
      width: '100px',
    },
  ];

  return (
    <Table
      columns={columns}
      data={products}
      isLoading={loading}
      error={error}
      currentPage={currentPage}
      totalItems={totalItems}
      onPageChange={onPageChange}
    />
  );
}
