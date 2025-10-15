import { Component, OnInit, inject, signal, WritableSignal } from '@angular/core';
import { MessageService } from 'primeng/api';
import { ActivatedRoute, Router } from '@angular/router';
import { ButtonModule } from 'primeng/button';
import { CardModule } from 'primeng/card';
import { TopNavigationComponent } from '../shared/top-navigation/top-navigation.component';

import { ToastModule } from 'primeng/toast';

@Component({
  selector: 'app-instrument-detail',
  templateUrl: './instrument-detail.component.html',
  styleUrls: ['./instrument-detail.component.scss'],
  imports: [ButtonModule, CardModule, TopNavigationComponent, ToastModule],
  providers: [MessageService]
})
export class InstrumentDetailComponent implements OnInit {
  private route = inject(ActivatedRoute);
  private messageService = inject(MessageService);
  private router = inject(Router);

  instrument = signal<any>(null);
  loading = signal(true);
  isFavorite = signal(false);

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      const symbol = params['symbol'];
      this.fetchInstrumentDetails(symbol);
    });
  }

  navigateTo(target: string) {
    this.router.navigate([target]);
  }

  fetchInstrumentDetails(symbol: string): void {
    this.loading.set(true);
    // Mock data
    this.instrument.set({
      symbol: symbol,
      name: `${symbol} Company`,
      price: Math.random() * 100 + 50,
      change: (Math.random() * 10 - 5).toFixed(2),
      volume: Math.floor(Math.random() * 1000000),
      description: `This is a mock description for ${symbol}. The company operates in the financial sector and has shown consistent growth.`
    });
    this.loading.set(false);
  }

  toggleFavorite(): void {
    this.isFavorite.update(fav => !fav);
    this.messageService.add({
      severity: 'success',
      summary: this.isFavorite() ? 'Added to favorites' : 'Removed from favorites',
      detail: this.isFavorite() ? 'This instrument has been added to your collection' : 'This instrument has been removed from your collection'
    });
  }

  setPriceAlert(): void {
    this.messageService.add({
      severity: 'info',
      summary: 'Price alert set',
      detail: 'You will be notified when the price changes significantly'
    });
  }

  async shareLink(): Promise<void> {
    const url = window.location.href;
    const title = 'Check this instrument';
    
    try {
      if (navigator.share) {
        await navigator.share({
          title: title,
          url: url
        });
      } else {
        await navigator.clipboard.writeText(url);
        this.messageService.add({
          severity: 'success',
          summary: 'Link copied',
          detail: 'The link has been copied to your clipboard'
        });
      }
    } catch (err) {
      this.messageService.add({
        severity: 'error',
        summary: 'Error sharing',
        detail: 'Could not share the link'
      });
    }
  }
}
