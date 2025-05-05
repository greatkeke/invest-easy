import { Component, OnInit } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { NewsService } from '../news/news.service';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [MatButtonModule, MatCardModule, MatIconModule, CommonModule, HttpClientModule],
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

  marketNews: any[] = [];

  constructor(private newsService: NewsService) {}

  ngOnInit() {
    this.newsService.getMarketNews().subscribe({
      next: (data) => this.marketNews = data.articles || [],
      error: (err) => console.error('Failed to load news:', err)
    });
  }

  closePromotion(index: number) {
    this.promotions[index].visible = false;
  }
}
