import React, { useEffect, useState } from 'react';
import { useDispatch } from 'react-redux';
import { AppDispatch } from '../store';
import { Product } from '../types/models';
import { Plus } from 'lucide-react';
import ProductsTable from '../components/products/ProductsTable';
import ProductForm, { ProductFormData } from '../components/products/ProductForm';
import ConfirmDialog from '../components/common/ConfirmDialog';
import Modal from '../components/common/Modal';
import { fetchProducts, createProduct, updateProduct, deleteProduct } from '../store/slices/productsSlice';
import { fetchCategories } from '../store/slices/categoriesSlice';

const Products: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false);
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);

  useEffect(() => {
    dispatch(fetchProducts());
    dispatch(fetchCategories());
  }, [dispatch]);

  const handleCreateClick = () => {
    setSelectedProduct(null);
    setIsFormOpen(true);
  };

  const handleEditClick = (product: Product) => {
    setSelectedProduct(product);
    setIsFormOpen(true);
  };

  const handleDeleteClick = (product: Product) => {
    setSelectedProduct(product);
    setIsDeleteDialogOpen(true);
  };

  const handleFormSubmit = async (data: ProductFormData) => {
    if (selectedProduct) {
      await dispatch(updateProduct({ id: selectedProduct.id, ...data }));
    } else {
      await dispatch(createProduct(data));
    }
    setIsFormOpen(false);
    dispatch(fetchProducts());
  };

  const handleDelete = async () => {
    if (selectedProduct) {
      await dispatch(deleteProduct(selectedProduct.id));
      setIsDeleteDialogOpen(false);
      dispatch(fetchProducts());
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Productos</h1>
        <button
          onClick={handleCreateClick}
          className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        >
          <Plus className="h-5 w-5 mr-2" />
          Nuevo Producto
        </button>
      </div>

      <ProductsTable onEdit={handleEditClick} onDelete={handleDeleteClick} />

      <Modal
        isOpen={isFormOpen}
        onClose={() => setIsFormOpen(false)}
        title={selectedProduct ? 'Editar Producto' : 'Nuevo Producto'}
      >
        <ProductForm
          product={selectedProduct || undefined}
          onSubmit={handleFormSubmit}
          onCancel={() => setIsFormOpen(false)}
        />
      </Modal>

      <ConfirmDialog
        isOpen={isDeleteDialogOpen}
        title="Eliminar Producto"
        message="¿Estás seguro de que deseas eliminar este producto? Esta acción no se puede deshacer."
        confirmLabel="Eliminar"
        cancelLabel="Cancelar"
        onConfirm={handleDelete}
        onCancel={() => setIsDeleteDialogOpen(false)}
      />
    </div>
  );
};

export default Products;
