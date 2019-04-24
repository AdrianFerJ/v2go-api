import { TestBed } from '@angular/core/testing';

import { SearchStationsService } from './search-stations.service';

describe('SearchStationsService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: SearchStationsService = TestBed.get(SearchStationsService);
    expect(service).toBeTruthy();
  });
});
