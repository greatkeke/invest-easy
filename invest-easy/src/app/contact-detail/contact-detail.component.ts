import { Component } from '@angular/core';
import { ButtonModule } from 'primeng/button';
import { TopNavigationComponent } from '../shared/top-navigation/top-navigation.component';

@Component({
    selector: 'app-contact-detail',
    templateUrl: './contact-detail.component.html',
    styleUrls: ['./contact-detail.component.scss'],
    imports: [ButtonModule, TopNavigationComponent]
})
export class ContactDetailComponent {
    constructor() { }
}
