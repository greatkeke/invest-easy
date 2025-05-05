import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class NewsService {
  private apiUrl = 'https://newsapi.org/v2/everything';

  constructor(private http: HttpClient) {}

  getMarketNews(): Observable<any> {
    const params = {
      q: 'finance OR stock OR market',
      language: 'en',
      sortBy: 'publishedAt',
      pageSize: '10',
      apiKey: environment.newsApiKey
    };
    return this.http.get(this.apiUrl, { params });
  }
}
