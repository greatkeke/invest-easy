import { Component } from '@angular/core';
import { DialogModule } from 'primeng/dialog';
import { CommonModule } from '@angular/common';
import { ButtonModule } from 'primeng/button';

@Component({
  selector: 'app-notification-center',
  standalone: true,
  imports: [DialogModule, CommonModule, ButtonModule],
  templateUrl: './notification-center.component.html',
  styleUrl: './notification-center.component.scss'
})
export class NotificationCenterComponent {
  visible = false;
  notifications = [
    { id: 1, title: 'Market Update', content: 'New market data available', read: false, date: new Date() },
    { id: 2, title: 'Account Alert', content: 'Your portfolio has been updated', read: true, date: new Date() },
    // Add more sample notifications
  ];

  showDialog() {
    this.visible = true;
  }

  onNotificationClick(notification: any) {
    notification.read = true;
    // Show notification detail - implement as needed
  }
}
