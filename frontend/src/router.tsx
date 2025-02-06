import { createBrowserRouter, Navigate } from 'react-router-dom';
import Layout from './components/layout/Layout';
import LoginPage from './pages/auth/login';
import ProductsPage from './pages/Products';
import ImportsPage from './pages/imports';
import ProtectedRoute from './components/auth/ProtectedRoute';

export const router = createBrowserRouter([
  {
    path: '/',
    element: <Layout />,
    children: [
      {
        index: true,
        element: <Navigate to="/products" replace />,
      },
      {
        path: 'login',
        element: <LoginPage />,
      },
      {
        path: 'products',
        element: (
          <ProtectedRoute>
            <ProductsPage />
          </ProtectedRoute>
        ),
      },
      {
        path: 'imports',
        element: (
          <ProtectedRoute>
            <ImportsPage />
          </ProtectedRoute>
        ),
      },
    ],
  },
]);
