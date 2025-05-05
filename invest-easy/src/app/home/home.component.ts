import { Component } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [MatButtonModule, MatCardModule, MatIconModule, CommonModule],
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent {
  showPromotions = true;
  promotions = [
    {
      title: 'Welcome Bonus',
      description: 'Receive ¥100 investment credit upon signup',
      visible: true
    },
    {
      title: 'Special Promotion',
      description: '50% discount on selected fund fees',
      visible: true
    },
    {
      title: 'Referral Reward',
      description: 'Both you and your friend get ¥50',
      visible: true
    }
  ];

  closePromotion(index: number) {
    this.promotions[index].visible = false;
  }
}
