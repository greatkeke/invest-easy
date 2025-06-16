import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { firstValueFrom } from 'rxjs';

export interface Position {
  id: string;
  quantity: number;
  avg_price: number;
  instrument_code: string;
  instrument_name: string;
  marketValue: number;
  price: number;
  cost: number;
  todayPL: number;
  pl: number;
  portfolioPercent: number;
}

@Injectable({
  providedIn: 'root'
})
export class PositionService {
  constructor(private http: HttpClient) {}

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
        pl: p.pl, 
        portfolioPercent: p.percentage 
      }));
    } catch (error) {
      console.error('Failed to fetch positions', error);
      throw error;
    }
  }
}
