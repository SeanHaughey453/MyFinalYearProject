import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { StaffAccountService } from './staffAccount.service';

@Injectable()
export class CreditsService {

    schedule_list: any;
    constructor(private http: HttpClient ,   public staffAccountService: StaffAccountService) {}


    getCredits() {
        const user = JSON.parse(sessionStorage.getItem('user') || '{}');
        const token = user.access_token;

        const headers = new HttpHeaders({
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          });
        return this.http.get('http://127.0.0.1:5000/v1/credits/active', {headers});
    }

    postCredit(creditForm: any){
        const creditFormJson = JSON.stringify(creditForm);
        console.log('creditFormJson', creditFormJson)
        const user = JSON.parse(sessionStorage.getItem('user') || '{}');
        const token = user.access_token;
        console.log('token', token)

        const headers = new HttpHeaders({
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          });

        return this.http.post('http://127.0.0.1:5000/v1/credit', creditFormJson,{headers});
    }

    giveClientCredit(creditForm: any){
        const user = JSON.parse(sessionStorage.getItem('user') || '{}');
        const token = user.access_token;
  
        const headers = new HttpHeaders({
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          });
        return this.http.patch('http://127.0.0.1:5000/v1/credits/add/'+ creditForm.clientID+'/token/'+ creditForm.creditID, {},{headers});
      }

}

