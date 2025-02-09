import { z } from 'zod';

export const createProductSchema = z.object({
  name: z
    .string()
    .min(1, 'Name is required')
    .max(100, 'Name must be less than 100 characters'),
  sku: z
    .string()
    .min(1, 'SKU is required')
    .max(50, 'SKU must be less than 50 characters'),
  description: z
    .string()
    .min(1, 'Description is required')
    .max(500, 'Description must be less than 500 characters'),
  price: z
    .number()
    .min(0, 'Price must be greater than or equal to 0')
    .or(z.string().regex(/^\d*\.?\d*$/).transform(Number)),
  stock: z
    .number()
    .min(0, 'Stock must be greater than or equal to 0')
    .or(z.string().regex(/^\d+$/).transform(Number)),
  stock_threshold: z
    .number()
    .min(0, 'Stock threshold must be greater than or equal to 0')
    .or(z.string().regex(/^\d+$/).transform(Number)),
  category_id: z
    .number()
    .min(1, 'Category is required')
    .or(z.string().regex(/^\d+$/).transform(Number)),
  image_url: z
    .string()
    .url('Invalid image URL')
    .optional()
    .or(z.literal('')),
});

export const updateProductSchema = createProductSchema.partial();
