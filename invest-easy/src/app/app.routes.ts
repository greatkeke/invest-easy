import { Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { GeneralSettingsComponent } from './user-panel/general-settings/general-settings.component';
import { HomeComponent } from './home/home.component';
import { MarketComponent } from './market/market.component';
import { NewsComponent } from './news/news.component';
import { TradeComponent } from './trade/trade.component';
import { TransferComponent } from './transfer/transfer.component';
import { AssetDetailComponent } from './asset-detail/asset-detail.component';
import { TradeStocksComponent } from './trade/trade-stocks.component';
import { LayoutComponent } from './shared/layout/layout.component';
import { ExchangeComponent } from './exchange/exchange.component';
import { ContactDetailComponent } from './contact-detail/contact-detail.component';
import { InstrumentDetailComponent } from './instrument-detail/instrument-detail.component';
import { UserPanelComponent } from './user-panel/user-panel.component';
import { AuthGuard } from './shared/auth.guard';
import { AdvertisementComponent } from './advertisement/advertisement.component';

export const routes: Routes = [
  { path: 'login', component: LoginComponent },
  {
    path: '',
    component: LayoutComponent,
    children: [
      {
        path: 'home',
        component: HomeComponent,
        canActivate: [AuthGuard]
      },
      {
        path: 'market',
        component: MarketComponent,
        canActivate: [AuthGuard]
      },
      {
        path: 'news',
        component: NewsComponent,
        canActivate: [AuthGuard]
      },
      {
        path: 'trade',
        component: TradeComponent,
        canActivate: [AuthGuard]
      },
      { path: '', redirectTo: '/home', pathMatch: 'full' }
    ]
  },
  {
    path: 'user-center',
    component: UserPanelComponent,
    canActivate: [AuthGuard]
  },
  {
    path: 'trade-stocks',
    component: TradeStocksComponent,
    canActivate: [AuthGuard]
  },
  {
    path: 'asset-detail',
    component: AssetDetailComponent,
    canActivate: [AuthGuard]
  },
  {
    path: 'transfer/:tab',
    component: TransferComponent,
    canActivate: [AuthGuard]
  },
  {
    path: 'transfer',
    component: TransferComponent,
    canActivate: [AuthGuard]
  },
  {
    path: 'exchange',
    component: ExchangeComponent,
    canActivate: [AuthGuard]
  },
  {
    path: 'instrument/:symbol',
    component: InstrumentDetailComponent,
    canActivate: [AuthGuard]
  },
  {
    path: 'contact-detail',
    component: ContactDetailComponent,
    canActivate: [AuthGuard]
  },
  {
    path: 'advertisement',
    component: AdvertisementComponent,
    canActivate: [AuthGuard]
  },
  {
    path: 'general-settings',
    component: GeneralSettingsComponent,
    canActivate: [AuthGuard]
  }
];
