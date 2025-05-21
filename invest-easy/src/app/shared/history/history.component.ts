import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ButtonModule } from 'primeng/button';

@Component({
  selector: 'app-history',
  standalone: true,
  imports: [CommonModule,ButtonModule],
  templateUrl: './history.component.html',
  styleUrl: './history.component.scss'
})
export class HistoryComponent {
  records = [
    { type: 'In', amount: 500, time: new Date('2025-05-15'), balance: 10500 },
    { type: 'Out', amount: 200, time: new Date('2025-05-14'), balance: 9800 },
    { type: 'In', amount: 1000, time: new Date('2025-05-10'), balance: 9000 }
  ];

  loadMore() {
    // Mock loading more records
    const newRecords = [
      { type: 'Out', amount: 150, time: new Date('2025-05-08'), balance: 8850 },
      { type: 'In', amount: 300, time: new Date('2025-05-05'), balance: 8550 },
      { type: 'Out', amount: 50, time: new Date('2025-05-01'), balance: 8500 }
    ];
    this.records = [...this.records, ...newRecords];
  }
}

