import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { DriverInfo } from '../data_classes/driver_profile';
import { User } from '../data_classes/user';

@Injectable({
  providedIn: 'root'
})
export class DriverProfileService {
  API_URL  =  'http://localhost:8888/api/v1.0-pre-alpha';
  user: User;

  constructor(private http: HttpClient) {
    const userData = localStorage.getItem('v2go.user');
    this.user = User.create(JSON.parse(userData));
  }

  public getProfileInfo(): Observable<DriverInfo> {
    return this.http.get<DriverInfo>(`${this.API_URL}/my-account/${this.user.id}`);
  }
}
