import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NewsService } from './news.service';
import { HeaderComponent } from '../shared/header/header.component';

@Component({
  selector: 'app-news',
  standalone: true,
  imports: [CommonModule, HeaderComponent],
  templateUrl: './news.component.html',
  styleUrls: ['./news.component.scss']
})
export class NewsComponent implements OnInit {
  marketNews: any[] = [];

  constructor(private newsService: NewsService) { }

  ngOnInit() {
    this.newsService.getMarketNews().subscribe({
      next: (data) => this.marketNews = data.articles || [],
      error: (err) => console.error('Failed to load news:', err)
    });
  }
}
