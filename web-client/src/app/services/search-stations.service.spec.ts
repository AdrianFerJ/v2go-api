import {
  HttpClientTestingModule, HttpTestingController, TestRequest
}                                from '@angular/common/http/testing';
import { TestBed }               from '@angular/core/testing';

import { CStationFactory }       from '../testing/factories';
import { SearchStationsService } from './search-stations.service';


describe('SearchStationsService', () => {
  let searchService: SearchStationsService;
  let httpMock: HttpTestingController;
  let API_URL:  'http://localhost:8000/api/v1.0-pre-alpha/near-poi';

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [ HttpClientTestingModule],
      providers: [ SearchStationsService ]
    });
    searchService = TestBed.get(SearchStationsService);
    httpMock = TestBed.get(HttpTestingController);
  });

  // afterEach(() => {
  //   httpMock.verify();
  // });

  it('should allow a driver to search CS near a point of interest (POI) location', () => {
    // const cs1 = CStationFactory.create();
    // const cs2 = CStationFactory.create();
    const testCS = [
      CStationFactory.create(), 
      CStationFactory.create()
    ]
  
    searchService.findStations().subscribe(stationsList => {
      // expect(stationsList).toEqual([cs1, cs2]);
      expect(stationsList).toEqual(testCS);
    });
    
    // console.log("OUTPUT: ", this.stationList)
    // console.log("FAKE: ", cs1, cs2)
    
    // const request: TestRequest = httpMock.expectOne(API_URL);

    // console.log('*'.repeat(100))
    // console.log(request)

    // request.flush(testCS);
    
  });
});