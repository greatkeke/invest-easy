import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

interface MarketIndex {
  name: string;
  symbol: string;
  price: number;
  change: number;
  percent: string;
}

import { MarketSnapshot } from './market-snapshot.model';
@Injectable({
  providedIn: 'root'
})
export class MarketService {
  private apiUrl = 'https://push2.eastmoney.com/api/qt/ulist.np/get';
  private snapshotUrl = '/market/snapshot';

  constructor(private http: HttpClient) { }

  getMarketIndices(): Observable<any> {
    const params = {
      fltt: '2',
      secids: '1.000001,0.399001,100.HSI,100.DJIA,100.NDX,100.SPX',
      fields: 'f2,f3,f4,f12,f14',
      _: Date.now()
    };
    return this.http.get(this.apiUrl, { params });
  }

  getMarketSnapshot(codes: string[]): Observable<MarketSnapshot[]> {
    return this.http.post<MarketSnapshot[]>(this.snapshotUrl, { code_list: codes });
  }
}
