import { Component } from '@angular/core';
import { OrdersComponent } from './orders/orders.component';
import { CommonModule } from '@angular/common';
import { ButtonModule } from 'primeng/button';
import { TableModule } from 'primeng/table';
import { Router } from '@angular/router';
import { HeaderComponent } from '../shared/header/header.component';
import { AccountBalance, AccountsService } from '../shared/api-services/accounts.service';
import { Position, PositionService } from '../shared/api-services/position.service';

@Component({
  selector: 'app-trade',
  standalone: true,
  imports: [CommonModule, HeaderComponent, ButtonModule, TableModule, OrdersComponent],
  templateUrl: './trade.component.html',
  styleUrls: ['./trade.component.scss']
})
export class TradeComponent {
  overviewAccount: AccountBalance | undefined;
  constructor(
    private router: Router,
    private accountSvc: AccountsService,
    private positionSvc: PositionService
  ) { }

  async ngOnInit() {
    try {
      this.overviewAccount = await this.accountSvc.fetchOverviewAccountBalances();
      this.positions = await this.positionSvc.getPositions();
    } catch (error) {
      console.error('Failed to load data', error);
    }
  }

  navigateTo(target: string, params?: Record<string, any>) {
    this.router.navigate([target], { queryParams: params })
  }

  showMetrics = true;

  toggleMetrics(event: Event) {
    event.stopPropagation();
    this.showMetrics = !this.showMetrics;
  }

  positions: Position[] = [];
}
