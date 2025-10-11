import { Component, inject } from '@angular/core';
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

  isLoading = false;
  accountBalances: AccountBalance[] = [];
  expand_id: string = "";

  goBack() {

  }


  async ngOnInit(): Promise<void> {
    await this.loadAccountBalances();
    this.expand_id = this.accountBalances[0].id;
  }

  async loadAccountBalances(): Promise<void> {
    this.isLoading = true;
    try {
      this.accountBalances = await this.accountsService.fetchAccountBalances();
    } catch (error) {
      console.error('Failed to load account balances:', error);
    } finally {
      this.isLoading = false;
    }
  }

  refreshData() {
    console.log('refresh data....');
  }
}
