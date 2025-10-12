import { Component, OnInit, inject, signal } from '@angular/core';
import { HistoryComponent } from '../history/history.component';
import { ActivatedRoute, Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { CommonModule, Location } from '@angular/common';
import { HttpClient, HttpParams } from '@angular/common/http';
import { AccountsService, Account } from '../shared/api-services/accounts.service';
import { SelectModule } from 'primeng/select';
import { TabsModule } from 'primeng/tabs';
import { DialogModule } from 'primeng/dialog';
import { ToastModule } from 'primeng/toast';
import { InputNumberModule } from 'primeng/inputnumber';
import { PasswordModule } from 'primeng/password';
import { ButtonModule } from 'primeng/button';
import { MessageService } from 'primeng/api';
import { TopNavigationComponent } from '../shared/top-navigation/top-navigation.component';
import { lastValueFrom } from 'rxjs';
import { AccountSelectorComponent } from '../shared/account-selector/account-selector.component';

@Component({
  selector: 'app-transfer',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    SelectModule,
    TabsModule,
    DialogModule,
    ToastModule,
    InputNumberModule,
    PasswordModule,
    ButtonModule,
    TopNavigationComponent,
    HistoryComponent,
    AccountSelectorComponent
  ],
  templateUrl: './transfer.component.html',
  styleUrls: ['./transfer.component.scss'],
  providers: [MessageService]
})
export class TransferComponent implements OnInit {
  private messageService = inject(MessageService);
  private route = inject(ActivatedRoute);
  private router = inject(Router);
  private http = inject(HttpClient);
  private location = inject(Location);
  private accountsService = inject(AccountsService);

  // Signal-based state
  accounts = signal<Account[]>([]);

  inForm = signal({
    toAccount: null as Account | null,
    amount: null as number | null
  });

  outForm = signal({
    fromAccount: null as Account | null,
    balance: 0, // Mock balance
    amount: null as number | null,
    password: ''
  });

  showSuccessDialog = signal(false);
  transferredAmount = signal(0);
  activeTabIndex = signal(0);
  isLoading = signal(false);
  RecordChangesAt = signal(new Date());

  ngOnInit() {
    const tab = this.route.snapshot.queryParamMap.get('tab');
    if (tab === 'out') {
      this.activeTabIndex.set(1);
    } else if (tab === 'record') {
      this.activeTabIndex.set(2);
    } else {
      this.activeTabIndex.set(0);
    }

    this.isLoading.set(true);
    this.accountsService.fetchAccounts().then(accounts => {
      this.accounts.set(accounts);
      if (this.accounts().length > 0) {
        this.inForm.update(form => ({ ...form, toAccount: this.accounts()[0] }));
        this.outForm.update(form => ({ ...form, fromAccount: this.accounts()[0] }));
      }
      this.isLoading.set(false);
    }).catch(() => {
      this.messageService.add({
        severity: 'error',
        summary: 'Error',
        detail: 'Failed to load accounts'
      });
      this.isLoading.set(false);
    });
  }

  onTabChange(event: any) {
    this.activeTabIndex.set(event);
    if (this.activeTabIndex() === 2) {
      this.RecordChangesAt.set(new Date());
    }

    let tabParam = '';
    if (this.activeTabIndex() === 1) {
      tabParam = 'out';
    } else if (this.activeTabIndex() === 2) {
      tabParam = 'record';
    }

    const params = new HttpParams().appendAll({ tab: tabParam });
    this.location.replaceState(location.pathname, params.toString());
  }

  async submitIn() {
    if (!this.inForm().toAccount || !this.inForm().amount) {
      this.messageService.add({
        severity: 'error',
        summary: 'Error',
        detail: 'Please fill all required fields'
      });
      return;
    }

    this.isLoading.set(true);
    try {
      await lastValueFrom(this.http.post('/balance/transfer/in', {
        account_id: this.inForm().toAccount?.id,
        amount: this.inForm().amount,
        transfer_in: true
      }));
      this.transferredAmount.set(this.inForm().amount || 0);
      this.RecordChangesAt.set(new Date());
      this.showSuccessDialog.set(true);
    } catch (error) {
      let accountName = this.accounts().filter(x => x.id === this.inForm().toAccount?.id)?.pop()?.name;
      this.messageService.add({
        severity: 'error',
        summary: 'Failed',
        detail: "Failed to transfer into " + accountName
      });
    }
    finally {
      this.isLoading.set(false);
    }
  }

  async submitOut() {
    if (!this.outForm().fromAccount || !this.outForm().amount || !this.outForm().password) {
      this.messageService.add({
        severity: 'error',
        summary: 'Error',
        detail: 'Please fill all required fields'
      });
      return;
    }

    this.isLoading.set(true);
    try {
      await lastValueFrom(this.http.post('/balance/transfer/out', {
        account_id: this.outForm().fromAccount?.id,
        amount: this.outForm().amount,
        password: this.outForm().password
      }));
      this.transferredAmount.set(this.outForm().amount || 0);
      this.RecordChangesAt.set(new Date());
      this.showSuccessDialog.set(true);
    } catch (error) {
      let accountName = this.accounts().filter(x => x.id === this.outForm().fromAccount?.id)?.pop()?.name;
      this.messageService.add({
        severity: 'error',
        summary: 'Failed',
        detail: "Failed to transfer from " + accountName
      });
    }
    finally {
      this.isLoading.set(false);
    }
  }

  closeDialog() {
    this.showSuccessDialog.set(false);
    this.resetForms();
  }

  checkRecord() {
    this.showSuccessDialog.set(false);
    this.activeTabIndex.set(2); // Switch to Record tab
    this.resetForms();
  }

  showSecurityTip() {
    setTimeout(() => {
      this.messageService.add({
        severity: 'warn',
        summary: 'Security Tip',
        detail: 'Be careful of security, don\'t tell anyone about the security code',
        life: 10000
      });
    }, 2000);
  }

  private resetForms() {
    this.inForm.update(form => ({ ...form, amount: null }));
    this.outForm.update(form => ({ ...form, amount: null, password: '' }));
  }
}
