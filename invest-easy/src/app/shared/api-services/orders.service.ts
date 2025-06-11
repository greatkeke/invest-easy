import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

export interface Instrument {
  id: string;
  code: string;
  name: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Order {
  id: string;
  user_account_id: string;
  instrument_id: string;
  position_id: string;
  quantity: number;
  price: number;
  trade_in: boolean;
  status: string;
  created_at: string;
}

export interface OrderResponse {
  order: Order;
  instrument: Instrument;
}

@Injectable({
  providedIn: 'root'
})
export class OrdersService {
  private apiUrl = '/orders/';

  constructor(private http: HttpClient) { }

  getOrders(): Observable<any[]> {
    return this.http.get<OrderResponse[]>(this.apiUrl).pipe(
      map(responses => responses.map(response => ({
        id: response.order.id,
        status: response.order.status,
        name: response.instrument.name,
        code: response.instrument.code,
        price: response.order.price,
        quantity: response.order.quantity,
        filled: response.order.quantity
      })))
    );
  }
}
