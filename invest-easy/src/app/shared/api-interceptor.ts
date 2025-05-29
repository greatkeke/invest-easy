import { HttpInterceptorFn } from '@angular/common/http';
import { environment } from '../../environments/environment';

export const InterceptorSkipHeader = 'X-Skip-Interceptor';

export const apiInterceptor: HttpInterceptorFn = (req, next) => {
  // Skip if URL is already absolute
  if (req.url.startsWith('http')) {
    return next(req);
  }

  if (req.headers.has(InterceptorSkipHeader)) {
    const headers = req.headers.delete(InterceptorSkipHeader);
    return next(req.clone({ headers }));
  }

  // Prepend base API URL for relative paths
  const apiReq = req.clone({
    url: `${environment.apiBaseUrl}/${req.url}`
  });

  return next(apiReq);
};
