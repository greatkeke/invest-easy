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
    private marketService: MarketService
  ) { }

  ngOnInit() {
    this.loadMarketData();
  }

  loadMarketData() {
    this.loading = true;
    this.marketService.getMarketSnapshot(['HK.00700']).subscribe({
      next: (snapshots) => {
        if (snapshots && snapshots.length > 0) {
          this.marketSnapshot = snapshots[0];
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
  accounts = [
    { label: 'Cash Account (USD)', value: 'cash' },
    { label: 'Margin Account (USD)', value: 'margin' }
  ];
  orderForm = {
    type: 'limit',
    price: 160.50,
    quantity: 100,
    goodUntil: new Date(),
    payFrom: 'cash'
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

  confirmOrder() {
    // TODO: Implement actual order submission
    this.messageService.add({
      severity: 'success',
      summary: 'Order Submitted',
      detail: 'Your order has been placed successfully'
    });
    this.displayPreview = false;
  }

  cancelPreview() {
    this.displayPreview = false;
  }
}
