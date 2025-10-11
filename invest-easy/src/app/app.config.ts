import { ApplicationConfig, isDevMode, inject, provideAppInitializer, provideZonelessChangeDetection } from '@angular/core';
import { ConfigService } from './shared/config.service';
import { provideRouter, withInMemoryScrolling } from '@angular/router';
import { HttpClient, HttpHeaders, provideHttpClient, withFetch, withInterceptors } from '@angular/common/http';
import { apiInterceptor, InterceptorSkipHeader } from './shared/api-interceptor';

import { routes } from './app.routes';
import { provideClientHydration, withEventReplay } from '@angular/platform-browser';
import { provideServiceWorker } from '@angular/service-worker';

import { providePrimeNG } from 'primeng/config';
import Material from '@primeng/themes/material';
import { definePreset } from '@primeng/themes';
import { catchError, firstValueFrom, tap } from 'rxjs';

const appPreset = definePreset(Material, {
  semantic: {
    primary: {
      50: '{red.50}',
      100: '{red.100}',
      200: '{red.200}',
      300: '{red.300}',
      400: '{red.400}',
      500: '{red.500}',
      600: '{red.600}',
      700: '{red.700}',
      800: '{red.800}',
      900: '{red.900}',
      950: '{red.950}'
    },
    colorScheme: {
      light: {
        primary: {
          color: '{red.950}',
          contrastColor: '#ffffff',
          hoverColor: '{red.900}',
          activeColor: '{red.800}'
        },
        highlight: {
          background: '{red.950}',
          focusBackground: '{red.700}',
          color: '#ffffff',
          focusColor: '#ffffff'
        }
      },
      dark: {
        primary: {
          color: '{red.50}',
          contrastColor: '{red.950}',
          hoverColor: '{red.100}',
          activeColor: '{red.200}'
        },
        highlight: {
          background: 'rgba(250, 250, 250, .16)',
          focusBackground: 'rgba(250, 250, 250, .24)',
          color: 'rgba(255,255,255,.87)',
          focusColor: 'rgba(255,255,255,.87)'
        }
      }
    }
  }
});

export const appConfig: ApplicationConfig = {
  providers: [
    provideAppInitializer(() => {
      const http = inject(HttpClient);
      const configSvc = inject(ConfigService);
      return firstValueFrom(
        http.get('/assets/config.json', { headers: new HttpHeaders().set(InterceptorSkipHeader, 'true') })
          .pipe(
            tap((data: any) => configSvc.config.apiBaseUrl = data.API_BASE_URL),
            catchError(err => configSvc.config.apiBaseUrl = "error")
          )
      );
    }),
    provideZonelessChangeDetection(),
    provideRouter(routes, withInMemoryScrolling({scrollPositionRestoration:'enabled'})),
    provideClientHydration(withEventReplay()),
    provideHttpClient(withFetch(), withInterceptors([apiInterceptor])),
    provideServiceWorker('ngsw-worker.js', {
      enabled: !isDevMode(),
      registrationStrategy: 'registerWhenStable:30000'
    }),
    providePrimeNG({
      theme: {
        preset: appPreset
      },
      ripple: true,
    })
  ]
};
