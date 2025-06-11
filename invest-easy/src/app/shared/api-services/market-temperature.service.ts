import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

interface MarketTemperature {
  temperature: number;
  description: string;
  trend: 'up' | 'down' | 'neutral';
  updatedAt: string;
}

@Injectable({
  providedIn: 'root'
})
export class MarketTemperatureService {
  private apiUrl = 'https://api.youzhiyouxing.com/market/temperature'; // TODO: Confirm actual API endpoint

  constructor(private http: HttpClient) { }

  getMarketTemperature(): Observable<MarketTemperature> {
    // TODO: Implement actual API call
    // Mock data for now
    return new Observable(observer => {
      observer.next({
        temperature: 65,
        description: 'Neutural Market Emotion',
        trend: 'neutral',
        updatedAt: new Date().toISOString()
      });
      observer.complete();
    });
  }
}
