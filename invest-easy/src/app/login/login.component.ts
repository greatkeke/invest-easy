import { Component } from '@angular/core';
import { NgForm } from '@angular/forms';
import { HttpClient, HttpHeaders } from '@angular/common/http';

interface LoginResponse {
  access_token: string;
  token_type: string;
}
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
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

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule, InputTextModule, PasswordModule,
    ButtonModule, InputIconModule, IconFieldModule, InputTextModule,
    IftaLabelModule, CheckboxModule, ImageModule, ProgressSpinnerModule],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent {
  constructor(private http: HttpClient, private router: Router) { }
  username = '';
  email = '';
  password = '';
  confirmPassword = '';
  rememberMe = false;
  loading = false;
  isSignUp = false;
  errorMessage = '';

  toggleMode() {
    this.isSignUp = !this.isSignUp;
    this.errorMessage = '';
  }

  onSubmit(form: NgForm) {
    if (form.invalid) return;

    if (this.isSignUp && this.password !== this.confirmPassword) {
      this.errorMessage = 'Passwords do not match';
      return;
    }

    this.loading = true;
    this.errorMessage = '';
    const apiUrl = this.isSignUp
      ? 'http://localhost:8000/auth/register'
      : 'http://localhost:8000/auth/jwt/login';

    const authData = this.isSignUp
      ? { email: this.email, password: this.password }
      : { username: this.username, password: this.password };

    const headers = new HttpHeaders({
      'Content-Type': 'application/x-www-form-urlencoded'
    });

    this.http.post<LoginResponse>(apiUrl, this.toFormData(authData), { observe: 'response', headers }).subscribe({
      next: (response) => {
        this.loading = false;
        if (response.body && !this.isSignUp) {
          localStorage.setItem('access_token', response.body.access_token);
        }
        this.router.navigate(['/home']);
      },
      error: (err) => {
        this.loading = false;
        this.errorMessage = err.error?.detail ||
          (this.isSignUp
            ? 'Registration failed. Please try again.'
            : 'Login failed. Please check your credentials.');
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
