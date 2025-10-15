import { Component, inject, signal, WritableSignal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ButtonModule } from 'primeng/button';
import { TableModule } from 'primeng/table';
import { AccordionModule } from 'primeng/accordion';
import { TopNavigationComponent } from '../shared/top-navigation/top-navigation.component';
import { HistoryComponent } from '../history/history.component';
import { ProgressSpinnerModule } from 'primeng/progressspinner';
import { AccountBalance, AccountsService } from '../shared/api-services/accounts.service';
import { SkeletonModule } from 'primeng/skeleton';

@Component({
  selector: 'app-asset-detail',
  standalone: true,
  imports: [CommonModule, ButtonModule, TableModule, TopNavigationComponent, HistoryComponent, ProgressSpinnerModule, AccordionModule, SkeletonModule],
  templateUrl: './asset-detail.component.html',
  styleUrl: './asset-detail.component.scss'
})
export class AssetDetailComponent {
  private accountsService = inject(AccountsService);

  isLoading = signal(false);
  accountBalances: WritableSignal<AccountBalance[]> = signal([]);
  expand_id = signal("");

  goBack() {

  }


  async ngOnInit(): Promise<void> {
    await this.loadAccountBalances();
    const balances = this.accountBalances();
    if (balances.length > 0) {
      this.expand_id.set(balances[0].id);
    }
  }

  async loadAccountBalances(): Promise<void> {
    this.isLoading.set(true);
    try {
      const balances = await this.accountsService.fetchAccountBalances();
      this.accountBalances.set(balances);
    } catch (error) {
      console.error('Failed to load account balances:', error);
    } finally {
      this.isLoading.set(false);
    }
  }

  refreshData() {
    console.log('refresh data....');
  }
}
