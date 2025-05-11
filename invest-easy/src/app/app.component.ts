import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet, RouterModule } from '@angular/router';
import { ButtonModule } from 'primeng/button';
import { DockModule } from 'primeng/dock';

@Component({
  selector: 'app-root',
  imports: [
    CommonModule, 
    RouterOutlet, 
    RouterModule,
    ButtonModule,
    DockModule
  ],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {
  title = 'invest-easy';
  navLinks = [
    { path: '/home', label: 'Home', icon: 'pi-home' },
    { path: '/market', label: 'Market', icon: 'pi-chart-line' },
    { path: '/news', label: 'News', icon: 'pi-book' },
    { path: '/trade', label: 'Trade', icon: 'pi-money-bill' }
  ];
}
