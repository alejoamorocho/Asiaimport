import { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { RootState } from '../store';
import { getCurrentUser } from '../store/slices/authSlice';
import { AppDispatch } from '../store';

export const useAuth = () => {
  const dispatch = useDispatch<AppDispatch>();
  const { user, isAuthenticated, isLoading, error } = useSelector(
    (state: RootState) => state.auth
  );

  useEffect(() => {
    if (!isAuthenticated && !isLoading) {
      dispatch(getCurrentUser());
    }
  }, [dispatch, isAuthenticated, isLoading]);

  return {
    user,
    isAuthenticated,
    isLoading,
    error,
  };
};
