import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { firstValueFrom } from 'rxjs';

interface SubmitPositionRequest {
  account_id: string;
  code: string;
  price: number;
  quantity: number;
}

@Injectable({
  providedIn: 'root'
})
export class TradeService {
  private http = inject(HttpClient);


  async tradeStock(request: SubmitPositionRequest) {
    try {
      const response = await firstValueFrom(
        this.http.post('/trade/in', request)
      );
      return response;
    } catch (error) {
      throw error;
    }
  }

  async tradeOut(request: SubmitPositionRequest) {
    try {
      const response = await firstValueFrom(
        this.http.post('/trade/out', request)
      );
      return response;
    } catch (error) {
      throw error;
    }
  }
}
