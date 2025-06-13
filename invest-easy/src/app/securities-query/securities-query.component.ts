import { Component, EventEmitter, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { InputTextModule } from 'primeng/inputtext';
import { ButtonModule } from 'primeng/button';
import { ListboxModule } from 'primeng/listbox';
import { IconFieldModule } from 'primeng/iconfield';
import { InputIconModule } from 'primeng/inputicon';
import { MarketService } from '../shared/api-services/market.service';

@Component({
  selector: 'app-securities-query',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    InputTextModule,
    ButtonModule,
    ListboxModule,
    IconFieldModule,
    InputIconModule
  ],
  templateUrl: './securities-query.component.html',
  styleUrls: ['./securities-query.component.scss']
})
export class SecuritiesQueryComponent {
  searchQuery = '';
  searchResults: any[] = [];
  loading = false;

  @Output() resultSelected = new EventEmitter<string>();

  constructor(private marketService: MarketService) { }

  onSearch(): void {
    if (!this.searchQuery.trim()) {
      this.searchResults = [];
      return;
    }

    this.loading = true;
    this.marketService.searchSecurities(this.searchQuery.trim()).subscribe({
      next: (response: {code: string, name: string}[]) => {
        this.searchResults = response.map((item: any) => ({
          code: item.code,
          name: item.name
        }));
        this.loading = false;
      },
      error: () => {
        this.loading = false;
      }
    });
  }

  clearSearch(): void {
    this.searchQuery = '';
    this.searchResults = [];
  }

  selectResult(code: string): void {
    this.resultSelected.emit(code);
  }
}
