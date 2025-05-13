import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ButtonModule } from 'primeng/button';
import { TopNavigationComponent } from '../shared/top-navigation/top-navigation.component';

@Component({
  selector: 'app-asset-detail',
  standalone: true,
  imports: [CommonModule, ButtonModule, TopNavigationComponent],
  templateUrl: './asset-detail.component.html',
  styleUrl: './asset-detail.component.scss'
})
export class AssetDetailComponent {

  goBack() {

  }

  refreshData() {
    console.log('refresh data....')
  }


}
