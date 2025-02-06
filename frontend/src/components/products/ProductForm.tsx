import React, { useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { useSelector } from 'react-redux';
import { RootState } from '../../store';
import { Product } from '../../types/models';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

interface ProductFormProps {
  product?: Product;
  onSubmit: (data: ProductFormData) => void;
  onCancel: () => void;
}

const productSchema = z.object({
  name: z.string()
    .min(3, 'El nombre debe tener al menos 3 caracteres')
    .max(100, 'El nombre no puede exceder los 100 caracteres'),
  description: z.string()
    .min(10, 'La descripción debe tener al menos 10 caracteres')
    .max(500, 'La descripción no puede exceder los 500 caracteres'),
  price: z.number()
    .min(0, 'El precio no puede ser negativo')
    .max(1000000, 'El precio no puede exceder 1,000,000'),
  category_id: z.number()
    .min(1, 'Debe seleccionar una categoría'),
  stock: z.number()
    .min(0, 'El stock no puede ser negativo')
    .max(100000, 'El stock no puede exceder 100,000'),
});

export type ProductFormData = z.infer<typeof productSchema>;

const ProductForm: React.FC<ProductFormProps> = ({ product, onSubmit, onCancel }) => {
  const { items: categories } = useSelector((state: RootState) => state.categories);
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting, isDirty },
    setError,
  } = useForm<ProductFormData>({
    resolver: zodResolver(productSchema),
    defaultValues: product
      ? {
          ...product,
          price: Number(product.price),
          stock: Number(product.stock),
        }
      : {
          name: '',
          description: '',
          price: 0,
          category_id: 0,
          stock: 0,
        },
  });

  useEffect(() => {
    if (product) {
      reset({
        ...product,
        price: Number(product.price),
        stock: Number(product.stock),
      });
    }
  }, [product, reset]);

  const onSubmitHandler = async (data: ProductFormData) => {
    try {
      await onSubmit(data);
    } catch (error) {
      if (error instanceof Error) {
        setError('root', { message: error.message });
      } else {
        setError('root', { message: 'Error al guardar el producto' });
      }
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmitHandler)} className="space-y-4">
      {errors.root && (
        <div className="p-3 bg-red-100 border border-red-400 text-red-700 rounded">
          {errors.root.message}
        </div>
      )}

      <div>
        <label htmlFor="name" className="block text-sm font-medium text-gray-700">
          Nombre
        </label>
        <input
          type="text"
          id="name"
          {...register('name')}
          className={`mt-1 block w-full rounded-md shadow-sm sm:text-sm
            ${errors.name ? 'border-red-300 focus:ring-red-500 focus:border-red-500' : 'border-gray-300 focus:ring-indigo-500 focus:border-indigo-500'}`}
        />
        {errors.name && <p className="mt-1 text-sm text-red-600">{errors.name.message}</p>}
      </div>

      <div>
        <label htmlFor="description" className="block text-sm font-medium text-gray-700">
          Descripción
        </label>
        <textarea
          id="description"
          rows={3}
          {...register('description')}
          className={`mt-1 block w-full rounded-md shadow-sm sm:text-sm
            ${errors.description ? 'border-red-300 focus:ring-red-500 focus:border-red-500' : 'border-gray-300 focus:ring-indigo-500 focus:border-indigo-500'}`}
        />
        {errors.description && <p className="mt-1 text-sm text-red-600">{errors.description.message}</p>}
      </div>

      <div>
        <label htmlFor="price" className="block text-sm font-medium text-gray-700">
          Precio
        </label>
        <div className="mt-1 relative rounded-md shadow-sm">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <span className="text-gray-500 sm:text-sm">$</span>
          </div>
          <input
            type="number"
            id="price"
            step="0.01"
            {...register('price', { valueAsNumber: true })}
            className={`pl-7 block w-full rounded-md sm:text-sm
              ${errors.price ? 'border-red-300 focus:ring-red-500 focus:border-red-500' : 'border-gray-300 focus:ring-indigo-500 focus:border-indigo-500'}`}
          />
        </div>
        {errors.price && <p className="mt-1 text-sm text-red-600">{errors.price.message}</p>}
      </div>

      <div>
        <label htmlFor="category_id" className="block text-sm font-medium text-gray-700">
          Categoría
        </label>
        <select
          id="category_id"
          {...register('category_id', { valueAsNumber: true })}
          className={`mt-1 block w-full rounded-md shadow-sm sm:text-sm
            ${errors.category_id ? 'border-red-300 focus:ring-red-500 focus:border-red-500' : 'border-gray-300 focus:ring-indigo-500 focus:border-indigo-500'}`}
        >
          <option value={0}>Seleccionar categoría</option>
          {categories.map((category) => (
            <option key={category.id} value={category.id}>
              {category.name}
            </option>
          ))}
        </select>
        {errors.category_id && <p className="mt-1 text-sm text-red-600">{errors.category_id.message}</p>}
      </div>

      <div>
        <label htmlFor="stock" className="block text-sm font-medium text-gray-700">
          Stock
        </label>
        <input
          type="number"
          id="stock"
          {...register('stock', { valueAsNumber: true })}
          className={`mt-1 block w-full rounded-md shadow-sm sm:text-sm
            ${errors.stock ? 'border-red-300 focus:ring-red-500 focus:border-red-500' : 'border-gray-300 focus:ring-indigo-500 focus:border-indigo-500'}`}
        />
        {errors.stock && <p className="mt-1 text-sm text-red-600">{errors.stock.message}</p>}
      </div>

      <div className="flex justify-end space-x-3 mt-6">
        <button
          type="button"
          onClick={onCancel}
          className="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        >
          Cancelar
        </button>
        <button
          type="submit"
          disabled={isSubmitting || !isDirty}
          className="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isSubmitting ? 'Guardando...' : product ? 'Actualizar' : 'Crear'}
        </button>
      </div>
    </form>
  );
};

export default ProductForm;
