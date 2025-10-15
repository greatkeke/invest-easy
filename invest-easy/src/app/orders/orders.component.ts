import { Component, inject, signal, computed } from '@angular/core';

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
  private ordersService = inject(OrdersService);
  private router = inject(Router);

  orders = signal<any[]>([]);
  loading = signal(false);
  allLoaded = signal(false);
  currentPage = signal(1);

  ngOnInit() {
    this.loadOrders();
  }

  navigateTo(path: string, params?: Record<string, any>) {
    this.router.navigate([path], { queryParams: params });
  }

  loadOrders() {
    this.loading.set(true);
    this.ordersService.getOrders(this.currentPage(), 5).subscribe({
      next: (orders) => {
        this.orders.update(currentOrders => [...currentOrders, ...orders]);
        this.loading.set(false);
        this.allLoaded.set(orders.length < 5); // Default page size is 5
        if (!this.allLoaded()) {
          this.currentPage.update(page => page + 1);
        }
      },
      error: () => {
        this.loading.set(false);
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
