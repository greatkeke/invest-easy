import { HttpInterceptorFn } from '@angular/common/http';
import { inject, PLATFORM_ID } from '@angular/core';
import { ConfigService } from './config.service';
import { isPlatformBrowser } from '@angular/common';

export const AUTH_TOKEN_KEY = 'access_token';

export const InterceptorSkipHeader = 'X-Skip-Interceptor';

export const apiInterceptor: HttpInterceptorFn = (req, next) => {
  const configSvc = inject(ConfigService);

  // Skip if URL is already absolute
  if (req.url.startsWith('http')) {
    return next(req);
  }

  if (req.headers.has(InterceptorSkipHeader)) {
    const headers = req.headers.delete(InterceptorSkipHeader);
    return next(req.clone({ headers }));
  }

  // Prepend base API URL for relative paths
  // Ensure clean URL concatenation without double slashes
  const baseUrl = configSvc.apiBaseUrl.endsWith('/') 
    ? configSvc.apiBaseUrl.slice(0, -1) 
    : configSvc.apiBaseUrl;
  const path = req.url.startsWith('/') 
    ? req.url.slice(1)
    : req.url;
    
  // Get token from storage (only in browser)
  const platformId = inject(PLATFORM_ID);
  const token = isPlatformBrowser(platformId) 
    ? localStorage.getItem(AUTH_TOKEN_KEY)
    : null;
  
  // Clone request with new URL and auth header
  const apiReq = req.clone({
    url: `${baseUrl}/${path}`,
    headers: token ? req.headers.set('Authorization', `Bearer ${token}`) : req.headers
  });

  return next(apiReq);
};
