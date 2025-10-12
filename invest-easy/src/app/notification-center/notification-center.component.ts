import { Component, signal, computed } from '@angular/core';
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
  visible = signal(false);
  notifications = signal([
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
      content: 'Your portfolio has been updated. <a href="/trade" class="text-blue-500 hover:underline">Check now</a>', 
      read: true, 
      date: new Date(),
      expanded: false
    },
    // Add more sample notifications
  ]);

  // Computed signal for unread notifications count
  unreadCount = computed(() => 
    this.notifications().filter(notification => !notification.read).length
  );

  showDialog() {
    this.visible.set(true);
  }

  markAsRead(notification: any) {
    const updatedNotifications = this.notifications().map(n => 
      n.id === notification.id ? { ...n, read: true } : n
    );
    this.notifications.set(updatedNotifications);
  }

  toggleExpand(notification: any) {
    const updatedNotifications = this.notifications().map(n => 
      n.id === notification.id ? { ...n, expanded: !n.expanded } : n
    );
    this.notifications.set(updatedNotifications);
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
