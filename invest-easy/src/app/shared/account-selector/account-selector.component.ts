import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Account } from '../api-services/accounts.service';
import { SelectModule } from 'primeng/select';

@Component({
  selector: 'app-account-selector',
  standalone: true,
  imports: [CommonModule, FormsModule, SelectModule],
  templateUrl: './account-selector.component.html',
  styleUrls: ['./account-selector.component.scss']
})
export class AccountSelectorComponent {
  @Input() options: Account[] = [];
  @Input() name: string = '';
  @Input() value: any;
  @Output() valueChange = new EventEmitter<Account>();

  onValueChange(selectedValue: Account) {
    this.value = selectedValue;
    this.valueChange.emit(selectedValue);
  }
}
