export interface Account {
  value: string;
  label: string;
}

export interface AccountBalance {
  id: string;
  name: string;
  balance_id: string;
  balance: number;
  ccy: string;
  flag: string;
}

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { lastValueFrom } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AccountsService {
  constructor(private http: HttpClient) { }

  async fetchAccounts(): Promise<Account[]> {
    try {
      const accounts = await lastValueFrom(this.http.get<any[]>('/accounts/'));
      return accounts.map(account => ({
        label: account.name,
        value: account.id
      } as Account));
    } catch (error) {
      throw error;
    }
  }

  async fetchAccountBalances(): Promise<AccountBalance[]> {
    try {
      const balances = await lastValueFrom(this.http.get<AccountBalance[]>('/accounts/balances'));
      return balances.map(b => ({
        ...b,
        flag: b.ccy.slice(0, 2).toLocaleLowerCase()
      }));
    } catch (error) {
      throw error;
    }
  }

  async fetchOverviewAccountBalances(): Promise<AccountBalance> {
    try {
      const result = await lastValueFrom(
        this.http.get<AccountBalance[]>('/accounts/balances', {
          params: { is_overview: 'true' }
        })
      );
      if (result.length != 1)
        throw Error('No overview account');
      return result[0];
    } catch (error) {
      throw error;
    }
  }
}
