import { Component, Input, ViewChild } from '@angular/core';
import { ButtonModule } from 'primeng/button';
import { CommonModule, NgStyle } from '@angular/common';
import { Router } from '@angular/router';
import { UserPanelComponent } from '../user-panel/user-panel.component';
import { DrawerModule } from 'primeng/drawer';
import { NotificationCenterComponent } from '../notification-center/notification-center.component';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [ButtonModule, CommonModule, UserPanelComponent, DrawerModule, NotificationCenterComponent, NgStyle],
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent {
  @ViewChild(NotificationCenterComponent) notificationCenter!: NotificationCenterComponent;
  @Input() title = 'HSBC'; // Default value
  @Input() bg_img = 'financial-regulation-header.jpg';
  displayUserPanel = false;

  constructor(
    private router: Router,
  ) { }

  goToNotifications() {
    // Show notification dialog
    this.notificationCenter.showDialog();
  }

  toggleUserPanel() {
    this.displayUserPanel = true;
  }
}
