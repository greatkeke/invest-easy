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
import { LayoutComponent } from './layout/layout.component';
import { ExchangeComponent } from './exchange/exchange.component';
import { ContactDetailComponent } from './contact-detail/contact-detail.component';
import { InstrumentDetailComponent } from './instrument-detail/instrument-detail.component';
import { UserPanelComponent } from './user-panel/user-panel.component';
import { AdvertisementComponent } from './shared/advertisement/advertisement.component';

export const routes: Routes = [
  { path: 'login', component: LoginComponent },
  {
    path: '',
    component: LayoutComponent,
    children: [
      { path: 'home', component: HomeComponent },
      { path: 'market', component: MarketComponent },
      { path: 'news', component: NewsComponent },
      { path: 'trade', component: TradeComponent },
      { path: '', redirectTo: '/home', pathMatch: 'full' }
    ]
  },
  { path: 'user-center', component: UserPanelComponent },
  { path: 'trade-stocks', component: TradeStocksComponent },
  { path: 'asset-detail', component: AssetDetailComponent },
  { path: 'transfer/:tab', component: TransferComponent },
  { path: 'transfer', component: TransferComponent },
  { path: 'exchange', component: ExchangeComponent },
  { path: 'instrument/:symbol', component: InstrumentDetailComponent },
  { path: 'contact-detail', component: ContactDetailComponent },
  { path: 'advertisement', component: AdvertisementComponent },
  { path: 'general-settings', component: GeneralSettingsComponent }
];
