import { HttpClient, HttpHeaders, HttpParams }  from '@angular/common/http';
import { Injectable }               from '@angular/core';

import { Observable, of }           from 'rxjs';
import { catchError, map, tap }     from 'rxjs/operators';

import { User }                     from '../data_classes/user';
import { ChargingStation }          from '../data_classes/chargingStation';
import { STATIONS}                  from '../data_classes/mock_cs'
import { environment }              from '../../environments/environment';
import { error }                    from '@angular/compiler/src/util';

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
  * 
  * @param poi_lat - Point of interest latitude, either from user's location or default lat (MTL)
  * @param poi_lng - Point of interest longitude or default lng (MTL)
  */
// findStations(): Observable<ChargingStation[]> {
  findStations(poi_lat: number, poi_lng: number,): Observable<ChargingStation[]> {
    if (typeof poi_lat == 'undefined' ||  typeof poi_lng == 'undefined') {
      console.log("Error at findStations(). Invalid coordinates.");
    } else {
      let params = new HttpParams()
        .set("poi_lat", String(poi_lat))
        .set("poi_lng", String(poi_lng));
        
        // Call API and return a Observable<CS[]> (aka. CS array)
        return this.http.get<ChargingStation[]>(this.API_URL, {params: params}).pipe(
          map(stationsList => stationsList.map(station => ChargingStation.create(station)))
        );
    }
  }
}


