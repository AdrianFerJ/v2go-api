import {HttpClientTestingModule, HttpTestingController, TestRequest
}                                     from '@angular/common/http/testing';
import { TestBed, ComponentFixture }  from '@angular/core/testing';
import { RouterTestingModule }        from '@angular/router/testing';
import { By }                         from '@angular/platform-browser';
import { DebugElement }               from '@angular/core';
import { FormsModule }                from '@angular/forms';

import { AuthService }                from '../../services/auth.service';
import { UserFactory }                from '../../testing/factories';
import { LandingComponent }           from './landing.component';

describe('LandingComponent', () => {
  let logOutButton: DebugElement;
  let component: LandingComponent;
  let fixture: ComponentFixture<LandingComponent>;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [
        FormsModule,
        HttpClientTestingModule,
        RouterTestingModule.withRoutes([])
      ],
      declarations: [ LandingComponent ],
      providers: [ AuthService ]
    });
    fixture = TestBed.createComponent(LandingComponent);
    component = fixture.componentInstance;
    httpMock = TestBed.get(HttpTestingController);
    localStorage.setItem('v2go.user', JSON.stringify(
      UserFactory.create()
    ));
    fixture.detectChanges();
    // Select logout button
    logOutButton = fixture.debugElement.query(By.css('button.btn.btn-primary'));
  });

  it('should allow a user to log out of an account', () => {
    logOutButton.triggerEventHandler('click', null);
    const request: TestRequest = httpMock.expectOne('http://localhost:8000/api/v1.0-pre-alpha/logout');
    request.flush({});
    expect(localStorage.getItem('v2go.user')).toBeNull();
  });

  it('should indicate whether a user is logged in', () => {
    localStorage.clear();
    expect(component.getUser()).toBeFalsy();
    localStorage.setItem('v2go.user', JSON.stringify(
      UserFactory.create()
    ));
    expect(component.getUser()).toBeTruthy();
  });

  it('should return true if the user is a driver (group)', () => {
    localStorage.clear();
    localStorage.setItem('v2go.user', JSON.stringify(
      UserFactory.create({group: 'driver'})
    ));
    expect(component.isDriver()).toBeTruthy();
  });

  afterEach(() => {
    httpMock.verify();
  });
});