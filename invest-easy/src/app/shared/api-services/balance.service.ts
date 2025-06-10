import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { lastValueFrom } from 'rxjs';

export interface BalanceDetail {
  balances: {
    account_id: string;
    amount: number;
    currency: string;
    type: string;
  }[];
}

@Injectable({
  providedIn: 'root'
})
export class BalanceService {
  constructor(private http: HttpClient) { }

  async getBalanceDetail(accountId?: string): Promise<BalanceDetail> {
    try {
      let params = new HttpParams();
      if (accountId) {
        params = params.set('account_id', accountId);
      }
      return await lastValueFrom(
        this.http.get<BalanceDetail>('/balance/detail', { params })
      );
    } catch (error) {
      throw error;
    }
  }
}
