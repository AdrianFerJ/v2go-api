import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DriverHomeMapComponent } from './driver-home-map.component';

describe('DriverHomeMapComponent', () => {
  let component: DriverHomeMapComponent;
  let fixture: ComponentFixture<DriverHomeMapComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DriverHomeMapComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DriverHomeMapComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  // it('should create', () => {
  //   expect(component).toBeTruthy();
  // });
});
