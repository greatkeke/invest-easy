import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ButtonModule } from 'primeng/button';
import { ProgressBarModule } from 'primeng/progressbar';
import { HttpClient } from '@angular/common/http';

interface Record {
  id: string;
  ccy: string;
  created_at: Date;
  transfer_in: boolean;
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
  records: Record[] = [];
  isInit = false;
  isLoading = false;
  allRecordsLoaded = false;
  currentPage = 0;
  pageSize = 3;

  constructor(private http: HttpClient) {
  }

  ngOnInit(): void {
    this.isInit = true;
    this.loadRecords();
    setTimeout(() => {
      this.isInit = false;
    }, 1500);
  }

  loadMore() {
    if (this.allRecordsLoaded || this.isLoading) return;
    this.currentPage++;
    this.loadRecords();
  }

  loadRecords() {
    this.isLoading = true;
    this.http.get(`/transfer/records?pageSize=${this.pageSize}&pageIndex=${this.currentPage}`)
      .subscribe({
        next: (response: any) => {
          const newRecords = response.records;
          this.records = [...this.records, ...newRecords];
          this.isLoading = false;

          if (newRecords.length < this.pageSize) {
            this.allRecordsLoaded = true;
          }
        },
        error: () => {
          this.isLoading = false;
        }
      });
  }
}
