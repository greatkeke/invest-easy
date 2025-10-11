import { Component, OnInit, inject, input } from '@angular/core';
import { ButtonModule } from 'primeng/button';
import { CommonModule, Location, NgStyle } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { DialogModule } from 'primeng/dialog';
import { NotificationCenterComponent } from '../../notification-center/notification-center.component';
import { HttpParams } from '@angular/common/http';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [ButtonModule, CommonModule, DialogModule, NotificationCenterComponent, NgStyle],
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss'],
})
export class HeaderComponent implements OnInit {
  private router = inject(Router);
  private route = inject(ActivatedRoute);
  private location = inject(Location);

  readonly title = input('Invest-Easy'); // Default value
  readonly bg_img = input('financial-regulation-header.jpg');
  displayUserPanel = false;
  displayNotificationCenter = false;

  ngOnInit() {
    this.route.queryParams.subscribe(params => {
      const ntf = params['notification'];
      if (!!ntf && ntf == "on") {
        this.displayNotificationCenter = true;
      }
      else {
        this.displayNotificationCenter = false;
      }
    })
  }

  goToNotifications() {
    this.displayNotificationCenter = true;
    this.router.navigate([], { queryParams: { notification: "on" } });
  }

  onClose() {
    const params = new HttpParams();
    this.location.replaceState(location.pathname, params.toString());
  }

  toggleUserPanel() {
    this.displayUserPanel = !this.displayUserPanel;
  }

  navigateTo(target: string) {
    this.router.navigate([target]);
  }
}
