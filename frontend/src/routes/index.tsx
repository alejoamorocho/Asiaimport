import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import { lazy, Suspense } from 'react';
import Layout from '../components/layout/Layout';
import PrivateRoute from './PrivateRoute';
import LoadingSpinner from '../components/common/LoadingSpinner';

// Lazy loading de componentes
const Dashboard = lazy(() => import('../pages/Dashboard'));
const Products = lazy(() => import('../pages/Products'));
const Categories = lazy(() => import('../pages/Categories'));
const Imports = lazy(() => import('../pages/Imports'));
const ImportDetail = lazy(() => import('../pages/ImportDetail'));
const ProductUnits = lazy(() => import('../pages/ProductUnits'));
const Login = lazy(() => import('../pages/Login'));
const NotFound = lazy(() => import('../pages/NotFound'));

const router = createBrowserRouter([
  {
    path: '/login',
    element: (
      <Suspense fallback={<LoadingSpinner />}>
        <Login />
      </Suspense>
    ),
  },
  {
    path: '/',
    element: <Layout />,
    children: [
      {
        path: '/',
        element: (
          <PrivateRoute>
            <Suspense fallback={<LoadingSpinner />}>
              <Dashboard />
            </Suspense>
          </PrivateRoute>
        ),
      },
      {
        path: 'products',
        element: (
          <PrivateRoute>
            <Suspense fallback={<LoadingSpinner />}>
              <Products />
            </Suspense>
          </PrivateRoute>
        ),
      },
      {
        path: 'categories',
        element: (
          <PrivateRoute>
            <Suspense fallback={<LoadingSpinner />}>
              <Categories />
            </Suspense>
          </PrivateRoute>
        ),
      },
      {
        path: 'imports',
        element: (
          <PrivateRoute>
            <Suspense fallback={<LoadingSpinner />}>
              <Imports />
            </Suspense>
          </PrivateRoute>
        ),
      },
      {
        path: 'imports/:id',
        element: (
          <PrivateRoute>
            <Suspense fallback={<LoadingSpinner />}>
              <ImportDetail />
            </Suspense>
          </PrivateRoute>
        ),
      },
      {
        path: 'product-units',
        element: (
          <PrivateRoute>
            <Suspense fallback={<LoadingSpinner />}>
              <ProductUnits />
            </Suspense>
          </PrivateRoute>
        ),
      },
      {
        path: '*',
        element: (
          <Suspense fallback={<LoadingSpinner />}>
            <NotFound />
          </Suspense>
        ),
      },
    ],
  },
]);

export function AppRouter() {
  return <RouterProvider router={router} />;
}
