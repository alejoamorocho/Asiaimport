import { ApiService } from '../../../core/services/api.service';
import { LoginCredentials, LoginResponse, User } from '../types';

export class AuthService {
  private static instance: AuthService;
  private apiService: ApiService;
  private readonly baseUrl = '/api/auth';

  private constructor() {
    this.apiService = ApiService.getInstance();
  }

  public static getInstance(): AuthService {
    if (!AuthService.instance) {
      AuthService.instance = new AuthService();
    }
    return AuthService.instance;
  }

  public async login(credentials: LoginCredentials): Promise<LoginResponse> {
    const response = await this.apiService.post<LoginResponse>(
      `${this.baseUrl}/login`,
      credentials
    );
    return response.data;
  }

  public async getCurrentUser(): Promise<User> {
    const response = await this.apiService.get<User>(`${this.baseUrl}/me`);
    return response.data;
  }

  public async refreshToken(refreshToken: string): Promise<LoginResponse> {
    const response = await this.apiService.post<LoginResponse>(
      `${this.baseUrl}/refresh`,
      { refresh_token: refreshToken }
    );
    return response.data;
  }

  public async updateProfile(data: Partial<User>): Promise<User> {
    const response = await this.apiService.put<User>(
      `${this.baseUrl}/profile`,
      data
    );
    return response.data;
  }

  public async changePassword(
    oldPassword: string,
    newPassword: string
  ): Promise<void> {
    await this.apiService.post(`${this.baseUrl}/change-password`, {
      old_password: oldPassword,
      new_password: newPassword,
    });
  }

  public async requestPasswordReset(email: string): Promise<void> {
    await this.apiService.post(`${this.baseUrl}/reset-password`, { email });
  }

  public async resetPassword(
    token: string,
    newPassword: string
  ): Promise<void> {
    await this.apiService.post(`${this.baseUrl}/reset-password/${token}`, {
      new_password: newPassword,
    });
  }
}
