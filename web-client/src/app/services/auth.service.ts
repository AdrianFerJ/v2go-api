import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { finalize, tap } from 'rxjs/operators';
import { User } from '../data_classes/user';
import { environment } from '../../environments/environment';


@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private API_URL = environment.devUrl;
  constructor(private http: HttpClient) {

  }
  // SignUp returns an Observable that will produce User data. Subscribing
  // .. to this Observable will then send the HTTP request to the API
  signUp(
    username: string,
    firstName: string,
    lastName: string,
    password1: string,
    password2: string,
    // group: string,
  ): Observable<User> {
    const url = this.API_URL + 'sign-up';
    // const url = 'sign_up/'; #UPDATE endpoint after wiring angular with nxing to rerout API calls
    const formData = new FormData();
    formData.append('username', username);
    formData.append('first_name', firstName);
    formData.append('last_name', lastName);
    formData.append('password1', password1);
    formData.append('password2', password2);
    // formData.append('group', group);
    return this.http.request<User>('POST', url, { body: formData });
  }
  // LogIn function collects a username and a password and sends the data to the API endpoint
  // .. logIn also returns an Observable that produces a User, and it saves that User object in localStorage
  logIn(username: string, password: string): Observable<User> {
    const url = this.API_URL + 'login';
    // const url = '/log_in/';
    // post converts data dictionary into data payload
    return this.http.post<User>(url, { username, password }).pipe(
      tap(user => localStorage.setItem('v2go.user', JSON.stringify(user))
      )
    );
  }
  // Simply subscribe to observable to send request to API (no data, nor component.ts required)
  // .. then removed logged user from localStorage
  logOut(): Observable<any> {
    const url = this.API_URL + 'logout';
    // const url = '/log_out/';
    return this.http.post(url, null).pipe(
      finalize(() => localStorage.removeItem('v2go.user'))
    );
  }

}
