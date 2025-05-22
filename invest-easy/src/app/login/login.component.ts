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
  password = '';
  rememberMe = false;
  loading = false;

  onSubmit() {
    this.loading = true;
    const mockApiUrl = 'https://jsonplaceholder.typicode.com/posts'; // Using placeholder mock API
    const loginData = {
      username: this.username,
      password: this.password
    };

    this.http.post(mockApiUrl, loginData).subscribe({
      next: () => {
        this.loading = false;
        this.router.navigate(['/home']);
      },
      error: (err) => {
        this.loading = false;
        console.error('Login failed:', err);
      }
    });
  }
}
