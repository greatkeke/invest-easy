import { Component, EventEmitter, Output } from '@angular/core';
import { CommonModule, Location } from '@angular/common';
import { ButtonModule } from 'primeng/button';
import { Router } from '@angular/router';

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

  constructor(private router: Router, private location: Location) {
  }

  closePanel() {
    this.panelClosed.emit();
    this.location.back();
  }

  navigateTo(target: string) {
    this.router.navigate([target]);
  }
}
