import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { catchError, finalize, tap } from 'rxjs/operators';
import { environment } from '../../environments/environment';
import { InterceptorSkipHeader } from './api-interceptor';
import { firstValueFrom, of, throwError } from 'rxjs';

@Injectable({
    providedIn: 'root'
})
export class ConfigService {
    public config: any = { apiBaseUrl: "/" };

    get apiBaseUrl(): string {
        return this.config?.apiBaseUrl;
    }
}
