import { HttpClient, HttpHeaders, HttpParams }  from '@angular/common/http';
import { Injectable }               from '@angular/core';

import { Observable, of }           from 'rxjs';
import { catchError, map, tap }     from 'rxjs/operators';

import { User }                     from '../data_classes/user';
import { ChargingStation }          from '../data_classes/chargingStation';
import { STATIONS}                  from '../data_classes/mock_cs'
import { environment }              from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class SearchStationsService {
  private API_URL = environment.baseUrl + 'volt_finder/near-poi';
  constructor(
    private http: HttpClient,
  ) { }

  /**
  * Performs CS search by calling the 'API/near-poi' endpoint.
  * 
  * @param POI - Point of interest locaiton
  * @param advance param ...
  */
  findStations(): Observable<ChargingStation[]> {
    // Create fake parameters
    // let testAddress = '1735 Rue Saint-Denis, Montréal, QC H2X 3K4, Canada';
    // let params = new HttpParams().set("poi_location", testAddress);
    let POI_LAT = String(45.5260525)
    let POI_LNG = String(-73.5596788)
    let params = new HttpParams()
      .set("poi_lat", POI_LAT)
      .set("poi_lng", POI_LNG);
    
    // Call API and return a Observable<CS[]> (aka. CS array)
    return this.http.get<ChargingStation[]>(this.API_URL, {params: params}).pipe(
      map(stationsList => stationsList.map(station => ChargingStation.create(station)))
        // catchError(this.handleError<ChargingStation[]>('findStationss', []))
    );
  }
  /**
  * Handle Http operation that failed, and Let the app continue.
  * 
  * @param operation - name of the operation that failed
  * @param result - optional value to return as the observable result
  */
  private handleError<T> (operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {
      // TODO: send the error to remote logging infrastructure
      console.error(`Error: ${operation} failed: ${error.message}`); 
      return of(result as T);
    };
  }
}


