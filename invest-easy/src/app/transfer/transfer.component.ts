import { Component, OnInit } from '@angular/core';
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
  accounts: Account[] = [];

  inForm = {
    toAccount: null as Account | null,
    amount: null as number | null
  };

  outForm = {
    fromAccount: null as Account | null,
    balance: 0, // Mock balance
    amount: null as number | null,
    password: ''
  };

  showSuccessDialog = false;
  transferredAmount = 0;
  activeTabIndex = 0;
  isLoading = false;
  RecordChangesAt = new Date();

  constructor(
    private messageService: MessageService,
    private route: ActivatedRoute,
    private router: Router,
    private http: HttpClient,
    private location: Location,
    private accountsService: AccountsService
  ) { }

  ngOnInit() {
    const tab = this.route.snapshot.queryParamMap.get('tab');
    if (tab === 'out') {
      this.activeTabIndex = 1;
    } else if (tab === 'record') {
      this.activeTabIndex = 2;
    } else {
      this.activeTabIndex = 0;
    }

    this.isLoading = true;
    this.accountsService.fetchAccounts().then(accounts => {
      this.accounts = accounts;
      if (this.accounts.length > 0) {
        this.inForm.toAccount = this.accounts[0];
        this.outForm.fromAccount = this.accounts[0];
      }
      this.isLoading = false;
    }).catch(() => {
      this.messageService.add({
        severity: 'error',
        summary: 'Error',
        detail: 'Failed to load accounts'
      });
      this.isLoading = false;
    });
  }


  onTabChange(event: any) {
    this.activeTabIndex = event;
    if (this.activeTabIndex == 2) {
      this.RecordChangesAt = new Date();
    }

    let tabParam = '';
    if (this.activeTabIndex === 1) {
      tabParam = 'out';
    } else if (this.activeTabIndex === 2) {
      tabParam = 'record';
    }

    const params = new HttpParams().appendAll({ tab: tabParam });
    this.location.replaceState(location.pathname, params.toString());
  }

  async submitIn() {
    if (!this.inForm.toAccount || !this.inForm.amount) {
      this.messageService.add({
        severity: 'error',
        summary: 'Error',
        detail: 'Please fill all required fields'
      });
      return;
    }

    this.isLoading = true;
    try {
      await lastValueFrom(this.http.post('/balance/transfer/in', {
        account_id: this.inForm.toAccount?.id,
        amount: this.inForm.amount,
        transfer_in: true
      }));
      this.transferredAmount = this.inForm.amount;
      this.RecordChangesAt = new Date();
      this.showSuccessDialog = true;
    } catch (error) {
      let accountName = this.accounts.filter(x => x.id === this.inForm.toAccount?.id)?.pop()?.name;
      this.messageService.add({
        severity: 'error',
        summary: 'Failed',
        detail: "Failed to transfer into " + accountName
      });
    }
    finally {
      this.isLoading = false;
    }
  }

  async submitOut() {
    if (!this.outForm.fromAccount || !this.outForm.amount || !this.outForm.password) {
      this.messageService.add({
        severity: 'error',
        summary: 'Error',
        detail: 'Please fill all required fields'
      });
      return;
    }

    this.isLoading = true;
    try {
      await lastValueFrom(this.http.post('/balance/transfer/out', {
        account_id: this.outForm.fromAccount?.id,
        amount: this.outForm.amount,
        password: this.outForm.password
      }));
      this.transferredAmount = this.outForm.amount;
      this.RecordChangesAt = new Date();
      this.showSuccessDialog = true;
    } catch (error) {
      let accountName = this.accounts.filter(x => x.id === this.outForm.fromAccount?.id)?.pop()?.name;
      this.messageService.add({
        severity: 'error',
        summary: 'Failed',
        detail: "Failed to transfer from " + accountName
      });
    }
    finally {
      this.isLoading = false;
    }
  }

  closeDialog() {
    this.showSuccessDialog = false;
    this.resetForms();
  }

  checkRecord() {
    this.showSuccessDialog = false;
    this.activeTabIndex = 2; // Switch to Record tab
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
    this.inForm = { ...this.inForm, amount: null };
    this.outForm = { ...this.outForm, amount: null, password: '' };
  }
}
