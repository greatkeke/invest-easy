import { Component, OnInit } from '@angular/core';
import { HistoryComponent } from '../history/history.component';
import { ActivatedRoute, Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
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
    HistoryComponent
  ],
  templateUrl: './transfer.component.html',
  styleUrls: ['./transfer.component.scss'],
  providers: [MessageService]
})
export class TransferComponent implements OnInit {
  accounts: { label: string; value: string }[] = [];

  inForm = {
    toAccount: '',
    amount: null
  };

  outForm = {
    fromAccount: '',
    balance: 0, // Mock balance
    amount: null,
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
    private http: HttpClient
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

    this.fetchAccounts();
  }

  fetchAccounts() {
    this.isLoading = true;
    this.http.get<any[]>('/accounts/').subscribe({
      next: (accounts) => {
        this.accounts = accounts.map(account => ({
          label: account.name,
          value: account.id
        }));
        if (this.accounts.length > 0) {
          this.inForm.toAccount = this.accounts[0].value;
          this.outForm.fromAccount = this.accounts[0].value;
        }
        this.isLoading = false;
      },
      error: () => {
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail: 'Failed to load accounts'
        });
        this.isLoading = false;
      }
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
    this.router.navigate([], {
      queryParams: { tab: tabParam },
      queryParamsHandling: 'merge'
    });
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
      await lastValueFrom(this.http.post('/transfer/in', {
        account_id: this.inForm.toAccount,
        amount: this.inForm.amount,
        transfer_in: true
      }));
      this.transferredAmount = this.inForm.amount;
      this.RecordChangesAt = new Date();
      this.showSuccessDialog = true;
    } catch (error) {
      let accountName = this.accounts.filter(x => x.value === this.inForm.toAccount)?.pop()?.label;
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

    if (this.outForm.amount > this.outForm.balance) {
      this.messageService.add({
        severity: 'error',
        summary: 'Error',
        detail: 'Insufficient balance'
      });
      return;
    }

    this.isLoading = true;
    try {
      await lastValueFrom(this.http.post('/transfer/out', {
        account_id: this.outForm.fromAccount,
        amount: this.outForm.amount,
        password: this.outForm.password
      }));
      this.transferredAmount = this.outForm.amount;
      this.RecordChangesAt = new Date();
      this.showSuccessDialog = true;
    } catch (error) {
      let accountName = this.accounts.filter(x => x.value === this.outForm.fromAccount)?.pop()?.label;
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

  openCustomerService() {
    this.messageService.add({
      severity: 'info',
      summary: 'Info',
      detail: 'Customer service will contact you shortly'
    });
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
    this.inForm = { toAccount: '', amount: null };
    this.outForm = { ...this.outForm, amount: null, password: '' };
  }
}
