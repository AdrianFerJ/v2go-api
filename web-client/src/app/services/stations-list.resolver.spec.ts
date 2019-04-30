import { Observable, of }       from 'rxjs';

import { ChargingStation }      from '../data_classes/chargingStation';
import { StationsListResolver } from '../services/stations-list.resolver';
import { CStationFactory }      from '../testing/factories';


describe('StationListResolver', () => {
  it('findStations() should resolve a list of stations (using resolver)', () => {
    // Create fake CS 
    const stationsMock: ChargingStation[] = [
      CStationFactory.create(),
      CStationFactory.create()
    ];
    // Create fake service (instead of calling the actual service and it's dependencies)
    const searchCsServiceMock: any = {
      findStations: (): Observable<ChargingStation[]> => {
          return of(stationsMock);
      }
    };
    // Test whether the resolver passes back an Observable object
    const stationsListResolver: StationsListResolver = new StationsListResolver(searchCsServiceMock);
    stationsListResolver.resolve(null, null).subscribe(stations => {
      expect(stations).toBe(stationsMock);
    });
  });
});