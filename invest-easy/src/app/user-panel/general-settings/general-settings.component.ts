import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { TopNavigationComponent } from '../../shared/top-navigation/top-navigation.component';

interface DefinedItem {
  Id: number;
  DefinedAttributeId: number;
  DefinedAttributeName: string;
  DefinedAttributeValue: any;
  DefinedAttributeType: 'text' | 'number' | 'boolean' | 'email' | 'phone' | 'address' | 'select';
  DefinedItemEditable: boolean;
}

@Component({
  selector: 'app-general-settings',
  imports: [CommonModule, ReactiveFormsModule, TopNavigationComponent],
  templateUrl: './general-settings.component.html',
  styleUrl: './general-settings.component.scss'
})
export class GeneralSettingsComponent {
  @Input() items: DefinedItem[] = [
    {
      Id: 1,
      DefinedAttributeId: 101,
      DefinedAttributeName: 'email',
      DefinedAttributeValue: 'user@example.com',
      DefinedAttributeType: 'email',
      DefinedItemEditable: true
    },
    {
      Id: 2,
      DefinedAttributeId: 102,
      DefinedAttributeName: 'phone',
      DefinedAttributeValue: '1234567890',
      DefinedAttributeType: 'phone',
      DefinedItemEditable: false
    },
    {
      Id: 3,
      DefinedAttributeId: 103,
      DefinedAttributeName: 'notifications',
      DefinedAttributeValue: true,
      DefinedAttributeType: 'boolean',
      DefinedItemEditable: true
    }
  ];
  form: FormGroup;

  constructor(private fb: FormBuilder) {
    this.form = this.fb.group({});
  }

  ngOnInit() {
    this.createForm();
  }

  createForm() {
    const formGroup: any = {};
    this.items.forEach(item => {
      formGroup[item.DefinedAttributeName] = [
        { value: item.DefinedAttributeValue, disabled: !item.DefinedItemEditable },
        this.getValidators(item.DefinedAttributeType)
      ];
    });
    this.form = this.fb.group(formGroup);
  }

  getValidators(type: string) {
    switch(type) {
      case 'email':
        return [Validators.email];
      case 'number':
        return [Validators.pattern(/^[0-9]+$/)];
      default:
        return [];
    }
  }
}
