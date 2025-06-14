import { Component, OnInit } from '@angular/core';
import { MarketService } from '../shared/api-services/market.service';
import { MarketSnapshot } from '../shared/api-services/market-snapshot.model';
import { MarketTemperatureService } from '../shared/api-services/market-temperature.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ButtonModule } from 'primeng/button';
import { ListboxModule } from 'primeng/listbox';
import { CardModule } from 'primeng/card';
import { Router, RouterModule } from '@angular/router';
import { TabsModule } from 'primeng/tabs';
import { HeaderComponent } from '../shared/header/header.component';
import { SecuritiesQueryComponent } from '../securities-query/securities-query.component';

@Component({
  selector: 'app-market',
  standalone: true,
  templateUrl: './market.component.html',
  styleUrls: ['./market.component.scss'],
  imports: [
    CommonModule,
    FormsModule,
    HeaderComponent,
    ButtonModule,
    ListboxModule,
    CardModule,
    TabsModule,
    RouterModule,
    SecuritiesQueryComponent
  ]
})
export class MarketComponent implements OnInit {
  indices: any[] = [];
  watchlist: any[] = [];
  marketTemperature: any = null;
  loading = true;

  constructor(private marketService: MarketService,
    private marketTempService: MarketTemperatureService,
    private router: Router) { }

  ngOnInit(): void {
    this.loadMarketData();
    this.loadWatchlist();

    this.marketTempService.getMarketTemperature().subscribe({
      next: (data) => this.marketTemperature = data,
      error: (err) => console.error('Failed to load market temperature:', err)
    });
  }

  loadMarketData(): void {
    this.marketService.getMarketIndices().subscribe({
      next: (snapshots: MarketSnapshot[]) => {
        this.indices = snapshots.map(snapshot => ({
          name: snapshot.name,
          symbol: snapshot.code,
          price: snapshot.last_price,
          change: snapshot.last_price - snapshot.prev_close_price,
          percent: ((snapshot.last_price - snapshot.prev_close_price) / snapshot.prev_close_price * 100).toFixed(2)
        }));
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
      { symbol: '600036', name: 'CM Bank', price: 35.20, change: 0.45, percent: '1.29', volume: '45.2' },
      { symbol: '000858', name: 'Wuliangye Yibin', price: 152.80, change: -1.20, percent: '-0.78', volume: '12.8' },
      { symbol: '601318', name: 'Pingan', price: 48.90, change: 0.32, percent: '0.66', volume: '28.5' }
    ];
  }

  navigateToResult(symbol: string): void {
    this.router.navigate(['/trade-stocks'], { queryParams: { code: symbol } });
  }
}
