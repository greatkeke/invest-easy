import { Component, OnInit } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { HeaderComponent } from '../header/header.component';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [MatButtonModule, MatCardModule, MatIconModule, CommonModule, HeaderComponent],
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
  account = { id: '1234567890', balance: 5000.00, currency: 'HKD' };

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
}
