import { ApiService } from '../../../core/services/api.service';
import { PaginatedResponse } from '../../../core/types';
import { CreateProductDTO, Product, ProductFilters, UpdateProductDTO } from '../types';

export class ProductService {
  private static instance: ProductService;
  private apiService: ApiService;
  private readonly baseUrl = '/api/products';

  private constructor() {
    this.apiService = ApiService.getInstance();
  }

  public static getInstance(): ProductService {
    if (!ProductService.instance) {
      ProductService.instance = new ProductService();
    }
    return ProductService.instance;
  }

  public async getProducts(
    page: number = 1,
    filters?: ProductFilters
  ): Promise<PaginatedResponse<Product>> {
    const queryParams = new URLSearchParams({
      page: page.toString(),
      ...(filters?.search && { search: filters.search }),
      ...(filters?.category_id && { category_id: filters.category_id.toString() }),
      ...(filters?.min_stock && { min_stock: filters.min_stock.toString() }),
      ...(filters?.max_stock && { max_stock: filters.max_stock.toString() }),
      ...(filters?.min_price && { min_price: filters.min_price.toString() }),
      ...(filters?.max_price && { max_price: filters.max_price.toString() }),
    });

    const response = await this.apiService.get<PaginatedResponse<Product>>(
      `${this.baseUrl}?${queryParams.toString()}`
    );
    return response.data;
  }

  public async getProduct(id: number): Promise<Product> {
    const response = await this.apiService.get<Product>(`${this.baseUrl}/${id}`);
    return response.data;
  }

  public async createProduct(data: CreateProductDTO): Promise<Product> {
    const response = await this.apiService.post<Product>(this.baseUrl, data);
    return response.data;
  }

  public async updateProduct(
    id: number,
    data: UpdateProductDTO
  ): Promise<Product> {
    const response = await this.apiService.put<Product>(
      `${this.baseUrl}/${id}`,
      data
    );
    return response.data;
  }

  public async deleteProduct(id: number): Promise<void> {
    await this.apiService.delete(`${this.baseUrl}/${id}`);
  }

  public async updateStock(id: number, quantity: number): Promise<Product> {
    const response = await this.apiService.put<Product>(
      `${this.baseUrl}/${id}/stock`,
      { quantity }
    );
    return response.data;
  }
}
