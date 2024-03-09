import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { AccountService } from './account.service';
import { switchMap, take, throwError } from 'rxjs';
import { StaffAccountService } from './staffAccount.service';

@Injectable()
export class ScheduleService {

    schedule_list: any;
    constructor(private http: HttpClient ,public accountService: AccountService,   public staffAccountService: StaffAccountService) {}


    getSchedules() {
        const user = JSON.parse(sessionStorage.getItem('user') || '{}');
        const token = user.access_token;

        const headers = new HttpHeaders({
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          });
        return this.http.get('http://127.0.0.1:5000/v1/schedules', {headers});
    }

    getAllSchedules() {
        const user = JSON.parse(sessionStorage.getItem('user') || '{}');
        const token = user.access_token;

        const headers = new HttpHeaders({
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          });
        return this.http.get('http://127.0.0.1:5000/v1/schedules/all', {headers});
    }

    getSchedule(id : any) {
        return this.http.get('http://localhost:5000/v1/schedule/' + id);     
    }

    postSchedule(){
        const user = JSON.parse(sessionStorage.getItem('user') || '{}');
        const token = user.access_token;

        const headers = new HttpHeaders({
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          });
        
          return this.http.post('http://127.0.0.1:5000/v1/schedule', {},{headers});
    }


    deleteSchedule(removeScheduleId: string){
        const user = JSON.parse(sessionStorage.getItem('user') || '{}');
        const token = user.access_token;
      
        const headers = new HttpHeaders({
              'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`,
        });
        return this.http.delete('http://127.0.0.1:5000/v1/schedule/'+ removeScheduleId, {headers});
      }
}

