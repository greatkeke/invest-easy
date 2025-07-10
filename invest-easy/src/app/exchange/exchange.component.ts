import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { InputNumberModule } from 'primeng/inputnumber';
import { ButtonModule } from 'primeng/button';
import { DialogModule } from 'primeng/dialog';
import { CardModule } from 'primeng/card';
import { TopNavigationComponent } from '../shared/top-navigation/top-navigation.component';
import { SelectModule } from 'primeng/select';
import { AccountSelectorComponent } from '../shared/account-selector/account-selector.component';
import { AccountBalance, AccountsService } from '../shared/api-services/accounts.service';


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
    TopNavigationComponent,
    AccountSelectorComponent
  ],
  templateUrl: './exchange.component.html',
  styleUrl: './exchange.component.scss'
})
export class ExchangeComponent implements OnInit {
  accounts: AccountBalance[] = [];

  fromAccount?: AccountBalance;
  fromAmount: number = 0.0;
  toAccount?: AccountBalance;
  toCcy: string = "";
  toAmount: number = 0.0;

  showDialog = false;
  dialogSuccess = false;
  dialogMessage = '';
  completedDate = new Date();

  constructor(private accountSvc: AccountsService) { }

  async ngOnInit(): Promise<void> {
    this.accounts = await this.accountSvc.fetchAccountBalances();

    let hkdAccount = this.accounts.filter(x => x.ccy == 'HKD')[0];
    if (hkdAccount) {
      this.fromAccount = hkdAccount;
    }
    let usdAccount = this.accounts.filter(x => x.ccy == "USD")[0];
    if (usdAccount) {
      this.toAccount = usdAccount;
    }
  }


  getExchangeRate(from?: string, to?: string): number {
    if (!!!from || !!!to) {
      return 1;
    }
    // Simplified exchange rates - in real app would fetch from API
    const rates: Record<string, number> = {
      'HKD': 1,
      'CNH': 0.97,
      'USD': 0.13,
      'EUR': 0.12,
      'GBP': 0.10,
      'JPY': 18.5,
      'CNY': 0.92
    };

    if (from === to) return 1;
    return rates[to] / rates[from];
  }

  calculateAmount(isFrom = true) {
    let rate = this.getExchangeRate(this.fromAccount?.ccy, this.toAccount?.ccy)
    let a = isFrom ? this.fromAmount : this.toAmount;
    let b = isFrom ? a * rate : a / rate;
    if (isFrom) {
      this.toAmount = b;
    } else {
      this.fromAmount = b;
    }
  }

  submitExchange() {
    if (!this.fromAccount || !this.toAccount) {
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
