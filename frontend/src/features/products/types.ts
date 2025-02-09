import { BaseEntity } from '../../core/types';

export interface Product extends BaseEntity {
  name: string;
  sku: string;
  description: string;
  price: number;
  stock: number;
  category_id: number;
  image_url?: string;
  stock_threshold: number;
}

export interface ProductFilters {
  search?: string;
  category_id?: number;
  min_stock?: number;
  max_stock?: number;
  min_price?: number;
  max_price?: number;
}

export interface CreateProductDTO {
  name: string;
  sku: string;
  description: string;
  price: number;
  stock: number;
  category_id: number;
  image_url?: string;
  stock_threshold: number;
}

export interface UpdateProductDTO extends Partial<CreateProductDTO> {}
