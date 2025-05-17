import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { SelectModule } from 'primeng/select';
import { TabsModule } from 'primeng/tabs';
import { DialogModule } from 'primeng/dialog';
import { ToastModule } from 'primeng/toast';
import { InputNumberModule } from 'primeng/inputnumber';
import { PasswordModule } from 'primeng/password';
import { ButtonModule } from 'primeng/button';
import { MessageService } from 'primeng/api';
import { TopNavigationComponent } from '../shared/top-navigation/top-navigation.component';

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
    TopNavigationComponent
  ],
  templateUrl: './transfer.component.html',
  styleUrls: ['./transfer.component.scss'],
  providers: [MessageService]
})
export class TransferComponent implements OnInit {
  accounts = [
    { label: 'Account 1', value: 'acc1' },
    { label: 'Account 2', value: 'acc2' },
    { label: 'Account 3', value: 'acc3' }
  ];

  inForm = {
    fromAccount: '',
    amount: null
  };

  outForm = {
    toAccount: '',
    balance: 10000, // Mock balance
    amount: null,
    password: ''
  };

  records = [
    { type: 'In', amount: 500, time: new Date('2025-05-15'), balance: 10500 },
    { type: 'Out', amount: 200, time: new Date('2025-05-14'), balance: 9800 },
    { type: 'In', amount: 1000, time: new Date('2025-05-10'), balance: 9000 }
  ];

  showSuccessDialog = false;
  transferredAmount = 0;
  activeTabIndex = 0;

  constructor(
    private messageService: MessageService,
    private route: ActivatedRoute
  ) { }

  ngOnInit() {
    const tab = this.route.snapshot.paramMap.get('tab');
    if (tab === 'out') {
      this.activeTabIndex = 1;
    } else if (tab === 'record') {
      this.activeTabIndex = 2;
    } else {
      this.activeTabIndex = 0;
    }
  }

  onTabChange(event: any) {
    this.activeTabIndex = event.index;
    // Optional: Update URL when tab changes
    // You would need to inject Router and use router.navigate
  }

  submitIn() {
    if (!this.inForm.fromAccount || !this.inForm.amount) {
      this.messageService.add({
        severity: 'error',
        summary: 'Error',
        detail: 'Please fill all required fields'
      });
      return;
    }

    this.transferredAmount = this.inForm.amount;
    this.showSuccessDialog = true;
  }

  submitOut() {
    if (!this.outForm.toAccount || !this.outForm.amount || !this.outForm.password) {
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

    this.transferredAmount = this.outForm.amount;
    this.showSuccessDialog = true;
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
    this.inForm = { fromAccount: '', amount: null };
    this.outForm = { ...this.outForm, amount: null, password: '' };
  }
}
