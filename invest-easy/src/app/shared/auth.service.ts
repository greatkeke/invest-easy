import { Injectable } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { PLATFORM_ID } from '@angular/core';
import { Inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { lastValueFrom, Observable, of } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  constructor(@Inject(PLATFORM_ID) private platformId: Object, private http: HttpClient) { }

  async isAuthenticated(): Promise<boolean> {
    if (isPlatformBrowser(this.platformId)) {
      if (!!!localStorage.getItem('access_token')) {
        return false;
      } else {
        try {
          await lastValueFrom(this.http.get('/users/me'));
          return true;
        } catch (error) {
          return false;
        }
      }
    }
    return false;
  }
}
