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
  private auth_at?: Date;
  constructor(@Inject(PLATFORM_ID) private platformId: Object, private http: HttpClient) { }

  async isAuthenticated(): Promise<boolean> {
    if (this.auth_at) {
      if ((new Date().getTime() - this.auth_at.getTime()) < 60 * 10 * 1000) {
        return true;
      }
    }
    if (isPlatformBrowser(this.platformId)) {
      if (!!!localStorage.getItem('access_token')) {
        return false;
      } else {
        try {
          await lastValueFrom(this.http.get('/users/me'));
          this.auth_at = new Date();
          return true;
        } catch (error) {
          return false;
        }
      }
    }
    return false;
  }
}
function isAuthenticated() {
  throw new Error('Function not implemented.');
}

