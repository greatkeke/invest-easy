import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TableModule } from 'primeng/table';
import { ButtonModule } from 'primeng/button';
import { TagModule } from 'primeng/tag';
import { OrdersService, OrderResponse } from '../../shared/api-services/orders.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-orders',
  standalone: true,
  imports: [CommonModule, TableModule, ButtonModule, TagModule],
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
      case 'QUEUED': return 'info';
      case 'WORKING': return 'warning';
      case 'FILLED': return 'success';
      case 'CANCELLED': return 'danger';
      default: return null;
    }
  }

  trimStatus(status: string): string {
    return status.substring(0, 4);
  }
}
