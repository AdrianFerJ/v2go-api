import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';

import { Observable, of } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';

import { User } from '../data_classes/user';
import { ChargingStation } from '../data_classes/chargingStation';
import { STATIONS } from '../data_classes/mock_cs'
import { environment } from '../../environments/environment';
import { Reservation } from '../../app/data_classes/reservation';
import { DriverInfo } from '../../app/data_classes/driver_profile';

@Injectable({
  providedIn: 'root'
})
export class SearchStationsService {
  private API_URL = environment.devUrl + 'volt_finder/near-poi';
  constructor(
    private http: HttpClient,
  ) { }

  /**
   * Performs CS search by calling the 'API/near-poi' endpoint.
   * @param poiLat - Point of interest latitude, either from user's location or default lat (MTL)
   * @param poiLng - Point of interest longitude or default lng (MTL)
   */
  // findStations(): Observable<ChargingStation[]> {
  findStations(poiLat: number, poiLng: number): Observable<ChargingStation[]> {
    if (typeof poiLat === 'undefined' || typeof poiLng === 'undefined') {
      console.log('Error at findStations(). Invalid coordinates.');
    } else {
      const params = new HttpParams()
        .set('poi_lat', String(poiLat))
        .set('poi_lng', String(poiLng));
      // Call API and return a Observable<CS[]> (aka. CS array)
      return this.http.get<ChargingStation[]>(this.API_URL, { params: params }).pipe(
        map(stationsList => stationsList.map(station => ChargingStation.create(station)))
      );
    }
  }
}

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

@Injectable({
  providedIn: 'root'
})
export class DriverProfileService {
  API_URL  =  environment.devUrl;
  user: User;

  constructor(private http: HttpClient) {
    const userData = localStorage.getItem('v2go.user');
    this.user = User.create(JSON.parse(userData));
  }

  public getProfileInfo(): Observable<DriverInfo> {
    return this.http.get<DriverInfo>(`${this.API_URL}my-account/${this.user.id}`);
  }
}
