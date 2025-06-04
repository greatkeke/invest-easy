import { Component, Input, SimpleChanges } from '@angular/core';
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
  @Input() RecordChanges: any;
  
  ngOnChanges(changes: SimpleChanges) {
    if (!changes['RecordChanges'].firstChange) {
      this.loadRecords();
    }
  }
  
  records: Record[] = [];
  isInit = false;
  isLoading = false;
  allRecordsLoaded = false;
  currentPage = 0;
  pageSize = 3;

  constructor(private http: HttpClient) {
  }

  ngOnInit(): void {
    this.loadRecords();
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
          // Merge and deduplicate records
          const mergedRecords = [...this.records, ...newRecords];
          const uniqueRecords = mergedRecords.filter((record, index, self) =>
            index === self.findIndex((r) => r.id === record.id)
          );
          // Sort by created_at descending
          this.records = uniqueRecords.sort((a, b) => 
            new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
          );
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
