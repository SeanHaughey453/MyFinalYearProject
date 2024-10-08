import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, map } from 'rxjs';
import { User } from '.././user/user';



@Injectable({
  providedIn: 'root'
})
export class AccountService {
  baseUrl = 'http://localhost:5000/v1/';
  private currentUserSource = new BehaviorSubject<User | null>(null);
  currentUser$ = this.currentUserSource.asObservable();

  constructor(private http: HttpClient) {
    const userJson = sessionStorage.getItem('user');
    if (userJson) {
      const user = JSON.parse(userJson);
      this.currentUserSource.next(user);
    }
   }

  login(loginUser: any) {
    const loginJson = JSON.stringify(loginUser);//convert to json
    console.log(loginJson)
    const headers = new HttpHeaders().set('Content-Type', 'application/json');

    return this.http.post<User>(this.baseUrl + 'login', loginJson,{headers}).pipe(
      map((response: User) => {
        const user = response;
        if (user) {
          this.setCurrentUser(user);
        }
      })
    )
  }

  register(newUser: any) {
    const newUserJson = JSON.stringify(newUser);//convert to json
    console.log(newUserJson)
    const headers = new HttpHeaders().set('Content-Type', 'application/json');

    let postData = new FormData();
        postData.append("firstName", newUser.firstName);
        postData.append("surtname", newUser.surname);
        postData.append("username", newUser.username);
        postData.append("password", newUser.password);
        postData.append("email", newUser.email);
        newUser.goals.forEach((goal: string | Blob, index: any) => {
          postData.append(`goals[${index}]`, goal);
        });

        return this.http.post(this.baseUrl +'signup', newUserJson, {headers});

  }

  setCurrentUser(user: User) {
    sessionStorage.setItem('user', JSON.stringify(user));
    this.currentUserSource.next(user);
  }

  logout() {
    const user = JSON.parse(sessionStorage.getItem('user') || '{}');
    const token = user.access_token;
  
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    });

    sessionStorage.removeItem('user');
    this.currentUserSource.next(null);

    this.http.get(this.baseUrl + 'logout', { headers }).subscribe({
      next: () => {
        sessionStorage.removeItem('user');
        this.currentUserSource.next(null);
      },
      error: (error) => {
        console.error('Logout error:', error);
      }}
    );
  }

  //need to make an account return
  getClients(){
    const user = JSON.parse(sessionStorage.getItem('user') || '{}');
    const token = user.access_token;
    const headers = new HttpHeaders(
      {
         'Content-Type': 'application/json',
         'Authorization': `Bearer ${token}`,
      });
    return this.http.get('http://127.0.0.1:5000/v1/get/clients', {headers});
  }

  getClientsPlans() {
    const user = JSON.parse(sessionStorage.getItem('user') || '{}');
    const token = user.access_token;

    const headers = new HttpHeaders({
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      });
    return this.http.get('http://127.0.0.1:5000/v1/plan/clients', {headers});
  }

  getClientsNumCredits() {
    const user = JSON.parse(sessionStorage.getItem('user') || '{}');
    const token = user.access_token;

    const headers = new HttpHeaders({
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      });
    return this.http.get('http://127.0.0.1:5000/v1/credits/clients', {headers});
  }

  getStaffProtected() {
    return this.http.get('http://127.0.0.1:5000/v1/get/staff/all');
  }

  getDecodedToken(token: string) {
    return JSON.parse(atob(token.split('.')[1]));
  }
}

