import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { InputNumberModule } from 'primeng/inputnumber';
import { ButtonModule } from 'primeng/button';
import { DialogModule } from 'primeng/dialog';
import { CardModule } from 'primeng/card';
import { TopNavigationComponent } from '../shared/top-navigation/top-navigation.component';
import { SelectModule } from 'primeng/select';

interface Currency {
  code: string;
  name: string;
}

interface Account {
  id: string;
  name: string;
  balance: number;
  currency: string;
}

@Component({
  selector: 'app-exchange',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    SelectModule,
    InputNumberModule,
    ButtonModule,
    DialogModule,
    CardModule,
    TopNavigationComponent
  ],
  templateUrl: './exchange.component.html',
  styleUrl: './exchange.component.scss'
})
export class ExchangeComponent {
  currencies: Currency[] = [
    { code: 'HKD', name: 'Hong Kong Dollar' },
    { code: 'USD', name: 'US Dollar' },
    { code: 'EUR', name: 'Euro' },
    { code: 'GBP', name: 'British Pound' },
    { code: 'JPY', name: 'Japanese Yen' },
    { code: 'CNY', name: 'Chinese Yuan' }
  ];

  accounts: Account[] = [
    { id: '1', name: 'Main Account', balance: 50000, currency: 'HKD' },
    { id: '2', name: 'Savings Account', balance: 20000, currency: 'HKD' },
    { id: '3', name: 'Investment Account', balance: 15000, currency: 'USD' }
  ];

  fromCurrency: string = 'HKD';
  toCurrency: string = 'USD';
  fromAmount: number | null = null;
  toAmount: number | null = null;
  fromAccount: string = '1';

  showDialog = false;
  dialogSuccess = false;
  dialogMessage = '';
  completedDate = new Date();

  getAvailableAmount(currency: string): string {
    const account = this.accounts.find(a => a.id === this.fromAccount);
    if (account && account.currency === currency) {
      return account.balance.toLocaleString();
    }
    return '0';
  }

  getExchangeRate(from: string, to: string): number {
    // Simplified exchange rates - in real app would fetch from API
    const rates: Record<string, number> = {
      'HKD': 1,
      'USD': 0.13,
      'EUR': 0.12,
      'GBP': 0.10,
      'JPY': 18.5,
      'CNY': 0.92
    };

    if (from === to) return 1;
    return rates[to] / rates[from];
  }

  submitExchange() {
    if (!this.fromAmount || !this.toAmount) {
      this.dialogSuccess = false;
      this.dialogMessage = 'Please enter valid amounts for both currencies';
      this.showDialog = true;
      return;
    }

    // In real app, would call API here
    this.completedDate = new Date();
    this.dialogSuccess = true;
    this.dialogMessage = 'Your exchange request has been processed successfully.';
    this.showDialog = true;
  }
}
