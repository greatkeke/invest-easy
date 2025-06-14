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
import { RTData } from './rt-data.model';
@Injectable({
  providedIn: 'root'
})
export class MarketService {
  constructor(private http: HttpClient) { }

  getMarketIndices(): Observable<MarketSnapshot[]> {
    const codes = ['HK.800000', 'HK.03032', 'SH.000001', 'SZ.399001', 'SZ.399006'];
    return this.getMarketSnapshot(codes);
  }

  getMarketSnapshot(codes: string[]): Observable<MarketSnapshot[]> {
    return this.http.post<MarketSnapshot[]>('/market/snapshot', codes);
  }

  getRTData(code: string): Observable<any[]> {
    return this.http.get<RTData[]>('/market/rt-data', { params: { code } });
  }

  searchSecurities(query: string): Observable<any[]> {
    return this.http.get<any[]>('/market/search', { params: { query } });
  }
}
