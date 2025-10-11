import { Routes } from '@angular/router';













import { AuthGuard } from './shared/auth.guard';





export const routes: Routes = [
  { path: 'login', loadComponent: () => import('./login/login.component').then(m => m.LoginComponent) },
  {
    path: '',
    loadComponent: () => import('./shared/layout/layout.component').then(m => m.LayoutComponent),
    children: [
      {
        path: 'home',
        loadComponent: () => import('./home/home.component').then(m => m.HomeComponent),
        canActivate: [AuthGuard]
      },
      {
        path: 'market',
        loadComponent: () => import('./market/market.component').then(m => m.MarketComponent),
        canActivate: [AuthGuard]
      },
      {
        path: 'news',
        loadComponent: () => import('./news/news.component').then(m => m.NewsComponent),
        canActivate: [AuthGuard]
      },
      {
        path: 'trade',
        loadComponent: () => import('./trade/trade.component').then(m => m.TradeComponent),
        canActivate: [AuthGuard]
      },
      { path: '', redirectTo: '/home', pathMatch: 'full' }
    ]
  },
  {
    path: 'user-center',
    loadComponent: () => import('./user-panel/user-panel.component').then(m => m.UserPanelComponent),
    canActivate: [AuthGuard]
  },
  {
    path: 'trade-stocks',
    loadComponent: () => import('./trade/trade-stocks.component').then(m => m.TradeStocksComponent),
    canActivate: [AuthGuard]
  },
  {
    path: 'asset-detail',
    loadComponent: () => import('./asset-detail/asset-detail.component').then(m => m.AssetDetailComponent),
    canActivate: [AuthGuard]
  },
  {
    path: 'transfer/:tab',
    loadComponent: () => import('./transfer/transfer.component').then(m => m.TransferComponent),
    canActivate: [AuthGuard]
  },
  {
    path: 'transfer',
    loadComponent: () => import('./transfer/transfer.component').then(m => m.TransferComponent),
    canActivate: [AuthGuard]
  },
  {
    path: 'exchange',
    loadComponent: () => import('./exchange/exchange.component').then(m => m.ExchangeComponent),
    canActivate: [AuthGuard]
  },
  {
    path: 'instrument/:symbol',
    loadComponent: () => import('./instrument-detail/instrument-detail.component').then(m => m.InstrumentDetailComponent),
    canActivate: [AuthGuard]
  },
  {
    path: 'contact-detail',
    loadComponent: () => import('./user-panel/contact-detail/contact-detail.component').then(m => m.ContactDetailComponent),
    canActivate: [AuthGuard]
  },
  {
    path: 'advertisement',
    loadComponent: () => import('./advertisement/advertisement.component').then(m => m.AdvertisementComponent),
    canActivate: [AuthGuard]
  },
  {
    path: 'general-settings',
    loadComponent: () => import('./user-panel/general-settings/general-settings.component').then(m => m.GeneralSettingsComponent),
    canActivate: [AuthGuard]
  },
  {
    path: 'order-detail',
    loadComponent: () => import('./orders/order-detail/order-detail.component').then(m => m.OrderDetailComponent),
    canActivate: [AuthGuard]
  },
  {
    path: 'report',
    loadComponent: () => import('./report/report.component').then(m => m.ReportComponent),
    canActivate: [AuthGuard]
  }
];
