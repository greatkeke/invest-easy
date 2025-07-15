import { Component, Input, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';
import { TopNavigationComponent } from '../../shared/top-navigation/top-navigation.component';
import { InputTextModule } from 'primeng/inputtext';
import { InputNumberModule } from 'primeng/inputnumber';
import { CheckboxModule } from 'primeng/checkbox';
import { InputMaskModule } from 'primeng/inputmask';
import { SelectModule } from 'primeng/select';
import { DefinedItem, SettingsService } from '../../shared/api-services/settings.service';
import { catchError, finalize } from 'rxjs/operators';
import { of } from 'rxjs';
import { CardModule } from 'primeng/card';
import { ButtonModule } from 'primeng/button';
import { MessageService } from 'primeng/api';
import { ToastModule } from 'primeng/toast';

@Component({
  selector: 'app-general-settings',
  imports: [
    CommonModule,
    ReactiveFormsModule,
    TopNavigationComponent,
    InputTextModule,
    InputNumberModule,
    CheckboxModule,
    InputMaskModule,
    SelectModule,
    CardModule,
    ButtonModule,
    ToastModule
  ],
  templateUrl: './general-settings.component.html',
  styleUrl: './general-settings.component.scss',
  providers: [MessageService]
})
export class GeneralSettingsComponent implements OnInit {
  @Input() items: DefinedItem[] = [];
  form: FormGroup;
  groupName: string = "";
  isLoading = false;
  error: string | null = null;

  constructor(
    private fb: FormBuilder,
    private settingsService: SettingsService,
    private route: ActivatedRoute,
    private messageService: MessageService
  ) {
    this.form = this.fb.group({});
  }

  ngOnInit() {
    this.groupName = this.route.snapshot.queryParamMap.get('group') || '';
    this.isLoading = true;
    this.settingsService.getDefinedItems(this.groupName)
      .pipe(
        catchError(err => {
          this.error = 'Failed to load settings';
          return of([]);
        }),
        finalize(() => this.isLoading = false)
      )
      .subscribe(items => {
        this.items = items;
        this.createForm();
      });
  }

  createForm() {
    const formGroup: any = {};
    this.items.forEach(item => {
      let value = item.user_defined_value == null ? item.item_value : item.user_defined_value;
      if (item.type == "OPTIONS") {
        const valueJson = JSON.parse(value);
        const optionsGroup: any = {};
        Object.keys(valueJson).forEach(key => {
          optionsGroup[key] = [
            { value: valueJson[key], disabled: !item.editable }
          ];
        });
        formGroup[item.name] = this.fb.group(optionsGroup);
      }
      else {
        formGroup[item.name] = [
          { value: value, disabled: !item.editable },
          this.getValidators(item.type)
        ];
        this.form = this.fb.group(formGroup);
      }
    });
  }

  getValidators(type: string) {
    switch (type) {
      case 'EMAIL':
        return [Validators.email];
      case 'NUMBER':
        return [Validators.pattern(/^[0-9]+$/)];
      default:
        return [];
    }
  }

  fromOptions(value: any) {
    const obj = JSON.parse(value);
    return Object.keys(obj);
  }

  onSave() {
    if (this.form.invalid) return;

    this.isLoading = true;
    const settings = this.form.getRawValue();
    Object.keys(settings).forEach(key => {
      if (typeof (settings[key]) != 'string') {
        settings[key] = JSON.stringify(settings[key]);
      }
    });
    this.settingsService.updateSettings(this.groupName, settings)
      .pipe(
        catchError(err => {
          this.messageService.add({
            severity: 'error',
            summary: 'Error',
            detail: 'Failed to save settings',
            life: 3000
          });
          return of(false);
        }),
        finalize(() => this.isLoading = false)
      )
      .subscribe((success: boolean) => {
        if (success) {
          this.messageService.add({
            severity: 'success',
            summary: 'Success',
            detail: 'Settings saved successfully',
            life: 3000
          });
        }
      });
  }
}
