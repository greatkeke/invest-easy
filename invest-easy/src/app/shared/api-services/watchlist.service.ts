import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, forkJoin, of } from 'rxjs';
import { catchError, map, switchMap } from 'rxjs/operators';
import { MarketService } from './market.service';
import { MarketSnapshot } from './market-snapshot.model';

export interface WatchlistItem {
  code: string;
  name: string;
  price: number;
  change: number;
  percent: string;
  volume: string;
}

@Injectable({
  providedIn: 'root'
})
export class WatchlistService {
  constructor(
    private http: HttpClient,
    private marketService: MarketService
  ) { }

  /**
   * Fetches and enriches watchlist items with current market data
   * @returns Observable of enriched WatchlistItem array
   */
  getWatchlist(): Observable<WatchlistItem[]> {
    return this.http.get<WatchlistItem[]>('/watchlist/list').pipe(
      switchMap(watchlistItems => {
        const symbols = watchlistItems.map(item => item.code);
        return forkJoin([
          of(watchlistItems),
          this.marketService.getMarketSnapshot(symbols).pipe(
            catchError(() => of([] as MarketSnapshot[]))
          )
        ]);
      }),
      map(([watchlistItems, marketSnapshots]) =>
        watchlistItems.map(item => {
          const marketData = marketSnapshots.find(s => s.code === item.code);
          if (!marketData) return item;

          const price = marketData.last_price;
          const prevClose = marketData.prev_close_price;
          const priceChange = price - prevClose;
          const percentChange = ((priceChange / prevClose) * 100).toFixed(2) + '%';

          return {
            ...item,
            price,
            change: priceChange,
            percent: percentChange,
            volume: marketData.turnover?.toString() || item.volume
          };
        })
      ),
      catchError(error => {
        console.error('Failed to load watchlist', error);
        return of([]);
      })
    );
  }

  addToWatchlist(symbol: string): Observable<any> {
    return this.http.post('/watchlist/add', { code: symbol });
  }
}
