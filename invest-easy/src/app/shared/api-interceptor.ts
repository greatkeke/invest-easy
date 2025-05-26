import { HttpInterceptorFn } from '@angular/common/http';
import { environment } from '../../environments/environment';

export const apiInterceptor: HttpInterceptorFn = (req, next) => {
  // Skip if URL is already absolute
  if (req.url.startsWith('http')) {
    return next(req);
  }

  // Prepend base API URL for relative paths
  const apiReq = req.clone({
    url: `${environment.apiBaseUrl}/${req.url}`
  });

  return next(apiReq);
};
