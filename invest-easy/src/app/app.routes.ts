import { Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { MarketComponent } from './market/market.component';
import { NewsComponent } from './news/news.component';
import { TradeComponent } from './trade/trade.component';
import { AssetDetailComponent } from './asset-detail/asset-detail.component';
import { TradeStocksComponent } from './trade/trade-stocks.component';

export const routes: Routes = [
  { path: 'home', component: HomeComponent },
  { path: 'market', component: MarketComponent },
  { path: 'news', component: NewsComponent },
  { path: 'trade', component: TradeComponent },
  { path: 'trade-stocks', component: TradeStocksComponent },
  { path: 'asset-detail', component: AssetDetailComponent },
  { path: '', redirectTo: '/home', pathMatch: 'full' }
];
