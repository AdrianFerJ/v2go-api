import {
  HttpClientTestingModule, HttpTestingController, TestRequest
}                                from '@angular/common/http/testing';
import { TestBed }               from '@angular/core/testing';
import { CStationFactory }       from '../testing/factories';
import { SearchStationsService } from './search-stations.service';


describe('SearchStationsService', () => {
  let csService: SearchStationsService;
  let httpMock: HttpTestingController;
  let API_URL  =  'http://localhost:8000/api/v1.0-pre-alpha/';
  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [
        HttpClientTestingModule
      ],
      providers: [ csService ]
    });
    csService = TestBed.get(SearchStationsService);
    httpMock = TestBed.get(HttpTestingController);
  });

  it('should allow a driver to search CS near a point of interest (POI) location', () => {
    const cs1 = CStationFactory.create();
    const cs2 = CStationFactory.create();
    // console.log('*'.repeat(100), "CS TEST....")
    // console.log(cs1, cs2)
    console.log('_'.repeat(200), "CStationService....")
    console.log(csService)

    csService.findStations().subscribe(stations => {
      expect(stations).toEqual([cs1, cs2]);
    });
  
    const request: TestRequest = httpMock.expectOne(`${this.API_URL}/near-poi`);
    request.flush([
      cs1,
      cs2
    ]);
    console.log('*'.repeat(100), "TEST request....")
    console.log(request)
  });

  afterEach(() => {
    httpMock.verify();
  });
});