import { Component, Input } from '@angular/core';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatDialog } from '@angular/material/dialog';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { UserPanelComponent } from '../user-panel/user-panel.component';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [MatButtonModule, MatIconModule, CommonModule],
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent {
  @Input() title = 'HSBC'; // Default value
  constructor(
    private router: Router,
    private dialog: MatDialog
  ) {}

  goToNotifications() {
    // Temporary implementation until notifications page is created
    alert('Notifications page is coming soon!');
    // this.router.navigate(['/notifications']);
  }

  toggleUserPanel() {
    this.dialog.open(UserPanelComponent, {
      position: { bottom: '0' },
      width: '100%',
      panelClass: 'user-panel-dialog'
    });
  }
}
