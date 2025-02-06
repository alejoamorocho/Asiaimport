import { ProductForm } from '@/components/products/ProductForm';
import { ProductList } from '@/components/products/ProductList';

export default function ProductsPage() {
  return (
    <div className="container mx-auto py-8 space-y-8">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        {/* Formulario de producto */}
        <div className="md:col-span-1">
          <ProductForm />
        </div>

        {/* Lista de productos */}
        <div className="md:col-span-2">
          <ProductList />
        </div>
      </div>
    </div>
  );
}
