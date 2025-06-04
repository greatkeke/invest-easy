import { Component } from '@angular/core';
import { OrdersComponent } from './orders/orders.component';
import { CommonModule } from '@angular/common';
import { ButtonModule } from 'primeng/button';
import { Router } from '@angular/router';
import { HeaderComponent } from '../shared/header/header.component';

@Component({
  selector: 'app-trade',
  standalone: true,
  imports: [CommonModule, HeaderComponent, ButtonModule, OrdersComponent],
  templateUrl: './trade.component.html',
  styleUrls: ['./trade.component.scss']
})
export class TradeComponent {
  constructor(private router: Router) {}

  navigateTo(target: string) {
    this.router.navigate([target])
  }

  showMetrics = true;
  totalAssets = 365013.73; // Will be formatted as $125K
  todayPL = 53.94; // Will be formatted as $2.45K 
  marketValue = 23410.78; // Will be formatted as $118K
  positionPL = 120.34; // Will be formatted as $7.5K
  maxWithdrawable = 25673.73; // Will be formatted as $85K

  formatCurrency(value: number): string {
    if (value >= 1000000) {
      return `$${(value/1000000).toFixed(1)}M`;
    }
    if (value >= 1000) {
      return `$${(value/1000).toFixed(1)}K`;
    }
    return `$${value}`;
  }

  toggleMetrics() {
    this.showMetrics = !this.showMetrics;
  }

  positions = [
    {
      symbol: 'QQQ',
      marketValue: 45000,
      quantity: 150,
      price: 300,
      cost: 280,
      todayPL: 1200,
      pl: 46.78,
      portfolioPercent: 0.36
    },
    {
      symbol: 'HSTI',
      marketValue: 38000,
      quantity: 200,
      price: 190,
      cost: 175,
      todayPL: 850,
      pl: -30.12,
      portfolioPercent: 0.30
    },
    {
      symbol: 'FoundBonds',
      marketValue: 35000,
      quantity: 25,
      price: 1400,
      cost: 1350,
      todayPL: 400,
      pl: 5.44,
      portfolioPercent: 0.28
    }
  ];
}
