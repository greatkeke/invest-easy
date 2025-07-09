import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { lastValueFrom, Observable, of } from 'rxjs';

export interface NewsItem {
  title: string;
  description: string;
  author: string;
  url: string;
  image_url: string;
  published_at: string;
  source: string;
}

@Injectable({
  providedIn: 'root'
})
export class NewsService {

  constructor(private http: HttpClient) { }

  getMarketNews(page: number = 1, pageSize: number = 10): Promise<NewsItem[]> {
    return lastValueFrom(this.http.get<NewsItem[]>("news/", { params: { page: page, page_size: pageSize } }))
  }
}
