import { Component, inject, input, output, signal } from '@angular/core';
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

  readonly title = input('');
  
  // Signal-based state
  isLoading = signal(false);
  readonly back = output<void>();
  readonly refresh = output<void>();

  refreshData() {
    this.isLoading.set(true);
    // Simulate API call
    setTimeout(() => {
      this.isLoading.set(false);
    }, 1000);
    this.refresh.emit();
  }

  goBack() {
    this.location.back();
  }
}
