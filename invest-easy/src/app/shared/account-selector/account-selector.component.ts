import { Component, Input, Output, EventEmitter, input } from '@angular/core';
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
  readonly options = input<Account[]>([]);
  readonly name = input<string>('');
  _value: any;
  @Output() valueChange = new EventEmitter<Account>();
  @Output() selectChange = new EventEmitter<Account>();

  private prevValue?: Account;

  @Input() set value(value: any) {
    this._value = value;
    this.prevValue = value;
  }

  onValueChange(selectedValue: Account) {
    this.valueChange.emit(selectedValue);
    if (selectedValue.id != this.prevValue!.id) {
      this.selectChange.emit(this.prevValue!);
    }
  }
}
