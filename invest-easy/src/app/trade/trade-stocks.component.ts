import { Component, inject, OnInit, PLATFORM_ID, signal } from '@angular/core';
import { TopNavigationComponent } from '../shared/top-navigation/top-navigation.component';
import { CommonModule, isPlatformBrowser, Location } from '@angular/common';
import { ButtonModule } from 'primeng/button';
import { ActivatedRoute, Router } from '@angular/router';
import { ChartModule } from 'primeng/chart';
import { SelectModule } from 'primeng/select';
import { InputNumberModule } from 'primeng/inputnumber';
import { DatePickerModule } from 'primeng/datepicker';
import { FormsModule } from '@angular/forms';
import { DialogModule } from 'primeng/dialog';
import { ToastModule } from 'primeng/toast';
import { MessageService } from 'primeng/api';
import { MarketService } from '../shared/api-services/market.service';
import { MarketSnapshot } from '../shared/api-services/market-snapshot.model';
import { RTData } from '../shared/api-services/rt-data.model';
import { Account, AccountBalance, AccountsService } from '../shared/api-services/accounts.service';
import { TradeService } from '../shared/api-services/trade.service';
import { WatchlistService } from '../shared/api-services/watchlist.service';
import { RadioButtonModule } from 'primeng/radiobutton';
import { HttpErrorResponse, HttpParams } from '@angular/common/http';
import { SecuritiesQueryComponent } from '../securities-query/securities-query.component';
import { AccountSelectorComponent } from '../shared/account-selector/account-selector.component';

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
    ToastModule,
    RadioButtonModule,
    SecuritiesQueryComponent,
    AccountSelectorComponent
  ],
  templateUrl: './trade-stocks.component.html',
  styleUrls: ['./trade-stocks.component.scss'],
  providers: [MessageService]
})
export class TradeStocksComponent implements OnInit {
  private router = inject(Router);
  private route = inject(ActivatedRoute);
  private messageService = inject(MessageService);
  private marketService = inject(MarketService);
  private accountsService = inject(AccountsService);
  private tradeService = inject(TradeService);
  private watchlistService = inject(WatchlistService);
  private location = inject(Location);

  today = new Date();

  // Signal-based state
  marketSnapshot = signal<MarketSnapshot | null>(null);
  loading = signal(true);
  isWatched = signal(false);
  documentStyle!: CSSStyleDeclaration;

  tradeType = signal('buy');
  security_code = signal('');

  dialogVisible = signal(false);
  options = signal({});
  instrument = signal<any>({});

  platformId = inject(PLATFORM_ID);
  displayPreview = signal(false);
  // Trading info is now dynamically loaded from market snapshot

  // Form data
  orderTypes = [
    { label: 'Limit price', value: 'limit' },
    { label: 'Market price', value: 'market' }
  ];
  accounts = signal<AccountBalance[]>([]);
  orderForm = signal({
    type: this.orderTypes[0],
    price: 0,
    quantity: 100,
    goodUntil: new Date(),
    payFrom: { id: '', name: '', balance: 0.0, ccy: "HKD", flag: 'hk' } as AccountBalance
  });

  async ngOnInit() {
    this.initChart();
    let params = this.route.snapshot?.queryParams;
    if (params['trade'] === 'sell') {
      this.tradeType.set('sell');
    }
    this.security_code.set(params["code"] || '');
    if (!this.security_code()) {
      this.showSecurityDialog();
    } else if (this.security_code()) {
      this.loadMarketData(this.security_code());
      this.loadRTData(this.security_code());
      this.checkIfWatched();
    }
    await this.loadAccounts();
    this.marketService.getInstrumentByCode(this.security_code()).subscribe({
      next: (data: any[]) => {
        this.instrument.set(data);
        let ccy = this.instrument().ccy;
        let matched = this.accounts().filter(x => x.ccy === ccy);
        if (!!matched && matched.length > 0) {
          this.orderForm.update(form => ({ ...form, payFrom: matched[0] }));
        }
      }
    })
  }

  initChart() {
    if (isPlatformBrowser(this.platformId)) {
      this.documentStyle = getComputedStyle(document.documentElement);
      const textColor = this.documentStyle.getPropertyValue('--p-text-color');
      const textColorSecondary = this.documentStyle.getPropertyValue('--p-text-muted-color');
      const surfaceBorder = this.documentStyle.getPropertyValue('--p-content-border-color');

      this.options.set({
        responsive: true,
        maintainAspectRatio: false,
        aspectRatio: 1.4,
        plugins: {
          legend: { display: false }
        },
        elements: {
          line: {
            borderColor: 'rgb(59, 130, 246)',
            borderWidth: 1
          },
          point: {
            radius: 0
          }
        },
        scales: {
          x: {
            ticks: {
              color: textColorSecondary
            },
            grid: {
              color: surfaceBorder
            }
          },
          y: {
            ticks: {
              color: textColorSecondary
            },
            grid: {
              color: surfaceBorder
            }
          }
        }
      });
    }
  }


  showSecurityDialog() {
    this.dialogVisible.set(true);
  }

  onSecuritySelected(code: string) {
    const params = new HttpParams().appendAll({ code: code, trade: this.tradeType() });
    this.location.replaceState(location.pathname, params.toString());

    this.security_code.set(code);
    this.dialogVisible.set(false);
    this.loadMarketData(code);
    this.loadRTData(code);
  }

  closeQuery() {
    this.goBack();
  }

  async loadAccounts() {
    try {
      const accounts = await this.accountsService.fetchAccountBalances();
      if (accounts && accounts.length > 0) {
        this.accounts.set(accounts);
        this.orderForm.update(form => ({ ...form, payFrom: accounts[0] }));
      }
    } catch (error) {
      this.messageService.add({
        severity: 'error',
        summary: 'Error',
        detail: 'Failed to load accounts'
      });
    }
  }

  loadMarketData(code: string) {
    this.loading.set(true);
    this.marketService.getMarketSnapshot([code]).subscribe({
      next: (snapshots) => {
        if (snapshots && snapshots.length > 0) {
          this.marketSnapshot.set(snapshots[0]);
          this.orderForm.update(form => ({ ...form, price: snapshots[0].last_price }));
        }
        this.loading.set(false);
      },
      error: (error) => {
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail: 'Failed to load market data'
        });
        this.loading.set(false);
      }
    });
  }

  loadRTData(code: string) {
    this.marketService.getRTData(code).subscribe({
      next: (data: RTData[]) => {
        if (data && data.length > 0) {
          this.chartData.update(x => x = {
            labels: data.map((item: RTData) => item.time.split(' ')[1].substring(0, 5)), // Extract time part
            datasets: [
              {
                label: 'Price',
                data: data.map((item: RTData) => item.cur_price),
                borderColor: this.documentStyle.getPropertyValue('--p-blue-500'),
                tension: 0.4
              }
            ]
          });
        }
        this.loading.set(false);
      },
      error: (error: any) => {
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail: 'Failed to load real-time data'
        });
        this.loading.set(false);
      }
    });
  }

  // Chart data
  chartData = signal<ChartData>({
    labels: [],
    datasets: [
      {
        label: 'Price',
        data: [],
        borderColor: '#4CAF50',
        tension: 0.4
      }
    ]
  });

  // Calculate estimated total
  get estimatedTotal(): number {
    return this.orderForm().price * this.orderForm().quantity;
  }

  goBack() {
    this.router.navigate(['/trade']);
  }

  refreshData() {
    // TODO: Implement data refresh
    console.log('Refreshing data...');
  }

  showPreview() {
    this.displayPreview.set(true);
  }

  async confirmOrder() {
    if (!this.security_code()) {
      this.messageService.add({
        severity: 'error',
        summary: 'Order Failed',
        detail: 'Please select a security to trade'
      });
      return;
    }

    try {
      const request = {
        account_id: this.orderForm().payFrom.id,
        code: this.security_code(),
        price: this.orderForm().price,
        quantity: this.orderForm().quantity
      };

      if (this.tradeType() === 'buy') {
        await this.tradeService.tradeStock(request);
        this.messageService.add({
          severity: 'success',
          summary: 'Buy Order Submitted',
          detail: 'Your buy order has been placed successfully'
        });
      } else {
        await this.tradeService.tradeOut(request);
        this.messageService.add({
          severity: 'success',
          summary: 'Sell Order Submitted',
          detail: 'Your sell order has been placed successfully'
        });
      }
      this.displayPreview.set(false);
    } catch (error) {
      this.messageService.add({
        severity: 'error',
        summary: 'Order Failed',
        detail: error instanceof HttpErrorResponse ? error.error.detail : 'Failed to submit order'
      });
    }
  }

  cancelPreview() {
    this.displayPreview.set(false);
  }

  addToWatchlist() {
    if (!this.security_code() || !this.marketSnapshot()) {
      return;
    }

    if (this.isWatched()) {
      this.watchlistService.removeFromWatchlist(this.security_code()).subscribe({
        next: () => {
          this.isWatched.set(false);
          this.messageService.add({
            severity: 'success',
            summary: 'Removed from Watchlist',
            detail: `${this.marketSnapshot()?.name} has been removed from your watchlist`
          });
        },
        error: () => {
          this.messageService.add({
            severity: 'error',
            summary: 'Error',
            detail: 'Failed to remove from watchlist'
          });
        }
      });
    } else {
      this.watchlistService.addToWatchlist(this.security_code()).subscribe({
        next: () => {
          this.isWatched.set(true);
          this.messageService.add({
            severity: 'success',
            summary: 'Added to Watchlist',
            detail: `${this.marketSnapshot()?.name} has been added to your watchlist`
          });
        },
        error: () => {
          this.messageService.add({
            severity: 'error',
            summary: 'Error',
            detail: 'Failed to add to watchlist'
          });
        }
      });
    }
  }

  checkIfWatched() {
    this.watchlistService.isWatched(this.security_code()).subscribe({
      next: (watched) => {
        this.isWatched.set(watched);
      },
      error: (error) => {
        console.error('Failed to check watchlist status', error);
      }
    });
  }
}
