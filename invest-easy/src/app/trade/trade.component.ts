import { Component, effect, inject, Signal, viewChild } from '@angular/core';
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

@Component({
  selector: 'app-trade',
  standalone: true,
  imports: [CommonModule, HeaderComponent, ButtonModule, TableModule, OrdersComponent, KeyValuePipe],
  templateUrl: './trade.component.html',
  styleUrls: ['./trade.component.scss']
})
export class TradeComponent {
  overviewAccount: AccountBalance | undefined;
  totalPL?: number;
  totalTodayPL?: number;

  viewportScroller = inject(ViewportScroller);
  scrollingRef = viewChild<HTMLElement>('scrolling');

  constructor(
    private router: Router,
    private accountSvc: AccountsService,
    private positionSvc: PositionService
  ) {
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
      this.overviewAccount = await this.accountSvc.fetchOverviewAccountBalances();
      this.positions = await this.positionSvc.getPositions();
      this.totalPL = 0;
      this.totalTodayPL = 0;
      for (let index = 0; index < this.positions.length; index++) {
        const element = this.positions[index];
        this.totalPL += element.pl;
        this.totalTodayPL += element.todayPL;
        if (this.groupPositions.has(element.ccy)) {
          this.groupPositions.get(element.ccy)?.push(element);
        } else {
          this.groupPositions.set(element.ccy, [element]);
        }
      }
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

  showMetrics = true;

  toggleMetrics(event: Event) {
    event.stopPropagation();
    this.showMetrics = !this.showMetrics;
  }

  positions: Position[] = [];
  groupPositions: Map<string, Position[]> = new Map<string, Position[]>();

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
