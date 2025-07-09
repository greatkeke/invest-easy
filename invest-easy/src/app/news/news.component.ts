import { Component, OnInit, HostListener } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HeaderComponent } from '../shared/header/header.component';
import { NewsItem, NewsService } from '../shared/api-services/news.service';

@Component({
  selector: 'app-news',
  standalone: true,
  imports: [CommonModule, HeaderComponent],
  templateUrl: './news.component.html',
  styleUrls: ['./news.component.scss']
})
export class NewsComponent implements OnInit {
  marketNews: NewsItem[] = [];
  currentPage = 1;
  isLoading = false;
  hasMore = true;

  constructor(private newsService: NewsService) { }

  async ngOnInit() {
    window.addEventListener('scroll', this.scrolling, true)
    await this.loadNews();
  }

  async loadNews() {
    if (this.isLoading || !this.hasMore) return;

    this.isLoading = true;
    try {
      const newNews = await this.newsService.getMarketNews(this.currentPage);
      if (newNews.length === 0) {
        this.hasMore = false;
      } else {
        this.marketNews = [...this.marketNews, ...newNews];
        this.currentPage++;
      }
    } finally {
      this.isLoading = false;
    }
  }

  scrolling = async (s: any) => {
    let st = s.target.scrollTop;
    let sh = s.target.scrollHeight;
    let oh = s.target.offsetHeight;
    if (sh <= (st + oh + 100)) {
      await this.loadNews();
    }
  }
}
