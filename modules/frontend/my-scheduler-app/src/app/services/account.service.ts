import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, map } from 'rxjs';
import { User } from '.././user/user';


@Injectable({
  providedIn: 'root'
})
export class AccountService {
  baseUrl = 'http://localhost:5000/api/v1.0/';
  private currentUserSource = new BehaviorSubject<User | null>(null);
  currentUser$ = this.currentUserSource.asObservable();

  constructor(private http: HttpClient) { }

  login(model: any) {
    const base64creds = btoa(`${model.username}:${model.password}`);//back ticks to make sure it gets evaluated correctly as normal ' will see it as a

    const headers = new HttpHeaders({
        'Content-Type': 'application/json',
        'Authorization': `Basic ${base64creds}`
      });

    return this.http.get<User>(this.baseUrl + 'login', {headers}).pipe(
      map((response: User) => {
        const user = response;
        if (user) {
          this.setCurrentUser(user);
        }
      })
    )
  }

  register(newUser: any) {
    let postData = new FormData();
        postData.append("name", newUser.name);
        postData.append("username", newUser.username);
        postData.append("password", newUser.password);
        postData.append("email", newUser.email);

        return this.http.post(this.baseUrl +'signup', postData);

  }

  setCurrentUser(user: User) {
    sessionStorage.setItem('user', JSON.stringify(user));
    this.currentUserSource.next(user);
  }

  logout() {
    const user = JSON.parse(sessionStorage.getItem('user') || '{}');
    const token = user.token;
  
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'x-access-token': token,
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


  getDecodedToken(token: string) {
    return JSON.parse(atob(token.split('.')[1]));
  }
}

