import { Injectable, inject } from '@angular/core';
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
  private http = inject(HttpClient);

  private apiUrl = 'https://api.youzhiyouxing.com/market/temperature';

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
