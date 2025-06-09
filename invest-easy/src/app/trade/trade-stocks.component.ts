import { Component, OnInit } from '@angular/core';
import { TopNavigationComponent } from '../shared/top-navigation/top-navigation.component';
import { CommonModule } from '@angular/common';
import { ButtonModule } from 'primeng/button';
import { Router } from '@angular/router';
import { ChartModule } from 'primeng/chart';
import { SelectModule } from 'primeng/select';
import { InputNumberModule } from 'primeng/inputnumber';
import { DatePickerModule } from 'primeng/datepicker';
import { FormsModule } from '@angular/forms';
import { DialogModule } from 'primeng/dialog';
import { ToastModule } from 'primeng/toast';
import { MessageService } from 'primeng/api';
import { MarketService } from '../market/market.service';
import { MarketSnapshot } from '../market/market-snapshot.model';
import { RTData } from '../market/rt-data.model';
import { Account, AccountsService } from '../shared/api-services/accounts.service';
import { TradeService } from '../shared/api-services/trade.service';

interface ChartData {
  labels: string[];
  datasets: {
    label: string;
    data: number[];
    borderColor: string;
    tension: number;
  }[];
}

@Component({
  selector: 'app-trade-stocks',
  standalone: true,
  imports: [
    CommonModule,
    ButtonModule,
    ChartModule,
    SelectModule,
    InputNumberModule,
    DatePickerModule,
    FormsModule,
    TopNavigationComponent,
    DialogModule,
    ToastModule
  ],
  templateUrl: './trade-stocks.component.html',
  styleUrls: ['./trade-stocks.component.scss'],
  providers: [MessageService]
})
export class TradeStocksComponent implements OnInit {
  today = new Date();
  marketSnapshot: MarketSnapshot | null = null;
  loading = true;

  constructor(
    private router: Router,
    private messageService: MessageService,
    private marketService: MarketService,
    private accountsService: AccountsService,
    private tradeService: TradeService
  ) { }

  ngOnInit() {
    this.loadMarketData();
    this.loadAccounts();
  }

  async loadAccounts() {
    try {
      const accounts = await this.accountsService.fetchAccounts();
      if (accounts && accounts.length > 0) {
        this.accounts = accounts;
        this.orderForm.payFrom = accounts[0];
      }
    } catch (error) {
      this.messageService.add({
        severity: 'error',
        summary: 'Error',
        detail: 'Failed to load accounts'
      });
    }
  }

  loadMarketData() {
    this.loading = true;
    this.marketService.getMarketSnapshot(['HK.00700']).subscribe({
      next: (snapshots) => {
        if (snapshots && snapshots.length > 0) {
          this.marketSnapshot = snapshots[0];
          this.orderForm.price = this.marketSnapshot.last_price;
        }
        this.loadRTData();
      },
      error: (error) => {
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail: 'Failed to load market data'
        });
        this.loading = false;
      }
    });
  }

  loadRTData() {
    this.marketService.getRTData('HK.00700').subscribe({
      next: (data: RTData[]) => {
        if (data && data.length > 0) {
          this.chartData = {
            labels: data.map((item: RTData) => item.time.split(' ')[1].substring(0, 5)), // Extract time part
            datasets: [
              {
                label: 'Price',
                data: data.map((item: RTData) => item.cur_price),
                borderColor: '#4CAF50',
                tension: 0.4
              }
            ]
          };
        }
        this.loading = false;
      },
      error: (error: any) => {
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail: 'Failed to load real-time data'
        });
        this.loading = false;
      }
    });
  }

  displayPreview = false;

  // Chart data
  chartData: ChartData = {
    labels: [],
    datasets: [
      {
        label: 'Price',
        data: [],
        borderColor: '#4CAF50',
        tension: 0.4
      }
    ]
  };

  // Trading info is now dynamically loaded from market snapshot

  // Form data
  orderTypes = [
    { label: 'Limit price', value: 'limit' },
    { label: 'Market price', value: 'market' }
  ];
  accounts: Account[] = [];
  orderForm = {
    type: this.orderTypes[0],
    price: 0,
    quantity: 100,
    goodUntil: new Date(),
    payFrom: this.accounts.length > 0 ? this.accounts[0] : { label: '', value: '' }
  };

  // Calculate estimated total
  get estimatedTotal(): number {
    return this.orderForm.price * this.orderForm.quantity;
  }

  goBack() {
    this.router.navigate(['/trade']);
  }

  refreshData() {
    // TODO: Implement data refresh
    console.log('Refreshing data...');
  }

  showPreview() {
    this.displayPreview = true;
  }

  async confirmOrder() {
    try {
      const request = {
        account_id: this.orderForm.payFrom.value,
        code: 'HK.00700', // TODO: Make this dynamic
        price: this.orderForm.price,
        quantity: this.orderForm.quantity,
        stock_in: true // TODO: Add buy/sell toggle
      };

      await this.tradeService.tradeIn(request);
      
      this.messageService.add({
        severity: 'success',
        summary: 'Order Submitted',
        detail: 'Your order has been placed successfully'
      });
      this.displayPreview = false;
    } catch (error) {
      this.messageService.add({
        severity: 'error',
        summary: 'Order Failed',
        detail: error instanceof Error ? error.message : 'Failed to submit order'
      });
    }
  }

  cancelPreview() {
    this.displayPreview = false;
  }
}
