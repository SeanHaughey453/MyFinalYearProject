import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { StaffAccountService } from './staffAccount.service';
import { switchMap, take, throwError } from 'rxjs';

@Injectable()
export class PlansService {

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

    postPlan(planForm: any){
        const planFormJson = JSON.stringify(planForm);
        console.log('planFormJson', planFormJson)
        const user = JSON.parse(sessionStorage.getItem('user') || '{}');
        const token = user.access_token;
        console.log('token', token)

        const headers = new HttpHeaders({
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          });

        return this.http.post('http://127.0.0.1:5000/v1/plan', planFormJson,{headers});
    }
    
    deletePlan(removePlanId: string){
      const user = JSON.parse(sessionStorage.getItem('user') || '{}');
      const token = user.access_token;
    
      const headers = new HttpHeaders({
            'Content-Type': 'application/json',
              'Authorization': `Bearer ${token}`,
      });
      return this.http.delete('http://127.0.0.1:5000/v1/plan/'+ removePlanId, {headers});
    }

    giveClientPlan(planForm: any){
      const user = JSON.parse(sessionStorage.getItem('user') || '{}');
      const token = user.access_token;

      const headers = new HttpHeaders({
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        });
      return this.http.patch('http://127.0.0.1:5000/v1/plans/add/'+ planForm.clientID+'/planid/'+ planForm.planID, {},{headers});
    }

}

