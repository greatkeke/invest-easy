import { Component, EventEmitter, Output } from '@angular/core';
import { CommonModule, Location } from '@angular/common';
import { ButtonModule } from 'primeng/button';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { lastValueFrom } from 'rxjs';
import { ConfigService } from '../shared/config.service';
import { AUTH_TOKEN_KEY } from '../shared/api-interceptor';

@Component({
  selector: 'app-user-panel',
  templateUrl: './user-panel.component.html',
  styleUrl: './user-panel.component.scss',
  standalone: true,
  imports: [
    CommonModule,
    ButtonModule
  ]
})
export class UserPanelComponent {
  now: Date = new Date();
  username: string = '';
  menuItems = [
    { label: 'General' },
    { label: 'Security' },
    { label: 'Pay and transfer' },
    { label: 'Contact details' },
    { label: 'Communication preferences' },
    { label: 'App permissions' },
    { label: 'Investment' },
    { label: 'Open Banking consent' },
    { label: 'Activity log' }
  ];

  @Output() panelClosed = new EventEmitter<void>();

  constructor(
    private router: Router,
    private location: Location,
    private http: HttpClient,
  ) { }

  async ngOnInit(): Promise<void> {
    await this.fetchUsername();
  }

  async fetchUsername(): Promise<void> {
    try {
      const response = await lastValueFrom(
        this.http.get<{username:string}>('/authenticated-user/name')
      );
      this.username = response.username;
    } catch (error) {
      console.error('Failed to fetch username:', error);
      this.username = 'User';
    }
  }

  closePanel() {
    this.panelClosed.emit();
    this.location.back();
  }

  navigateTo(target: string) {
    this.router.navigate([target]);
  }

  async LogOff() {
    try {
      await lastValueFrom(this.http.post('/auth/jwt/logout', null));
      localStorage.removeItem(AUTH_TOKEN_KEY);
      this.router.navigate(['/login']);
    } catch (error) {
      console.error('Logout failed:', error);
      this.router.navigate(['/login']);
    }
  }
}
