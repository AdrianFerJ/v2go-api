import { TestBed } from '@angular/core/testing';

import { DriverProfileService } from './driver-profile.service';

describe('DriverProfileService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: DriverProfileService = TestBed.get(DriverProfileService);
    expect(service).toBeTruthy();
  });
});
