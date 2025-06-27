import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface DefinedItem {
  name: string;
  value: any;
  type: 'TEXT' | 'NUMBER' | 'BOOLEAN' | 'EMAIL' | 'PHONE' | 'ADDRESS' | 'OPTIONS';
  editable: boolean;
  secret: boolean;
}

@Injectable({
  providedIn: 'root'
})
export class SettingsService {
  constructor(private http: HttpClient) { }

  getDefinedItems(groupName: string): Observable<DefinedItem[]> {
    return this.http.get<DefinedItem[]>(`/settings/defined-items/${groupName}`);
  }
}
