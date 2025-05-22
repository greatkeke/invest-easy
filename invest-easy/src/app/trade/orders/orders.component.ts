import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TableModule } from 'primeng/table';
import { ButtonModule } from 'primeng/button';
import { TagModule } from 'primeng/tag';

interface Order {
  id: number;
  status: 'All' | 'Queued' | 'Working' | 'Deactivated';
  name: string;
  price: number | 'Mkt Price';
  quantity: number;
  filled: number;
}

@Component({
  selector: 'app-orders',
  standalone: true,
  imports: [CommonModule, TableModule, ButtonModule, TagModule],
  templateUrl: './orders.component.html',
  styleUrls: ['./orders.component.scss']
})
export class OrdersComponent {
  orders: Order[] = [];
  loading = false;
  allLoaded = false;

  constructor() {
  }

  ngOnInit() {
    this.loadOrders();
  }

  loadOrders() {
    this.loading = true;
    // Simulate API call
    setTimeout(() => {
      const newOrders = this.generateOrders(this.orders.length, 10);
      this.orders = [...this.orders, ...newOrders];
      this.loading = false;
      this.allLoaded = this.orders.length >= 30; // Demo limit
    }, 1000);
  }

  private generateOrders(start: number, count: number): Order[] {
    const statuses: Order['status'][] = ['Queued', 'Working', 'Deactivated'];
    const stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META', 'JPM', 'V', 'WMT'];

    return Array(count).fill(0).map((_, i) => ({
      id: start + i + 1,
      status: statuses[Math.floor(Math.random() * statuses.length)],
      name: stocks[Math.floor(Math.random() * stocks.length)],
      price: Math.random() > 0.3 ? Math.round(Math.random() * 1000 * 100) / 100 : 'Mkt Price',
      quantity: Math.round(Math.random() * 1000),
      filled: Math.round(Math.random() * 1000 * Math.random())
    }));
  }

  getStatusSeverity(status: Order['status']) {
    switch (status) {
      case 'Queued': return 'info';
      case 'Working': return 'warning';
      case 'Deactivated': return 'danger';
      default: return null;
    }
  }
}
