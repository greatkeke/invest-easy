import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-user-panel',
  templateUrl: './user-panel.component.html',
  styleUrl: './user-panel.component.scss',
  standalone: true,
  imports: [
    CommonModule
  ]
})
export class UserPanelComponent {
  menuItems = [
    { label: 'General' },
    { label: 'Security' },
    { label: 'Pay and transfer' },
    { label: 'Contact details' },
    { label: 'Communication preferences' },
    { label: 'App permissions' },
    { label: 'Investment' },
    { label: 'Open Banking consent' },
    { label: 'Activity log' }
  ];

  closePanel() {
    // Implementation to close the panel would go here
    // This could be handled by a parent component or service
    console.log('Close panel clicked');
  }
}
