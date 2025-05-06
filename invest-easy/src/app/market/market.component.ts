import { Component, OnInit } from '@angular/core';
import { MarketService } from './market.service';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';

@Component({
  selector: 'app-market',
  standalone: true,
  templateUrl: './market.component.html',
  styleUrls: ['./market.component.scss'],
  imports: [CommonModule, MatCardModule]
})
export class MarketComponent implements OnInit {
  indices: any[] = [];
  loading = true;

  constructor(private marketService: MarketService) {}

  ngOnInit(): void {
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

  private getMarketName(symbol: string): string {
    const names: Record<string, string> = {
      '000001': '上证指数',
      '399001': '深证成指',
      'HSI': '恒生指数',
      'DJIA': '道琼斯',
      'NDX': '纳斯达克',
      'SPX': '标普500'
    };
    return names[symbol] || symbol;
  }
}
