import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { firstValueFrom } from 'rxjs';

export interface Position {
  id: string;
  quantity: number;
  avg_price: number;
  instrument_code: string;
  instrument_name: string;
  instrument_market: string;
  ccy: string;
  marketValue: number;
  price: number;
  cost: number;
  todayPL: number;
  todayPL_p: number;
  pl: number;
  pl_p: number;
  portfolioPercent: number;
}

@Injectable({
  providedIn: 'root'
})
export class PositionService {
  constructor(private http: HttpClient) { }

  async getPositions(): Promise<Position[]> {
    try {
      const positions = await firstValueFrom(
        this.http.get<any[]>('/positions/')
      );

      // Calculate derived fields for frontend display
      return positions.map(p => ({
        ...p,
        marketValue: p.market_value,
        price: p.price,
        cost: p.avg_price,
        todayPL: p.today_pl,
        todayPL_p: !!!p.market_value ? 0.0 : p.today_pl / p.market_value,
        pl: p.pl,
        pl_p: !!!p.market_value ? 0.0 : p.pl / p.market_value,
        portfolioPercent: p.percentage
      }));
    } catch (error) {
      console.error('Failed to fetch positions', error);
      throw error;
    }
  }
}
