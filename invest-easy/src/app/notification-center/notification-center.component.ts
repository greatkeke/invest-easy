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
    { 
      id: 1, 
      title: 'Market Update', 
      content: 'New market data available. <a href="/market" class="text-blue-500 hover:underline">View market</a> \n A new flexable market added! \n Plex is move on the screen shot.', 
      read: false, 
      date: new Date(),
      expanded: false
    },
    { 
      id: 2, 
      title: 'Account Alert', 
      content: 'Your portfolio has been updated. <a href="/portfolio" class="text-blue-500 hover:underline">Check now</a>', 
      read: true, 
      date: new Date(),
      expanded: false
    },
    // Add more sample notifications
  ];

  showDialog() {
    this.visible = true;
  }

  markAsRead(notification: any) {
    notification.read = true;
  }

  toggleExpand(notification: any) {
    notification.expanded = !notification.expanded;
  }

  onNotificationClick(notification: any) {
    this.markAsRead(notification);
    this.toggleExpand(notification);
  }

  handleLinkClick(event: Event) {
    event.stopPropagation();
    // Link handling will be done by Angular router
  }
}
