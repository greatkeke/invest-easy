import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HeaderComponent } from '../header/header.component';
import { ButtonModule } from 'primeng/button';
import { Router } from '@angular/router';

@Component({
  selector: 'app-trade',
  standalone: true,
  imports: [CommonModule, HeaderComponent,ButtonModule],
  templateUrl: './trade.component.html',
  styleUrls: ['./trade.component.scss']
})
export class TradeComponent {
  constructor(private router: Router) {}

  navigateToAssetDetail() {
    this.router.navigate(['/asset-detail']);
  }
  showMetrics = true;
  totalAssets = 365013.73; // Will be formatted as $125K
  todayPL = 2450; // Will be formatted as $2.45K 
  marketValue = 118000; // Will be formatted as $118K
  positionPL = 7500; // Will be formatted as $7.5K
  maxWithdrawable = 85000; // Will be formatted as $85K

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
      symbol: 'AAPL',
      marketValue: 45000,
      quantity: 150,
      price: 300,
      cost: 280,
      todayPL: 1200,
      pl: 3000,
      portfolioPercent: 0.36
    },
    {
      symbol: 'MSFT',
      marketValue: 38000,
      quantity: 200,
      price: 190,
      cost: 175,
      todayPL: 850,
      pl: 3000,
      portfolioPercent: 0.30
    },
    {
      symbol: 'GOOGL',
      marketValue: 35000,
      quantity: 25,
      price: 1400,
      cost: 1350,
      todayPL: 400,
      pl: 1500,
      portfolioPercent: 0.28
    }
  ];
}
