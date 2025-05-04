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
      title: '新用户优惠',
      description: '注册即送100元投资券',
      visible: true
    },
    {
      title: '限时特惠',
      description: '部分基金手续费5折',
      visible: true
    },
    {
      title: '推荐有礼',
      description: '邀请好友各得50元',
      visible: true
    }
  ];

  closePromotion(index: number) {
    this.promotions[index].visible = false;
  }
}
