import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class DriverProfileService {
  API_URL = 'http://localhost/';

  constructor(private http: HttpClient) { }
}
