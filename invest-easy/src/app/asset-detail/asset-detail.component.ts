import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ButtonModule } from 'primeng/button';
import { TopNavigationComponent } from '../shared/top-navigation/top-navigation.component';
import { HistoryComponent } from '../history/history.component';
import { ProgressSpinnerModule } from 'primeng/progressspinner';
import { BalanceService } from '../shared/api-services/balance.service';
import { AccountBalance, AccountsService } from '../shared/api-services/accounts.service';

@Component({
  selector: 'app-asset-detail',
  standalone: true,
  imports: [CommonModule, ButtonModule, TopNavigationComponent, HistoryComponent, ProgressSpinnerModule],
  templateUrl: './asset-detail.component.html',
  styleUrl: './asset-detail.component.scss'
})
export class AssetDetailComponent {
  isLoading = false;
  accountBalances: AccountBalance[] = [];

  constructor(
    private accountsService: AccountsService
  ) { }

  goBack() {

  }


  async ngOnInit(): Promise<void> {
    await this.loadAccountBalances();
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
