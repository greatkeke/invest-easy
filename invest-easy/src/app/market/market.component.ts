import { Component, OnInit } from '@angular/core';
import { MarketIndex, MarketService } from '../shared/api-services/market.service';
import { WatchlistItem, WatchlistService } from '../shared/api-services/watchlist.service';
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
import { SkeletonModule } from 'primeng/skeleton';

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
    SecuritiesQueryComponent,
    SkeletonModule
  ]
})
export class MarketComponent implements OnInit {
  indices: MarketIndex[] = [];
  watchlist: WatchlistItem[] = [];
  marketTemperature: any = null;
  loading = true;

  constructor(private marketService: MarketService,
    private watchlistService: WatchlistService,
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
      next: (data) => {
        this.indices = data;
        this.loading = false;
      },
      error: (err) => {
        console.error('Failed to load market indices:', err);
        this.loading = false;
      }
    });
  }

  loadWatchlist(): void {
    this.watchlistService.getWatchlist().subscribe({
      next: (data) => {
        this.watchlist = data;
      },
      error: (err) => {
        console.error('Failed to load watchlist:', err);
      }
    });
  }

  navigateToResult(symbol: string): void {
    this.router.navigate(['/trade-stocks'], { queryParams: { code: symbol } });
  }
}
