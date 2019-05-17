import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';

import { Observable, of } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';

import { User } from '../data_classes/user';
import { ChargingStation } from '../data_classes/chargingStation';
import { STATIONS} from '../data_classes/mock_cs'
import { environment } from '../../environments/environment';

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
  findStations(poiLat: number, poiLng: number ): Observable<ChargingStation[]> {
    if (typeof poiLat === 'undefined' ||  typeof poiLng === 'undefined') {
      console.log('Error at findStations(). Invalid coordinates.');
    } else {
      const params = new HttpParams()
        .set('poi_lat', String(poiLat))
        .set('poi_lng', String(poiLng));
        // Call API and return a Observable<CS[]> (aka. CS array)
      return this.http.get<ChargingStation[]>(this.API_URL, {params: params}).pipe(
        map(stationsList => stationsList.map(station => ChargingStation.create(station)))
        );
    }
  }
}


