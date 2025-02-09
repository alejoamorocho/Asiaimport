import React from 'react';
import { RouteObject } from 'react-router-dom';
import { MainLayout } from '../../shared/layouts/MainLayout';
import { ProtectedRoute } from './ProtectedRoute';

// Lazy loading de las páginas
const Login = React.lazy(() => import('../../features/auth/pages/Login'));
const Dashboard = React.lazy(() => import('../../features/dashboard/pages/Dashboard'));
const Products = React.lazy(() => import('../../features/products/pages/Products'));
const ProductDetail = React.lazy(() => import('../../features/products/pages/ProductDetail'));
const Imports = React.lazy(() => import('../../features/imports/pages/Imports'));
const ImportDetail = React.lazy(() => import('../../features/imports/pages/ImportDetail'));
const Profile = React.lazy(() => import('../../features/auth/pages/Profile'));
const NotFound = React.lazy(() => import('../../shared/components/NotFound'));

export const routes: RouteObject[] = [
  {
    path: '/login',
    element: <Login />,
  },
  {
    path: '/',
    element: <MainLayout />,
    children: [
      {
        path: '/',
        element: (
          <ProtectedRoute>
            <Dashboard />
          </ProtectedRoute>
        ),
      },
      {
        path: 'products',
        element: (
          <ProtectedRoute>
            <Products />
          </ProtectedRoute>
        ),
      },
      {
        path: 'products/:id',
        element: (
          <ProtectedRoute>
            <ProductDetail />
          </ProtectedRoute>
        ),
      },
      {
        path: 'imports',
        element: (
          <ProtectedRoute>
            <Imports />
          </ProtectedRoute>
        ),
      },
      {
        path: 'imports/:id',
        element: (
          <ProtectedRoute>
            <ImportDetail />
          </ProtectedRoute>
        ),
      },
      {
        path: 'profile',
        element: (
          <ProtectedRoute>
            <Profile />
          </ProtectedRoute>
        ),
      },
      {
        path: '*',
        element: <NotFound />,
      },
    ],
  },
];
