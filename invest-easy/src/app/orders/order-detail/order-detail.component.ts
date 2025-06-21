import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { OrdersService, OrderDetail } from '../../shared/api-services/orders.service';
import { TopNavigationComponent } from '../../shared/top-navigation/top-navigation.component';
import { CardModule } from 'primeng/card';
import { FieldsetModule } from 'primeng/fieldset';
import { TagModule } from 'primeng/tag';
import { ProgressSpinnerModule } from 'primeng/progressspinner';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-orders-detail',
  imports: [
    CommonModule,
    TopNavigationComponent,
    CardModule,
    FieldsetModule,
    TagModule,
    ProgressSpinnerModule
  ],
  templateUrl: './order-detail.component.html',
  styleUrl: './order-detail.component.scss'
})
export class OrderDetailComponent implements OnInit {
  orderDetail?: OrderDetail;
  loading = false;

  constructor(
    private route: ActivatedRoute,
    private ordersService: OrdersService
  ) { }

  ngOnInit(): void {
    this.getOrderDetail();
  }

  getOrderDetail(): void {
    this.loading = true;
    const id = this.route.snapshot.queryParamMap.get('id');
    if (id) {
      this.ordersService.getOrderDetailById(id).subscribe({
        next: (response) => {
          this.orderDetail = response;
          this.loading = false;
        },
        error: () => {
          this.loading = false;
        }
      });
    }
  }
}
