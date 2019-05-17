import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { User } from '../data_classes/user';
import { Observable } from 'rxjs';
import { Reservation } from '../data_classes/reservation';

@Injectable({
  providedIn: 'root'
})
export class ReservationService {
  API_URL = 'http://localhost:8888/api/v1.0-pre-alpha/volt_reservation/reservations/';
  user: User;

  constructor(private http: HttpClient) {
    const userData = localStorage.getItem('v2go.user');
    this.user = User.create(JSON.parse(userData));
  }

  public makeReservation(eventCsNk, evNk): Observable<Reservation> {
    return this.http.post<Reservation>(this.API_URL,
      {
        'event_cs_nk': eventCsNk,
        'ev_nk': evNk
      });
  }
}
