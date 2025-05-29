import { Component } from '@angular/core';
import { NgForm } from '@angular/forms';
import { HttpClient, HttpHeaders } from '@angular/common/http';
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

    this.loading = true;
    this.errorMessage = '';

    if (this.isSignUp) {
      this.signUp(form);
    } else {
      this.login(form);
    }
  }


  signUp(form: NgForm): void {
    if (this.password !== this.confirmPassword) {
      this.errorMessage = 'Passwords do not match';
      return;
    }
    const apiUrl = 'auth/register';
    const authData = { email: this.email, password: this.password };

    this.http.post<SignUpResponse>(apiUrl, authData, { observe: 'response' }).subscribe({
      next: (response) => {
        this.loading = false;
        this.isSignUp = false;
        if (response.body) {
          this.username = response.body.email;
        }
      },
      error: (err) => {
        this.loading = false;
        this.errorMessage = err.error?.detail || ('Registration failed. Please try again.');
      }
    });
  }

  login(form: NgForm): void {
    const apiUrl = 'auth/jwt/login';

    const authData = { username: this.username, password: this.password };

    const headers = new HttpHeaders({
      'Content-Type': 'application/x-www-form-urlencoded'
    });

    // Without setting withCredentials=true, browsers will ignore cookies sent from the backend during a CORS request .
    this.http.post<LoginResponse>(apiUrl, this.toFormData(authData), { observe: 'response', headers: headers, withCredentials: true }).subscribe({
      next: (response) => {
        this.loading = false;
        if (response.body) {
          localStorage.setItem('access_token', response.body.access_token);
        }
        this.router.navigate(['/home']);
      },
      error: (err) => {
        this.loading = false;
        this.errorMessage = err.error?.detail || ('Login failed. Please check your credentials.');
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

