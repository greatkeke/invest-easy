import { Component, Input, ViewChild } from '@angular/core';
import { ButtonModule } from 'primeng/button';
import { CommonModule, NgStyle } from '@angular/common';
import { Router } from '@angular/router';
import { UserPanelComponent } from '../user-panel/user-panel.component';
import { NotificationCenterComponent } from '../notification-center/notification-center.component';
import { DialogModule } from 'primeng/dialog';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [ButtonModule, CommonModule, UserPanelComponent, DialogModule, NotificationCenterComponent, NgStyle],
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent {
  @Input() title = 'HSBC'; // Default value
  @Input() bg_img = 'financial-regulation-header.jpg';
  displayUserPanel = false;
  displayNotificationCenter = false;

  constructor(
    private router: Router,
  ) { }

  goToNotifications() {
    // Show notification dialog
    this.displayNotificationCenter = true;
  }

  toggleUserPanel() {
    this.displayUserPanel = !this.displayUserPanel;
  }
}
