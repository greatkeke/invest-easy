import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { lastValueFrom } from 'rxjs';


@Injectable({
    providedIn: 'root'
})
export class ExchangeService {
    constructor(private http: HttpClient) { }

    async exchange(fromAccountId: string, toAccountId: string, amount: number): Promise<Boolean> {
        try {
            return await lastValueFrom(
                this.http.post<boolean>('/exchange/', { from_account_id: fromAccountId, to_account_id: toAccountId, amount: amount })
            );
        } catch (error) {
            throw error;
        }
    }
}
