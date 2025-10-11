import { Component, inject, input, output } from '@angular/core';
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
  isLoading = false;
  readonly back = output<void>();
  readonly refresh = output<void>();

  refreshData() {
    this.isLoading = true;
    // Simulate API call
    setTimeout(() => {
      this.isLoading = false;
    }, 1000);
    // TODO: The 'emit' function requires a mandatory void argument
    this.refresh.emit();
  }


  goBack() {
    this.location.back();
  }
}
