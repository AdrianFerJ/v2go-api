import { HttpClient, HttpHeaders }  from '@angular/common/http';
import { Injectable }               from '@angular/core';

import { Observable, of }           from 'rxjs';
import { catchError, map, tap }     from 'rxjs/operators';

import { User }                     from './auth.service';
import { ChargingStation }          from '../data_classes/chargingStation';
import { STATIONS}                  from '../data_classes/mock_cs'


@Injectable({
  providedIn: 'root'
})
export class SearchStationsService {
  private API_URL  =  'http://localhost:8000/api/v1.0-pre-alpha';
  constructor(
    private http: HttpClient, 
  ) { }

  /**
  * Performs CS search by calling the 'API/near-poi' endpoint.
  * Let the app continue.
  * @param POI - Point of interest locaiton
  * @param advance param ...
  */
  findStations(): Observable<ChargingStation[]> {
    // console.log('#'.repeat(50), "Inside findStations()....")
    // console.log("Stations: ", STATIONS)
    // Fake Data
    // of(Stations) returns an Observable<CS[]> that 
    // .. emits a single value (array of CSs objects)
    // return of(STATIONS);

    // Call API and return a CS array
    return this.http.get<ChargingStation[]>(`${this.API_URL}/stations`)
      .pipe(
        catchError(this.handleError<ChargingStation[]>('findStationss', []))
    );
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



  /**
  * Handle Http operation that failed.
  * Let the app continue.
  * @param operation - name of the operation that failed
  * @param result - optional value to return as the observable result
  */
  private handleError<T> (operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {

      // TODO: send the error to remote logging infrastructure
      console.error(`Error: ${operation} failed: ${error.message}`); 

      // Let the app keep running by returning an empty result.
      return of(result as T);
    };
  }

}
