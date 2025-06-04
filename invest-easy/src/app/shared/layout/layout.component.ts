import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { RouterModule, RouterOutlet } from '@angular/router';
import { ButtonModule } from 'primeng/button';

@Component({
  selector: 'app-layout',
  imports: [CommonModule,
    RouterOutlet,
    RouterModule,
    ButtonModule,],
  templateUrl: './layout.component.html',
  styleUrl: './layout.component.scss'
})
export class LayoutComponent {
  title = 'invest-easy';
  navLinks = [
    { path: '/home', label: 'Home', icon: 'pi-home' },
    { path: '/market', label: 'Market', icon: 'pi-chart-line' },
    { path: '/news', label: 'News', icon: 'pi-book' },
    { path: '/trade', label: 'Trade', icon: 'pi-money-bill' }
  ];
}
