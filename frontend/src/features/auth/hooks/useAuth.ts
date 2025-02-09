import { useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { AuthService } from '../services/auth.service';
import { LoginCredentials } from '../types';
import { setUser, clearUser } from '../../../store/slices/authSlice';
import { useToast } from '../../../core/hooks/useToast';
import { RootState } from '../../../store/types';

export function useAuth() {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const toast = useToast();
  const authService = AuthService.getInstance();
  
  const { user, isAuthenticated } = useSelector((state: RootState) => state.auth);

  const login = useCallback(
    async (credentials: LoginCredentials) => {
      try {
        const response = await authService.login(credentials);
        dispatch(setUser(response.user));
        localStorage.setItem('auth_token', response.token);
        localStorage.setItem('refresh_token', response.refreshToken);
        toast.success('Login successful');
        navigate('/dashboard');
      } catch (error: any) {
        toast.error(error.message || 'Login failed');
        throw error;
      }
    },
    [dispatch, navigate, toast]
  );

  const logout = useCallback(() => {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('refresh_token');
    dispatch(clearUser());
    navigate('/login');
    toast.info('Logged out successfully');
  }, [dispatch, navigate, toast]);

  const checkAuth = useCallback(async () => {
    const token = localStorage.getItem('auth_token');
    if (token && !isAuthenticated) {
      try {
        const user = await authService.getCurrentUser();
        dispatch(setUser(user));
      } catch (error) {
        logout();
      }
    }
  }, [dispatch, isAuthenticated, logout]);

  return {
    user,
    isAuthenticated,
    login,
    logout,
    checkAuth,
  };
}
