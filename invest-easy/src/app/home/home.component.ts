import { Component, OnInit } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { MatDialog } from '@angular/material/dialog';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { NewsService } from '../news/news.service';
import { UserPanelComponent } from '../user-panel/user-panel.component';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [MatButtonModule, MatCardModule, MatIconModule, CommonModule],
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
  showPromotions = true;
  promotions = [
    {
      title: 'Welcome Bonus',
      description: 'Receive ¥100 investment credit upon signup',
      visible: true
    }
  ];

  marketNews: any[] = [];

  constructor(
    private newsService: NewsService,
    private router: Router,
    private dialog: MatDialog
  ) {}

  goToNotifications() {
    // Temporary implementation until notifications page is created
    alert('Notifications page is coming soon!');
    // this.router.navigate(['/notifications']);
  }

  toggleUserPanel() {
    this.dialog.open(UserPanelComponent, {
      position: { bottom: '0' },
      width: '100%',
      panelClass: 'user-panel-dialog'
    });
  }

  ngOnInit() {
    this.newsService.getMarketNews().subscribe({
      next: (data) => this.marketNews = data.articles || [],
      error: (err) => console.error('Failed to load news:', err)
    });

  }

  closePromotion(index: number) {
    this.promotions[index].visible = false;
  }

  navigateTo(route: string) {
    this.router.navigate([route]);
  }
}
