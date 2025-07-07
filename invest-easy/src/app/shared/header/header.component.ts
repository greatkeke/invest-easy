import { Component, Input, OnInit } from '@angular/core';
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
  @Input() title = 'Invest-Easy'; // Default value
  @Input() bg_img = 'financial-regulation-header.jpg';
  displayUserPanel = false;
  displayNotificationCenter = false;

  constructor(
    private router: Router,
    private route: ActivatedRoute,
    private location: Location
  ) { }

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
