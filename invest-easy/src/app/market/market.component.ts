import { Component, OnInit } from '@angular/core';
import { MarketService } from './market.service';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatTabsModule } from '@angular/material/tabs';

@Component({
  selector: 'app-market',
  standalone: true,
  templateUrl: './market.component.html',
  styleUrls: ['./market.component.scss'],
  imports: [CommonModule, MatCardModule, MatTabsModule]
})
export class MarketComponent implements OnInit {
  indices: any[] = [];
  watchlist: any[] = [];
  loading = true;

  constructor(private marketService: MarketService) {}

  ngOnInit(): void {
    this.loadMarketData();
    this.loadWatchlist();
  }

  loadMarketData(): void {
    this.marketService.getMarketIndices().subscribe({
      next: (response) => {
        if (response.data && response.data.diff) {
          this.indices = response.data.diff.map((item: any) => ({
            name: this.getMarketName(item.f12),
            symbol: item.f12,
            price: item.f2,
            change: item.f4,
            percent: item.f3
          }));
        }
        this.loading = false;
      },
      error: () => {
        this.loading = false;
      }
    });
  }

  loadWatchlist(): void {
    // TODO: Implement watchlist data loading
    // Mock data for now
    this.watchlist = [
      { symbol: '600036', name: '招商银行', price: 35.20, change: 0.45, percent: '1.29', volume: '45.2万手' },
      { symbol: '000858', name: '五粮液', price: 152.80, change: -1.20, percent: '-0.78', volume: '12.8万手' },
      { symbol: '601318', name: '中国平安', price: 48.90, change: 0.32, percent: '0.66', volume: '28.5万手' }
    ];
  }

  private getMarketName(symbol: string): string {
    const names: Record<string, string> = {
      '000001': '上证指数',
      '399001': '深证成指',
      'HSI': '恒生指数',
      'DJIA': '道琼斯',
      'NDX': '纳斯达克',
      'SPX': '标普500',
      '600036': '招商银行',
      '000858': '五粮液',
      '601318': '中国平安'
    };
    return names[symbol] || symbol;
  }
}
