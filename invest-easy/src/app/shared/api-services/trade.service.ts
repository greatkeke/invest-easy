import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { firstValueFrom } from 'rxjs';

interface SubmitPositionRequest {
  account_id: string;
  code: string;
  price: number;
  quantity: number;
  stock_in: boolean;
}

@Injectable({
  providedIn: 'root'
})
export class TradeService {

  constructor(private http: HttpClient) {}

  async tradeIn(request: SubmitPositionRequest) {
    try {
      const response = await firstValueFrom(
        this.http.post('/trade/in', request)
      );
      return response;
    } catch (error) {
      throw error;
    }
  }
}
