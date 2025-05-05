import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet, RouterModule } from '@angular/router';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatTabsModule } from '@angular/material/tabs';

@Component({
  selector: 'app-root',
  imports: [CommonModule, RouterOutlet, RouterModule, MatToolbarModule, MatButtonModule, MatIconModule, MatTabsModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {
  title = 'invest-easy';
  navLinks = [
    { path: '/home', label: 'Home', icon: 'home' },
    { path: '/market', label: 'Market', icon: 'trending_up' },
    { path: '/news', label: 'News', icon: 'message' },
    { path: '/trade', label: 'Trade', icon: 'paid' }
  ];
}
