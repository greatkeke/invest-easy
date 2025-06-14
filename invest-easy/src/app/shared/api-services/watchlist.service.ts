import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface WatchlistItem {
  symbol: string;
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
  constructor(private http: HttpClient) { }

  getWatchlist(): Observable<WatchlistItem[]> {
    return this.http.get<WatchlistItem[]>('/watchlist/list');
  }

  addToWatchlist(symbol: string): Observable<any> {
    return this.http.post('/watchlist/add', { code: symbol });
  }
}
