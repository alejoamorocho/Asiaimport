import { BaseEntity } from '../../core/types';

export interface User extends BaseEntity {
  email: string;
  first_name: string;
  last_name: string;
  is_active: boolean;
  is_staff: boolean;
  last_login?: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface LoginResponse {
  user: User;
  token: string;
  refreshToken: string;
}

export interface PasswordReset {
  email: string;
}

export interface PasswordChange {
  old_password: string;
  new_password: string;
}
