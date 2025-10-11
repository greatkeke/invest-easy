import { Component } from '@angular/core';

import { TableModule } from 'primeng/table';
import { ButtonModule } from 'primeng/button';
import { Router } from '@angular/router';
import { OrdersService } from '../shared/api-services/orders.service';

@Component({
  selector: 'app-orders',
  standalone: true,
  imports: [TableModule, ButtonModule],
  templateUrl: './orders.component.html',
  styleUrls: ['./orders.component.scss']
})
export class OrdersComponent {
  orders: any[] = [];
  loading = false;
  allLoaded = false;
  currentPage = 1;

  constructor(private ordersService: OrdersService, private router: Router) {
  }

  ngOnInit() {
    this.loadOrders();
  }

  navigateTo(path: string, params?: Record<string, any>) {
    this.router.navigate([path], { queryParams: params });
  }

  loadOrders() {
    this.loading = true;
    this.ordersService.getOrders(this.currentPage, 5).subscribe({
      next: (orders) => {
        this.orders = [...this.orders, ...orders];
        this.loading = false;
        this.allLoaded = orders.length < 5; // Default page size is 5
        if (!this.allLoaded) {
          this.currentPage++;
        }
      },
      error: () => {
        this.loading = false;
      }
    });
  }

  getStatusSeverity(status: string) {
    switch (status) {
      case 'QUEUED': return 'text-cyan-800';
      case 'WORKING': return 'text-teal-900';
      case 'FILLED': return 'text-emerald-800';
      case 'CANCELLED': return 'text-slate-500';
      default: return 'text-neutral-400';
    }
  }
}
