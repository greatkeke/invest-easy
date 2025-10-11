import { Component, OnInit, signal, Signal, WritableSignal } from '@angular/core';
import { ButtonModule } from 'primeng/button';
import { CardModule } from 'primeng/card';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { HeaderComponent } from '../shared/header/header.component';
import { AccountBalance, AccountsService } from '../shared/api-services/accounts.service';
import { SecuritiesQueryComponent } from '../securities-query/securities-query.component';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [ButtonModule, CardModule, CommonModule, HeaderComponent, SecuritiesQueryComponent],
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
  showPromotions = signal(true);
  promotions = signal([
    {
      title: 'Welcome Bonus',
      description: 'Receive ¥100 investment credit upon signup',
      visible: true
    }
  ]);

  showBalance = signal(true);
  account: WritableSignal<AccountBalance | undefined> = signal(undefined);

  toggleBalanceVisibility() {
    this.showBalance.set(!this.showBalance());
  }

  constructor(
    private router: Router,
    private accountSvc: AccountsService
  ) { }

  async ngOnInit() {
    await this.fetchOverviewAccount();
  }

  async fetchOverviewAccount() {
    this.account.set(await this.accountSvc.fetchOverviewAccountBalances());
  }

  closePromotion(index: number) {
    this.promotions.update(x => x.map((v, i) =>
      i === index ? { ...v, visible: !v.visible } : v
    ))
  }

  navigateTo(route: string, queryParams?: Record<string, any>) {
    this.router.navigate([route], { queryParams: queryParams });
  }

  navigateToAd(adType: string) {
    this.router.navigate(['/advertisement', { adType }]);
  }

  checkSecurity(code: string) {
    this.router.navigate(['/report', { code }]);
  }
}
