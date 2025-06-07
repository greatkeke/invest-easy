export interface Account {
  value: string;
  label: string;
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
}
