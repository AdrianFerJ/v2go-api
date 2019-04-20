import { HttpClient } from '@angular/common/http'; 
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { finalize, tap } from 'rxjs/operators';

export class User {
  // Data model to store user info (a JSON-serialized string returned by API) in the UI
  constructor(
    public id?: number,
    public username?: string,
    public first_name?: string,
    public last_name?: string,
    public group?: string,
  ) {}
  

  // Convenience method to handle the conversion from JSON to data object 
  static create(data: any): User { 
    return new User(
      data.id,
      data.username,
      data.first_name,
      data.last_name,
      data.group,
    );
  }
  // Convinience method to check if user is logged in
  static getUser(): User {
    const userData = localStorage.getItem('v2go.user');
    if (userData) {
      return User.create(JSON.parse(userData));
    }
    return null;
  }
}
@Injectable({
  providedIn: 'root'
})
export class AuthService {
  constructor(private http: HttpClient) {} 
  // SignUp returns an Observable that will produce User data. Subscribing
  // .. to this Observable will then send the HTTP request to the API
  signUp( 
    username: string,
    firstName: string,
    lastName: string,
    password: string,
    group: string,
  ): Observable<User> {
    const url = 'http://localhost:8000/api/v1.0-pre-alpha/sign-up';
    // const url = 'sign_up/'; #UPDATE endpoint after wiring angular with nxing to rerout API calls
    const formData = new FormData();
    formData.append('username', username);
    formData.append('first_name', firstName);
    formData.append('last_name', lastName);
    formData.append('password1', password);
    formData.append('password2', password);
    formData.append('group', group);
    return this.http.request<User>('POST', url, {body: formData});
  }
  // LogIn function collects a username and a password and sends the data to the API endpoint
  // .. logIn also returns an Observable that produces a User, and it saves that User object in localStorage
  logIn(username: string, password: string): Observable<User> {
    const url = 'http://localhost:8000/api/v1.0-pre-alpha/login';
    // const url = '/log_in/';
    // post converts data dictionary into data payload
    return this.http.post<User>(url, {username, password}).pipe(
      tap(user => localStorage.setItem('v2go.user', JSON.stringify(user))
      )
    );
  }
  // Simply subscribe to observable to send request to API (no data, nor component.ts required)
  // .. then removed logged user from localStorage
  logOut(): Observable<any> {
    const url = 'http://localhost:8000/api/v1.0-pre-alpha/logout';
    // const url = '/log_out/';
    return this.http.post(url, null).pipe(
      finalize(() => localStorage.removeItem('v2go.user'))
    );
  }

}