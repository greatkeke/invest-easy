import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { lastValueFrom } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AccountsService {
  constructor(private http: HttpClient) { }

  async fetchAccounts() {
    try {
      const accounts = await lastValueFrom(this.http.get<any[]>('/accounts/'));
      return accounts.map(account => ({
        label: account.name,
        value: account.id
      }));
    } catch (error) {
      throw error;
    }
  }
}
