import { Component, OnInit, inject, signal } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { OrdersService, OrderDetail } from '../../shared/api-services/orders.service';
import { TopNavigationComponent } from '../../shared/top-navigation/top-navigation.component';
import { CardModule } from 'primeng/card';
import { FieldsetModule } from 'primeng/fieldset';
import { TagModule } from 'primeng/tag';
import { ProgressSpinnerModule } from 'primeng/progressspinner';
import { CommonModule } from '@angular/common';
import { SkeletonModule } from 'primeng/skeleton';

@Component({
  selector: 'app-orders-detail',
  imports: [
    CommonModule,
    TopNavigationComponent,
    CardModule,
    FieldsetModule,
    TagModule,
    ProgressSpinnerModule,
    SkeletonModule
  ],
  templateUrl: './order-detail.component.html',
  styleUrl: './order-detail.component.scss'
})
export class OrderDetailComponent implements OnInit {
  private route = inject(ActivatedRoute);
  private ordersService = inject(OrdersService);

  orderDetail = signal<OrderDetail | undefined>(undefined);
  loading = signal(false);

  ngOnInit(): void {
    this.getOrderDetail();
  }

  getOrderDetail(): void {
    this.loading.set(true);
    const id = this.route.snapshot.queryParamMap.get('id');
    if (id) {
      this.ordersService.getOrderDetailById(id).subscribe({
        next: (response) => {
          this.orderDetail.set(response);
          this.loading.set(false);
        },
        error: () => {
          this.loading.set(false);
        }
      });
    }
  }
}
