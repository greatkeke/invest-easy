import { Component } from '@angular/core';
import { ButtonModule } from 'primeng/button';
import { PanelModule } from 'primeng/panel';
import { ListboxModule } from 'primeng/listbox';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-user-panel',
  templateUrl: './user-panel.component.html',
  styleUrl: './user-panel.component.scss',
  standalone: true,
  imports: [
    ButtonModule,
    PanelModule,
    ListboxModule,
    CommonModule
  ]
})
export class UserPanelComponent {
  menuItems = [
    { label: 'Preference' },
    { label: 'eStatements' },
    { label: 'Security' },
    { label: 'Reports' },
    { label: 'Action' },
    { label: 'Performance' },
    { label: 'About' },
    { label: 'Rating' }
  ];
}
