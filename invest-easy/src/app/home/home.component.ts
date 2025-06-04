import { Component, OnInit } from '@angular/core';
import { ButtonModule } from 'primeng/button';
import { CardModule } from 'primeng/card';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { HeaderComponent } from '../shared/header/header.component';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [ButtonModule, CardModule, CommonModule, HeaderComponent],
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
  showPromotions = true;
  promotions = [
    {
      title: 'Welcome Bonus',
      description: 'Receive ¥100 investment credit upon signup',
      visible: true
    }
  ];

  showBalance = true;
  account = { id: '190108', balance: 365013.73, currency: 'HKD' };

  toggleBalanceVisibility() {
    this.showBalance = !this.showBalance;
  }

  constructor(
    private router: Router
  ) { }

  ngOnInit() {

  }

  closePromotion(index: number) {
    this.promotions[index].visible = false;
  }

  navigateTo(route: string) {
    this.router.navigate([route]);
  }

  navigateToAd(adType: string) {
    this.router.navigate(['/advertisement', { adType }]);
  }
}
