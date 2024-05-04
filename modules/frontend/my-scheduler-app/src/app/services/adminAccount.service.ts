import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, map } from 'rxjs';
import { User } from '.././user/user';


@Injectable({
  providedIn: 'root'
})
export class AdminAccountService {
  baseUrl = 'http://127.0.0.1:5000/v1/admin/';
  private currentUserSource = new BehaviorSubject<User | null>(null);
  currentUser$ = this.currentUserSource.asObservable();

  constructor(private http: HttpClient) { }

  login(loginUser: any) {
    const loginJson = JSON.stringify(loginUser); // convert to json
    console.log(loginJson);
    const headers = new HttpHeaders().set('Content-Type', 'application/json');
  
    return this.http.post<User>(this.baseUrl + 'login', loginJson, { headers }).pipe(
      map((response: User) => {
        const user = response;
        if (user) {
          this.setCurrentUser(user);
        }
      })
    );
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
        newUser.skills.forEach((skill: string | Blob, index: any) => {
          postData.append(`skills[${index}]`, skill);
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

  getDecodedToken(token: string) {
    return JSON.parse(atob(token.split('.')[1]));
  }


    getUsers(){
      const user = JSON.parse(sessionStorage.getItem('user') || '{}');
      const token = user.access_token;
      const headers = new HttpHeaders(
        {
           'Content-Type': 'application/json',
           'Authorization': `Bearer ${token}`,
        });
      return this.http.get('http://127.0.0.1:5000/v1/get/users', {headers});
    }

    getStaff(){
      const user = JSON.parse(sessionStorage.getItem('user') || '{}');
      const token = user.access_token;
      const headers = new HttpHeaders(
        {
           'Content-Type': 'application/json',
           'Authorization': `Bearer ${token}`,
        });
      return this.http.get('http://127.0.0.1:5000/v1/get/staff/all', {headers});
    }

    deleteUser(removeUserId: string){
      const user = JSON.parse(sessionStorage.getItem('user') || '{}');
      const token = user.access_token;
    
      const headers = new HttpHeaders({
            'Content-Type': 'application/json',
              'Authorization': `Bearer ${token}`,
      });
      return this.http.delete('http://127.0.0.1:5000/v1/user/delete/'+ removeUserId, {headers});
    }

    deleteStaff(removeStaffId: string){
      const user = JSON.parse(sessionStorage.getItem('user') || '{}');
      const token = user.access_token;
    
      const headers = new HttpHeaders({
            'Content-Type': 'application/json',
              'Authorization': `Bearer ${token}`,
      });
      return this.http.delete('http://127.0.0.1:5000/v1/staff/delete/'+ removeStaffId, {headers});
    }


}


