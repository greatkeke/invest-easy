import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { tap } from 'rxjs/operators';
import { environment } from '../../environments/environment';
import { InterceptorSkipHeader } from './api-interceptor';
import { firstValueFrom } from 'rxjs';

@Injectable({
    providedIn: 'root'
})
export class ConfigService {
    private config: any;

    constructor(private http: HttpClient) {
    }

    loadConfig() {
        return firstValueFrom(
            this.http.get('/assets/config.json', {
                headers: new HttpHeaders().set(InterceptorSkipHeader, 'true')
            })
                .pipe(
                    tap(config => {
                        this.config = config;
                        environment.apiBaseUrl = this.apiBaseUrl;
                    })
                )

        );
    }

    get apiBaseUrl(): string {
        return this.config?.API_BASE_URL;
    }
}
