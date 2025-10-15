import { Component, SimpleChanges, inject, input, signal, WritableSignal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ButtonModule } from 'primeng/button';
import { ProgressBarModule } from 'primeng/progressbar';
import { HttpClient } from '@angular/common/http';
import { BalanceType } from '../shared/models/balance-types';

interface Record {
  id: string;
  ccy: string;
  created_at: Date;
  type: BalanceType;
  amount: number;
  balanceId: string;
  account_name: string;
}

@Component({
  selector: 'app-history',
  standalone: true,
  imports: [CommonModule, ButtonModule, ProgressBarModule],
  templateUrl: './history.component.html',
  styleUrl: './history.component.scss'
})

export class HistoryComponent {
  private http = inject(HttpClient);

  BalanceType = BalanceType;
  readonly RecordChanges = input<any>();
  
  ngOnChanges(changes: SimpleChanges) {
    if (!changes['RecordChanges'].firstChange) {
      this.loadRecords();
    }
  }
  
  records: WritableSignal<Record[]> = signal([]);
  isInit = signal(false);
  isLoading = signal(false);
  allRecordsLoaded = signal(false);
  currentPage = signal(0);
  pageSize = 3;

  ngOnInit(): void {
    this.loadRecords();
  }

  loadMore() {
    if (this.allRecordsLoaded() || this.isLoading()) return;
    this.currentPage.update(page => page + 1);
    this.loadRecords();
  }

  loadRecords() {
    this.isLoading.set(true);
    this.http.get(`/balance/transfer/records?pageSize=${this.pageSize}&pageIndex=${this.currentPage()}`)
      .subscribe({
        next: (response: any) => {
          const newRecords = response.records;
          // Merge and deduplicate records
          const currentRecords = this.records();
          const mergedRecords = [...currentRecords, ...newRecords];
          const uniqueRecords = mergedRecords.filter((record, index, self) =>
            index === self.findIndex((r) => r.id === record.id)
          );
          // Sort by created_at descending
          this.records.set(uniqueRecords.sort((a, b) => 
            new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
          ));
          this.isLoading.set(false);

          if (newRecords.length < this.pageSize) {
            this.allRecordsLoaded.set(true);
          }
        },
        error: () => {
          this.isLoading.set(false);
        }
      });
  }
}
