import { HttpClient, HttpHeaders, HttpParams }  from '@angular/common/http';
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
  private API_URL  =  'http://localhost:8000/api/v1.0-pre-alpha/volt_finder/near-poi'
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
    console.log('#findStations'.repeat(5), "Inside findStations()....")

    // Create fake parameters
    let testAddress = '1735 Rue Saint-Denis, Montréal, QC H2X 3K4, Canada';
    let params = new HttpParams().set("poi_location", testAddress);

    // Call API and return a Observable<CS[]> (aka. CS array)
    return this.http.get<ChargingStation[]>(this.API_URL, {params: params}).pipe(
      map(stationsList => stationsList.map(station => ChargingStation.create(station)))
        // catchError(this.handleError<ChargingStation[]>('findStationss', []))
    );
  }
  // OLD APPROACH
  // findStations(){
  //   let resp = this.http.get(`${this.API_URL}/near-poi`);
  //   console.log('# RESP: ', resp)
  //   return resp


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
