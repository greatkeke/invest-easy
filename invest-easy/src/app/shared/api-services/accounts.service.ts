export interface Account {
  id: string;
  name: string;
  ccy: string;
  flag: string;
}

export interface AccountBalance extends Account {
  balance_id: string;
  balance: number;
}

import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { lastValueFrom } from 'rxjs';
import { Flag } from '../flag';

@Injectable({
  providedIn: 'root'
})
export class AccountsService {
  private http = inject(HttpClient);


  async fetchAccounts(): Promise<Account[]> {
    try {
      const accounts = await lastValueFrom(this.http.get<any[]>('/accounts/'));
      return accounts.map(account => ({
        ...account,
        flag: this.getFlagFromCcy(account.ccy)
      } as Account));
    } catch (error) {
      throw error;
    }
  }

  private getFlagFromCcy(ccy: string): string {
    return new Flag(ccy).flag;
  }

  async fetchAccountBalances(): Promise<AccountBalance[]> {
    try {
      const balances = await lastValueFrom(this.http.get<AccountBalance[]>('/accounts/balances'));
      return balances.map(b => ({
        ...b,
        flag: this.getFlagFromCcy(b.ccy)
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
