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
    CardModule
  ],
  templateUrl: './general-settings.component.html',
  styleUrl: './general-settings.component.scss'
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
    private route: ActivatedRoute
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
      formGroup[item.name] = [
        { value: item.value, disabled: !item.editable },
        this.getValidators(item.type)
      ];
    });
    this.form = this.fb.group(formGroup);
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

  getOptions(value: string) {
    return value.split(',').map(option => option.trim());
  }
}
