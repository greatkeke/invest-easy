import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

export interface MarketIndex {
  name: string;
  code: string;
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

  getMarketIndices(): Observable<MarketIndex[]> {
    const codes = ['HK.800000', 'HK.03032', 'US.QQQ', 'SH.000001', 'SH.000300', 'SZ.399001', 'SZ.399006'];
    return this.getMarketSnapshot(codes).pipe(
      map((snapshots: MarketSnapshot[]) => snapshots.map(snapshot => ({
        name: snapshot.name,
        code: snapshot.code,
        price: snapshot.last_price,
        change: snapshot.last_price - snapshot.prev_close_price,
        percent: ((snapshot.last_price - snapshot.prev_close_price) / snapshot.prev_close_price * 100).toFixed(2)
      })))
    );
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

  getInstrumentsByUser(): Observable<any[]> {
    return this.http.get<any[]>('/market/instruments-by-user');
  }

  getInstrumentByCode(code:string): Observable<any>{
    return this.http.get<any>(`/market/instrument/${code}`)
  }
}
