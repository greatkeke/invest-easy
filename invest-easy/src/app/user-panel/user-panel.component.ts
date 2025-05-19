import { Component, EventEmitter, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ButtonModule } from 'primeng/button';

@Component({
  selector: 'app-user-panel',
  templateUrl: './user-panel.component.html',
  styleUrl: './user-panel.component.scss',
  standalone: true,
  imports: [
    CommonModule,
    ButtonModule
  ]
})
export class UserPanelComponent {
  now: Date = new Date();
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

  @Output() panelClosed = new EventEmitter<void>();

  closePanel() {
    this.panelClosed.emit();
  }
}
