import { Component, OnInit, inject, signal, computed, model } from '@angular/core';
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
import { ExchangeService } from '../shared/api-services/exchange.service';
import { FxrateService } from '../shared/api-services/fxrate.service';
import { RouterModule } from '@angular/router';


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
    AccountSelectorComponent,
    RouterModule
  ],
  templateUrl: './exchange.component.html',
  styleUrl: './exchange.component.scss'
})
export class ExchangeComponent implements OnInit {
  private accountSvc = inject(AccountsService);
  private exchangeSvc = inject(ExchangeService);
  private fxrateSvc = inject(FxrateService);

  accounts = signal<AccountBalance[]>([]);

  fromAccount = model<AccountBalance | undefined>(undefined);
  fromAmount = model<number>(0.0);
  toAccount = model<AccountBalance | undefined>(undefined);
  toAmount = model<number>(0.0);

  showDialog = signal(false);
  dialogSuccess = signal(false);
  dialogMessage = signal('');
  completedDate = signal(new Date());

  // Computed values
  exchangeRate = computed(() => {
    const fromCcy = this.fromAccount()?.ccy;
    const toCcy = this.toAccount()?.ccy;
    return this.fxrateSvc.getExchangeRate(fromCcy, toCcy);
  });

  canSubmit = computed(() => {
    return !!this.fromAccount() && !!this.toAccount() && this.fromAmount() > 0 && this.toAmount() > 0;
  });

  async ngOnInit(): Promise<void> {
    const accountBalances = await this.accountSvc.fetchAccountBalances();
    this.accounts.set(accountBalances);

    const hkdAccount = accountBalances.find(x => x.ccy === 'HKD');
    if (hkdAccount) {
      this.fromAccount.set(hkdAccount);
    }
    const usdAccount = accountBalances.find(x => x.ccy === 'USD');
    if (usdAccount) {
      this.toAccount.set(usdAccount);
    }
  }

  calculateAmount(amount: string | number | null, isFrom = true) {
    const rate = this.exchangeRate();
    
    // Convert amount to number, handling null and string cases
    const numericAmount = amount === null ? 0 : Number(amount);
    
    // Only perform calculation if we have a valid number
    if (!isNaN(numericAmount)) {
      if (isFrom) {
        this.toAmount.set(numericAmount * rate);
      } else {
        this.fromAmount.set(numericAmount / rate);
      }
    }
  }

  exchangeFlag() {
    const tmpFromAccount = this.fromAccount();
    const tmpToAccount = this.toAccount();
    
    this.fromAccount.set(tmpToAccount);
    this.toAccount.set(tmpFromAccount);

    const tmpFromAmount = this.fromAmount();
    const tmpToAmount = this.toAmount();
    
    this.fromAmount.set(tmpToAmount);
    this.toAmount.set(tmpFromAmount);
  }

  onSelectChange(prevAccount: any, isFrom = false) {
    if (this.fromAccount()?.id === this.toAccount()?.id) {
      if (isFrom) {
        this.toAccount.set(prevAccount);
      } else {
        this.fromAccount.set(prevAccount);
      }
    }
  }

  async submitExchange() {
    const fromAccount = this.fromAccount();
    const toAccount = this.toAccount();
    const fromAmount = this.fromAmount();

    if (!fromAccount || !toAccount || fromAmount <= 0) {
      this.dialogSuccess.set(false);
      this.dialogMessage.set('Please enter valid amounts for both currencies');
      this.showDialog.set(true);
      return;
    }

    const ok = await this.exchangeSvc.exchange(fromAccount.id, toAccount.id, fromAmount);

    if (ok) {
      this.completedDate.set(new Date());
      this.dialogSuccess.set(true);
      this.dialogMessage.set('Your exchange request has been processed successfully.');
      this.showDialog.set(true);
    }
  }
}
