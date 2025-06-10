import { Component } from '@angular/core';
import { OrdersComponent } from './orders/orders.component';
import { CommonModule } from '@angular/common';
import { ButtonModule } from 'primeng/button';
import { Router } from '@angular/router';
import { HeaderComponent } from '../shared/header/header.component';
import { AccountBalance, AccountsService } from '../shared/api-services/accounts.service';

@Component({
  selector: 'app-trade',
  standalone: true,
  imports: [CommonModule, HeaderComponent, ButtonModule, OrdersComponent],
  templateUrl: './trade.component.html',
  styleUrls: ['./trade.component.scss']
})
export class TradeComponent {
  overviewAccount: AccountBalance | undefined;
  constructor(private router: Router, private accountSvc: AccountsService) { }

  async ngOnInit() {
    try {
      this.overviewAccount = await this.accountSvc.fetchOverviewAccountBalances();
    } catch (error) {

    }
  }

  navigateTo(target: string, queryParams?: Record<string, any>) {
    this.router.navigate([target], { queryParams })
  }

  showMetrics = true;

  toggleMetrics(event: Event) {
    event.stopPropagation();
    this.showMetrics = !this.showMetrics;
  }

  positions = [
    {
      symbol: 'QQQ',
      marketValue: 45000,
      quantity: 150,
      price: 300,
      cost: 280,
      todayPL: 1200,
      pl: 46.78,
      portfolioPercent: 0.36
    },
    {
      symbol: 'HSTI',
      marketValue: 38000,
      quantity: 200,
      price: 190,
      cost: 175,
      todayPL: 850,
      pl: -30.12,
      portfolioPercent: 0.30
    },
    {
      symbol: 'FoundBonds',
      marketValue: 35000,
      quantity: 25,
      price: 1400,
      cost: 1350,
      todayPL: 400,
      pl: 5.44,
      portfolioPercent: 0.28
    }
  ];
}
