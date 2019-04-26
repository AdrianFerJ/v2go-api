import { HttpClient }      from '@angular/common/http';
import { Injectable }      from '@angular/core';

import { Observable, of }      from 'rxjs';
import { map }             from 'rxjs/operators';

import { User }            from './auth.service';
import { ChargingStation } from '../data_classes/chargingStation';

import { STATIONS}         from '../data_classes/mock_cs'


@Injectable({
  providedIn: 'root'
})
export class SearchStationsService {
  API_URL  =  'http://localhost:8000/api/v1.0-pre-alpha/';
  constructor(
    // private http: HttpClient
  ) { }

  findStations(): Observable<ChargingStation[]> {
    console.log('#'.repeat(50), "Inside findStations()....")
    console.log("Stations: ", STATIONS)
    
    // of(Stations) returns an Observable<CS[]> that 
    // .. emits a single value (array of CSs)
    return of(STATIONS);
  }

  // findStations(){
  //   console.log('#'.repeat(50), "Inside findStations()....")
  //   let resp = this.http.get(`${this.API_URL}/near-poi`);
  //   console.log('# RESP: ', resp)
  //   return resp

  // findStations(): Observable<ChargingStation[]> {
  //   console.log('#'.repeat(50), "Inside findStations()....")
  //   return this.http.get<ChargingStation[]>(`${this.API_URL}/near-poi`).pipe(
  //     map(stations => stations.map(station => ChargingStation.create(station)))
  //   );
  // }

}
