import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HeaderComponent } from '../header/header.component';

@Component({
  selector: 'app-trade',
  standalone: true,
  imports: [CommonModule, HeaderComponent],
  templateUrl: './trade.component.html',
  styleUrls: ['./trade.component.scss']
})
export class TradeComponent {
  showMetrics = true;
  totalAssets = 125000;
  todayPL = 2450;
  marketValue = 118000;
  positionPL = 7500;
  maxWithdrawable = 85000;

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
