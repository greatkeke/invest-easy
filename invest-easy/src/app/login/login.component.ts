import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
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
  constructor(private http: HttpClient, private router: Router) {}
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

  onSubmit() {
    if (this.isSignUp && this.password !== this.confirmPassword) {
      this.errorMessage = 'Passwords do not match';
      return;
    }

    this.loading = true;
    this.errorMessage = '';
    const mockApiUrl = 'https://jsonplaceholder.typicode.com/posts';
    const authData = this.isSignUp 
      ? { email: this.email, username: this.username, password: this.password }
      : { username: this.username, password: this.password };

    this.http.post(mockApiUrl, authData).subscribe({
      next: () => {
        this.loading = false;
        this.router.navigate(['/home']);
      },
      error: (err) => {
        this.loading = false;
        this.errorMessage = this.isSignUp 
          ? 'Sign up failed. Please try again.' 
          : 'Login failed. Invalid credentials.';
      }
    });
  }
}
