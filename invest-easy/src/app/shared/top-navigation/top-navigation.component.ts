import { Component, EventEmitter, Input, Output, inject } from '@angular/core';
import { Location } from '@angular/common';
import { ButtonModule } from 'primeng/button';


@Component({
  selector: 'app-top-navigation',
  templateUrl: './top-navigation.component.html',
  imports: [ButtonModule],
  styles: []
})
export class TopNavigationComponent {
  private location = inject(Location);

  @Input() title = '';
  isLoading = false;
  @Output() back = new EventEmitter<void>();
  @Output() refresh = new EventEmitter<void>();

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
