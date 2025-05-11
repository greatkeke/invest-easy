import { Component, Input } from '@angular/core';
import { ButtonModule } from 'primeng/button';
import { DialogModule } from 'primeng/dialog';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { UserPanelComponent } from '../user-panel/user-panel.component';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [ButtonModule, DialogModule, CommonModule,UserPanelComponent],
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent {
  @Input() title = 'HSBC'; // Default value
  displayUserPanel = false;

  constructor(
    private router: Router,
  ) {}

  goToNotifications() {
    // Temporary implementation until notifications page is created
    alert('Notifications page is coming soon!');
    // this.router.navigate(['/notifications']);
  }

  toggleUserPanel() {
    this.displayUserPanel = true;
  }
}
