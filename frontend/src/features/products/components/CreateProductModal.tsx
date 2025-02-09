import React from 'react';
import {
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalFooter,
  ModalBody,
  ModalCloseButton,
  Button,
  FormControl,
  FormLabel,
  Input,
  NumberInput,
  NumberInputField,
  Select,
  VStack,
  FormErrorMessage,
} from '@chakra-ui/react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { CreateProductDTO } from '../types';
import { createProductSchema } from '../validation';
import { useCategories } from '../../categories/hooks/useCategories';

interface CreateProductModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (data: CreateProductDTO) => Promise<void>;
}

export function CreateProductModal({
  isOpen,
  onClose,
  onSubmit,
}: CreateProductModalProps) {
  const { categories } = useCategories();
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    reset,
  } = useForm<CreateProductDTO>({
    resolver: zodResolver(createProductSchema),
  });

  const handleClose = () => {
    reset();
    onClose();
  };

  const onFormSubmit = async (data: CreateProductDTO) => {
    try {
      await onSubmit(data);
      handleClose();
    } catch (error) {
      // Error handling is managed by the parent component
    }
  };

  return (
    <Modal isOpen={isOpen} onClose={handleClose} size="xl">
      <ModalOverlay />
      <ModalContent>
        <form onSubmit={handleSubmit(onFormSubmit)}>
          <ModalHeader>Create New Product</ModalHeader>
          <ModalCloseButton />
          
          <ModalBody>
            <VStack spacing={4}>
              <FormControl isInvalid={!!errors.name}>
                <FormLabel>Name</FormLabel>
                <Input {...register('name')} />
                <FormErrorMessage>{errors.name?.message}</FormErrorMessage>
              </FormControl>

              <FormControl isInvalid={!!errors.sku}>
                <FormLabel>SKU</FormLabel>
                <Input {...register('sku')} />
                <FormErrorMessage>{errors.sku?.message}</FormErrorMessage>
              </FormControl>

              <FormControl isInvalid={!!errors.description}>
                <FormLabel>Description</FormLabel>
                <Input {...register('description')} />
                <FormErrorMessage>{errors.description?.message}</FormErrorMessage>
              </FormControl>

              <FormControl isInvalid={!!errors.price}>
                <FormLabel>Price</FormLabel>
                <NumberInput min={0}>
                  <NumberInputField {...register('price')} />
                </NumberInput>
                <FormErrorMessage>{errors.price?.message}</FormErrorMessage>
              </FormControl>

              <FormControl isInvalid={!!errors.stock}>
                <FormLabel>Initial Stock</FormLabel>
                <NumberInput min={0}>
                  <NumberInputField {...register('stock')} />
                </NumberInput>
                <FormErrorMessage>{errors.stock?.message}</FormErrorMessage>
              </FormControl>

              <FormControl isInvalid={!!errors.stock_threshold}>
                <FormLabel>Stock Threshold</FormLabel>
                <NumberInput min={0}>
                  <NumberInputField {...register('stock_threshold')} />
                </NumberInput>
                <FormErrorMessage>
                  {errors.stock_threshold?.message}
                </FormErrorMessage>
              </FormControl>

              <FormControl isInvalid={!!errors.category_id}>
                <FormLabel>Category</FormLabel>
                <Select {...register('category_id')}>
                  <option value="">Select category</option>
                  {categories.map((category) => (
                    <option key={category.id} value={category.id}>
                      {category.name}
                    </option>
                  ))}
                </Select>
                <FormErrorMessage>
                  {errors.category_id?.message}
                </FormErrorMessage>
              </FormControl>

              <FormControl isInvalid={!!errors.image_url}>
                <FormLabel>Image URL</FormLabel>
                <Input {...register('image_url')} />
                <FormErrorMessage>{errors.image_url?.message}</FormErrorMessage>
              </FormControl>
            </VStack>
          </ModalBody>

          <ModalFooter>
            <Button variant="ghost" mr={3} onClick={handleClose}>
              Cancel
            </Button>
            <Button
              colorScheme="blue"
              type="submit"
              isLoading={isSubmitting}
            >
              Create
            </Button>
          </ModalFooter>
        </form>
      </ModalContent>
    </Modal>
  );
}
