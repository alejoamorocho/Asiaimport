import React from 'react';
import {
  Table as ChakraTable,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  TableContainer,
  Box,
  Text,
  Spinner,
  Flex,
} from '@chakra-ui/react';
import { Pagination } from '../Pagination';

interface Column<T> {
  header: string;
  accessor: keyof T | ((item: T) => React.ReactNode);
  width?: string;
}

interface TableProps<T> {
  columns: Column<T>[];
  data: T[];
  isLoading?: boolean;
  error?: string | null;
  currentPage?: number;
  totalItems?: number;
  pageSize?: number;
  onPageChange?: (page: number) => void;
}

export function Table<T extends { id: number | string }>({
  columns,
  data,
  isLoading = false,
  error = null,
  currentPage,
  totalItems,
  pageSize = 10,
  onPageChange,
}: TableProps<T>) {
  if (error) {
    return (
      <Box p={4} textAlign="center">
        <Text color="red.500">{error}</Text>
      </Box>
    );
  }

  return (
    <Box>
      <TableContainer>
        <ChakraTable variant="simple">
          <Thead>
            <Tr>
              {columns.map((column, index) => (
                <Th key={index} width={column.width}>
                  {column.header}
                </Th>
              ))}
            </Tr>
          </Thead>
          <Tbody>
            {isLoading ? (
              <Tr>
                <Td colSpan={columns.length}>
                  <Flex justify="center" align="center" py={4}>
                    <Spinner />
                  </Flex>
                </Td>
              </Tr>
            ) : data.length === 0 ? (
              <Tr>
                <Td colSpan={columns.length}>
                  <Text textAlign="center">No data available</Text>
                </Td>
              </Tr>
            ) : (
              data.map((item) => (
                <Tr key={item.id}>
                  {columns.map((column, index) => (
                    <Td key={index}>
                      {typeof column.accessor === 'function'
                        ? column.accessor(item)
                        : item[column.accessor]}
                    </Td>
                  ))}
                </Tr>
              ))
            )}
          </Tbody>
        </ChakraTable>
      </TableContainer>

      {currentPage && totalItems && onPageChange && (
        <Box mt={4}>
          <Pagination
            currentPage={currentPage}
            totalItems={totalItems}
            pageSize={pageSize}
            onPageChange={onPageChange}
          />
        </Box>
      )}
    </Box>
  );
}
