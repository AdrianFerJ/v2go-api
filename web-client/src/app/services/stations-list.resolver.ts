import { Injectable }            from '@angular/core';
import { Observable }            from 'rxjs';

import {
  ActivatedRouteSnapshot, Resolve, RouterStateSnapshot
} from '@angular/router';

import { SearchStationsService } from './api.service';
import { ChargingStation }       from '../data_classes/chargingStation';

@Injectable()
/**
 * Prevents component to load until data from service is fully loaded. 
 * 
 * retunts: an observable for the component to subscribe to
 * 
 */
export class StationsListResolver implements Resolve<ChargingStation[]> {
  constructor(private searchService: SearchStationsService) {}
  resolve(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): Observable<ChargingStation[]> {
    return this.searchService.findStations();
  }
}