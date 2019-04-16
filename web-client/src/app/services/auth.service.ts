import { HttpClient } from '@angular/common/http'; 
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs'; 

export class User {
  // Data model to store user info (a JSON-serialized string returned by API) in the UI
  constructor(
    public id?: number,
    public username?: string,
    public first_name?: string,
    public last_name?: string,
    public group?: string,
    public photo?: any
  ) {}

  // Convenience method to handle the conversion from JSON to data object 
  static create(data: any): User { // new
    return new User(
      data.id,
      data.username,
      data.first_name,
      data.last_name,
      data.group,
      data.photo
    );
  }
}
@Injectable({
  providedIn: 'root'
})
export class AuthService {
  // AuthService returns an Observable that will produce User data. Subscribing
  // .. to this Observable will then send the HTTP request to the API
  constructor(private http: HttpClient) {} 
  signUp( 
    username: string,
    firstName: string,
    lastName: string,
    password: string,
    group: string,
  ): Observable<User> {
    const url = 'http://localhost:8000/api/sign_up/';
    const formData = new FormData();
    formData.append('username', username);
    formData.append('first_name', firstName);
    formData.append('last_name', lastName);
    formData.append('password1', password);
    formData.append('password2', password);
    formData.append('group', group);
    return this.http.request<User>('POST', url, {body: formData});
  }
}