import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CommonModule, Location } from '@angular/common';
import { ButtonModule } from 'primeng/button';


@Component({
  selector: 'app-top-navigation',
  templateUrl: './top-navigation.component.html',
  imports: [CommonModule, ButtonModule],
  styles: []
})
export class TopNavigationComponent {
  @Input() title = '';
  isLoading = false;
  @Output() back = new EventEmitter<void>();
  @Output() refresh = new EventEmitter<void>();

  constructor(private location: Location) { }

  refreshData() {
    this.isLoading = true;
    // Simulate API call
    setTimeout(() => {
      this.isLoading = false;
    }, 1000);
    this.refresh.emit();
  }


  goBack() {
    this.location.back();
  }
}
