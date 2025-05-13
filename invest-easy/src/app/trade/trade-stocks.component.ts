import { Component } from '@angular/core';
import { TopNavigationComponent } from '../shared/top-navigation/top-navigation.component';
import { CommonModule } from '@angular/common';
import { ButtonModule } from 'primeng/button';
import { Router } from '@angular/router';
import { ChartModule } from 'primeng/chart';
import { DropdownModule } from 'primeng/dropdown';
import { InputNumberModule } from 'primeng/inputnumber';
import { CalendarModule } from 'primeng/calendar';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-trade-stocks',
  standalone: true,
  imports: [
    CommonModule,
    ButtonModule,
    ChartModule,
    DropdownModule,
    InputNumberModule,
    CalendarModule,
    FormsModule,
    TopNavigationComponent
  ],
  templateUrl: './trade-stocks.component.html',
  styleUrls: ['./trade-stocks.component.scss']
})
export class TradeStocksComponent {
  constructor(private router: Router) {}

  // Chart data
  chartData = {
    labels: ['9:30', '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00', '13:30', '14:00', '14:30', '15:00', '15:30', '16:00'],
    datasets: [
      {
        label: 'Price',
        data: [150, 152, 151, 153, 154, 155, 156, 155, 156, 157, 158, 159, 160, 161],
        borderColor: '#4CAF50',
        tension: 0.4
      }
    ]
  };

  // Trading info
  tradingInfo = [
    { label: 'Open', value: '150.00' },
    { label: 'Prev. close', value: '149.50' },
    { label: 'Day low', value: '149.80' },
    { label: 'Day high', value: '161.20' },
    { label: '52 wk low', value: '120.50' },
    { label: '52 wk high', value: '175.30' },
    { label: 'Turnover', value: '1.2M' },
    { label: 'Currency', value: 'USD' },
    { label: 'P/E ratio', value: '25.4' },
    { label: 'Market cap', value: '2.5T' },
    { label: 'Lot size', value: '100' },
    { label: 'Spread', value: '0.10' },
    { label: 'Div yield', value: '0.7%' },
    { label: 'Volume', value: '15.4M' },
    { label: 'CAS eligible', value: 'Yes' },
    { label: 'POS eligible', value: 'No' }
  ];

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
}
