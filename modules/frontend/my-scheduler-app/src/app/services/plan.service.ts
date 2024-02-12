import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { StaffAccountService } from './staffAccount.service';

@Injectable()
export class PlansService {

    schedule_list: any;
    constructor(private http: HttpClient ,   public staffAccountService: StaffAccountService) {}


    getPlans() {
        const user = JSON.parse(sessionStorage.getItem('user') || '{}');
        const token = user.access_token;

        const headers = new HttpHeaders({
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          });
        return this.http.get('http://127.0.0.1:5000/v1/plans', {headers});
    }

}

