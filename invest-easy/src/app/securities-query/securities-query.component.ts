import { Component, OnInit, ElementRef, inject, input, output, viewChild } from '@angular/core';

import { FormsModule } from '@angular/forms';
import { InputTextModule } from 'primeng/inputtext';
import { ButtonModule } from 'primeng/button';
import { ListboxModule } from 'primeng/listbox';
import { IconFieldModule } from 'primeng/iconfield';
import { InputIconModule } from 'primeng/inputicon';
import { MarketService } from '../shared/api-services/market.service';
import { AutoFocusModule } from 'primeng/autofocus';
import { ToastModule } from 'primeng/toast';
import { MessageService } from 'primeng/api';

@Component({
  selector: 'app-securities-query',
  standalone: true,
  imports: [
    FormsModule,
    InputTextModule,
    ButtonModule,
    ListboxModule,
    IconFieldModule,
    InputIconModule,
    AutoFocusModule,
    ToastModule
],
  providers: [MessageService],
  templateUrl: './securities-query.component.html',
  styleUrls: ['./securities-query.component.scss']
})
export class SecuritiesQueryComponent implements OnInit {
  private marketService = inject(MarketService);
  private messageService = inject(MessageService);

  readonly autofocus = input(false);
  readonly placeholder = input('');
  readonly searchInput = viewChild.required<ElementRef>('searchInput');

  searchQuery = '';
  searchResults: any[] = [];
  instruments: any[] = [];
  loading = false;
  showLatestInstruments = false;

  readonly resultSelected = output<string>();

  onSearch(): void {
    if (!this.searchQuery.trim()) {
      this.searchResults = [];
      return;
    }
    this.loading = true;
    this.marketService.searchSecurities(this.searchQuery.trim()).subscribe({
      next: (response: { code: string, name: string }[]) => {
        this.showLatestInstruments = false;
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
    this.showLatestInstruments = this.autofocus() ? true : false;
  }

  selectResult(code: string): void {
    this.resultSelected.emit(code);
  }

  ngOnInit(): void {
    this.ShowLatestInstruments();
  }

  private ShowLatestInstruments() {
    this.marketService.getInstrumentsByUser().subscribe({
      next: (instruments) => {
        this.instruments = instruments;
        if (this.autofocus()) {
          this.showLatestInstruments = true;
        }
      },
      error: (err) => {
        console.error('Failed to load instruments', err);
      }
    });
  }

  onFocus(): void {
    this.showLatestInstruments = true;
  }

  onBlur(): void {
    if (!this.autofocus()) {
      this.showLatestInstruments = false;
    }
  }
}
