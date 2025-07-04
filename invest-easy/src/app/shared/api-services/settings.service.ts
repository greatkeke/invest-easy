import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface DefinedItem {
  item_id: number;
  name: string;
  item_value: string;
  type: 'EMPTY' | 'TEXT' | 'NUMBER' | 'BOOLEAN' | 'EMAIL' | 'PHONE' | 'ADDRESS' | 'OPTIONS' | 'SINGLE';
  user_defined_value: string;
  editable: boolean;
  secret: boolean;
  note: string;
}

@Injectable({
  providedIn: 'root'
})
export class SettingsService {
  constructor(private http: HttpClient) { }

  getDefinedItems(groupName: string): Observable<DefinedItem[]> {
    return this.http.get<DefinedItem[]>(`/settings/defined-items/${groupName}`);
  }

  updateSettings(groupName: string, settings: any): Observable<boolean> {
    return this.http.put<boolean>(`/settings/${groupName}`, settings);
  }
}
