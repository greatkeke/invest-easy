import { Component, inject, signal } from '@angular/core';
import { NgForm } from '@angular/forms';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Router } from '@angular/router';

import { FormsModule } from '@angular/forms';
import { InputTextModule } from 'primeng/inputtext';
import { PasswordModule } from 'primeng/password';
import { ButtonModule } from 'primeng/button';
import { InputIconModule } from 'primeng/inputicon';
import { IconFieldModule } from 'primeng/iconfield';
import { IftaLabelModule } from 'primeng/iftalabel';
import { CheckboxModule } from 'primeng/checkbox';
import { ImageModule } from 'primeng/image';
import { ProgressSpinnerModule } from 'primeng/progressspinner';
import { AUTH_TOKEN_KEY } from '../shared/api-interceptor';

interface LoginResponse {
  access_token: string;
  token_type: string;
}

interface SignUpResponse {
  id: string;
  email: string;
  is_active: boolean;
  is_superuser: boolean;
  is_verified: boolean;
}

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule, InputTextModule, PasswordModule, ButtonModule, InputIconModule, IconFieldModule, InputTextModule, IftaLabelModule, CheckboxModule, ImageModule, ProgressSpinnerModule],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent {
  private http = inject(HttpClient);
  private router = inject(Router);

  username = signal('');
  email = signal('');
  password = signal('');
  confirmPassword = signal('');
  rememberMe = signal(false);
  loading = signal(false);
  isSignUp = signal(false);
  errorMessage = signal('');

  toggleMode() {
    this.isSignUp.set(!this.isSignUp());
    this.errorMessage.set('');
  }

  onSubmit(form: NgForm) {
    if (form.invalid) return;

    this.loading.set(true);
    this.errorMessage.set('');

    if (this.isSignUp()) {
      this.signUp(form);
    } else {
      this.login(form);
    }
  }


  signUp(form: NgForm): void {
    if (this.password() !== this.confirmPassword()) {
      this.errorMessage.set('Passwords do not match');
      return;
    }
    const apiUrl = 'auth/register';
    const authData = { email: this.email(), username: this.username(), password: this.password() };

    this.http.post<SignUpResponse>(apiUrl, authData, { observe: 'response' }).subscribe({
      next: (response) => {
        this.loading.set(false);
        this.isSignUp.set(false);
        if (response.body) {
          this.username.set(response.body.email);
        }
      },
      error: (err) => {
        this.loading.set(false);
        this.errorMessage.set(err.error?.detail || ('Registration failed. Please try again.'));
      }
    });
  }

  login(form: NgForm): void {
    const apiUrl = 'auth/jwt/login';

    const authData = { username: this.email(), password: this.password() };

    const headers = new HttpHeaders({
      'Content-Type': 'application/x-www-form-urlencoded'
    });

    this.http.post<LoginResponse>(apiUrl, this.toFormData(authData), { observe: 'response', headers: headers }).subscribe({
      next: (response) => {
        this.loading.set(false);
        if (response.body) {
          localStorage.setItem(AUTH_TOKEN_KEY, response.body.access_token);
        }
        this.router.navigate(['/home']);
      },
      error: (err) => {
        this.loading.set(false);
        this.errorMessage.set(err.error?.detail || ('Login failed. Please check your credentials.'));
      }
    });
  }

  toFormData(obj: any): string {
    const formData: string[] = [];
    for (const key in obj) {
      if (obj.hasOwnProperty(key)) {
        formData.push(encodeURIComponent(key) + '=' + encodeURIComponent(obj[key]));
      }
    }
    return formData.join('&');
  }

}
