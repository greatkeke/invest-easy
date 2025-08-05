import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class FxrateService {

  // Simplified exchange rates - in real app would fetch from API
  private rates: Record<string, number> = {
    'HKD': 1,
    'CNH': 0.97,
    'USD': 0.13,
    'EUR': 0.12,
    'GBP': 0.10,
    'JPY': 18.5,
    'CNY': 0.92
  };

  getExchangeRate(from?: string, to?: string): number {
    if (!!!from || !!!to) {
      return 1;
    }

    if (from === to) return 1;
    return this.rates[to] / this.rates[from];
  }
}
