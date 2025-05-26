import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ButtonModule } from 'primeng/button';
import { TopNavigationComponent } from '../shared/top-navigation/top-navigation.component';
import { HistoryComponent } from '../shared/history/history.component';
import { ProgressSpinnerModule } from 'primeng/progressspinner';

@Component({
  selector: 'app-asset-detail',
  standalone: true,
  imports: [CommonModule, ButtonModule, TopNavigationComponent, HistoryComponent, ProgressSpinnerModule],
  templateUrl: './asset-detail.component.html',
  styleUrl: './asset-detail.component.scss'
})
export class AssetDetailComponent {
  isLoading = false;

  goBack() {

  }

  ngOnInit(): void {
    this.isLoading = true;
    // Simulate data loading
    setTimeout(() => {
      this.isLoading = false;
    }, 1500);

  }

  refreshData() {
    console.log('refresh data....');
  }
}
