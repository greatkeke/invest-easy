import { Component, OnInit, HostListener, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HeaderComponent } from '../shared/header/header.component';
import { NewsItem, NewsService } from '../shared/api-services/news.service';
import { SkeletonModule } from 'primeng/skeleton';

@Component({
  selector: 'app-news',
  standalone: true,
  imports: [CommonModule, HeaderComponent, SkeletonModule],
  templateUrl: './news.component.html',
  styleUrls: ['./news.component.scss']
})
export class NewsComponent implements OnInit {
  private newsService = inject(NewsService);

  marketNews = signal<NewsItem[]>([]);
  currentPage = signal(1);
  isLoading = signal(false);
  hasMore = signal(true);

  async ngOnInit() {
    window.addEventListener('scroll', this.scrolling, true)
    await this.loadNews();
  }

  async loadNews() {
    if (this.isLoading() || !this.hasMore()) return;

    this.isLoading.set(true);
    try {
      const newNews = await this.newsService.getMarketNews(this.currentPage());
      if (newNews.length === 0) {
        this.hasMore.set(false);
      } else {
        this.marketNews.update(currentNews => [...currentNews, ...newNews]);
        this.currentPage.update(page => page + 1);
      }
    } finally {
      this.isLoading.set(false);
    }
  }

  scrolling = async (s: any) => {
    let st = s.target.scrollingElement.scrollTop;
    let sh = s.target.scrollingElement.scrollHeight;
    let oh = s.target.scrollingElement.offsetHeight;
    if (sh <= (st + oh + 100)) {
      await this.loadNews();
    }
  }
}
