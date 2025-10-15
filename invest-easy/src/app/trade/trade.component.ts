import { Component, effect, inject, Signal, viewChild, signal } from '@angular/core';
import { CommonModule, KeyValuePipe, ViewportScroller } from '@angular/common';
import { ButtonModule } from 'primeng/button';
import { TableModule } from 'primeng/table';
import { Router, Scroll } from '@angular/router';
import { HeaderComponent } from '../shared/header/header.component';
import { AccountBalance, AccountsService } from '../shared/api-services/accounts.service';
import { Position, PositionService } from '../shared/api-services/position.service';
import { OrdersComponent } from '../orders/orders.component';
import { filter, map } from 'rxjs';
import { toSignal } from '@angular/core/rxjs-interop';
import { Flag } from '../shared/flag';
import { FxrateService } from '../shared/api-services/fxrate.service';

@Component({
  selector: 'app-trade',
  standalone: true,
  imports: [CommonModule, HeaderComponent, ButtonModule, TableModule, OrdersComponent, KeyValuePipe],
  templateUrl: './trade.component.html',
  styleUrls: ['./trade.component.scss']
})
export class TradeComponent {
  private router = inject(Router);
  private accountSvc = inject(AccountsService);
  private positionSvc = inject(PositionService);
  private fxrateSvc = inject(FxrateService);

  // Signal-based state
  overviewAccount = signal<AccountBalance | undefined>(undefined);
  totalPL = signal<number | undefined>(undefined);
  totalTodayPL = signal<number | undefined>(undefined);
  totalMV = signal(0.0);
  showMetrics = signal(true);
  positions = signal<Position[]>([]);
  groupPositions = signal(new Map<string, Position[]>());

  viewportScroller = inject(ViewportScroller);
  scrollingRef = viewChild<HTMLElement>('scrolling');

  constructor() {
    const scrollingPosition: Signal<[number, number] | undefined> = toSignal(
      inject(Router).events.pipe(
        filter((event): event is Scroll => event instanceof Scroll),
        map((event: Scroll) => event.position || [0, 0]),
      ),
    );

    effect(() => {
      if (this.scrollingRef() && scrollingPosition()) {
        this.viewportScroller.scrollToPosition(scrollingPosition()!);
      }
    });
  }

  async ngOnInit() {
    try {
      const account = await this.accountSvc.fetchOverviewAccountBalances();
      this.overviewAccount.set(account);
      const positions = await this.positionSvc.getPositions();
      this.positions.set(positions);
      
      let totalPL = 0;
      let totalTodayPL = 0;
      let totalMV = 0;
      const groupPositions = new Map<string, Position[]>();
      
      for (let index = 0; index < positions.length; index++) {
        const element = positions[index];
        let fxrate = this.fxrateSvc.getExchangeRate(element.ccy, account.ccy);
        totalPL += element.pl * fxrate;
        totalTodayPL += element.todayPL * fxrate;
        totalMV += element.marketValue * fxrate;
        if (groupPositions.has(element.ccy)) {
          groupPositions.get(element.ccy)?.push(element);
        } else {
          groupPositions.set(element.ccy, [element]);
        }
      }
      
      this.totalPL.set(totalPL);
      this.totalTodayPL.set(totalTodayPL);
      this.totalMV.set(totalMV);
      this.groupPositions.set(groupPositions);
    } catch (error) {
      console.error('Failed to load data', error);
    }
  }

  navigateTo(target: string, params?: Record<string, any>) {
    this.router.navigate([target], { queryParams: params })
  }

  getFlag(ccy: string) {
    return new Flag(ccy).flag;
  }

  toggleMetrics(event: Event) {
    event.stopPropagation();
    this.showMetrics.update(show => !show);
  }

  sumPL(positions: Position[]) {
    if (!!!positions) 
      return 0.0;
    return positions.reduce((acc, cur) => acc + cur.pl, 0);
  }

  sumTodayPL(positions: Position[]) {
    if (!!!positions)
      return 0.0;
    return positions.reduce((acc, cur) => acc + cur.todayPL, 0);
  }

  sumMV(positions: Position[]) {
    if (!!!positions)
      return 0.0;
    return positions.reduce((acc, cur) => acc + cur.marketValue, 0);
  }
}
