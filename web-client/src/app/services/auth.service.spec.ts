import {
  HttpClientTestingModule, HttpTestingController
} from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';

import { AuthService, User } from './auth.service';
import { UserFactory } from '../testing/factories';


describe('AuthService', () => {
  let authService: AuthService;
  beforeEach(() => {
    TestBed.configureTestingModule({
      
      imports: [ HttpClientTestingModule ],
      
      declarations: [],
      
      providers: [ AuthService ]
    });
    authService = TestBed.get(AuthService);
  });
  it('should be created', () => {
    expect(authService).toBeTruthy();
  });
});

describe('Authentication using a service', () => {
  //TODO UPDATE all API END POINTS
  let authService: AuthService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [ HttpClientTestingModule ],
      providers: [ AuthService ]
    });
    authService = TestBed.get(AuthService);
    httpMock = TestBed.get(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should allow a user to sign up for a new account', () => {
    // Create test user
    const userData = UserFactory.create();
    
    // Test sign-up
    authService.signUp(
      userData.username,
      userData.first_name,
      userData.last_name,
      'letmein!',
      'letmein!'
      // userData.group,
    ).subscribe(user => {
      debugger
      expect(user).toBe(userData);
    });
    const request = httpMock.expectOne('http://localhost:8000/api/v1.0-pre-alpha/sign-up');
    request.flush(userData);
  });

  it('should allow a user to log in to an existing account', () => {
    const userData = UserFactory.create();
    // A successful login should write data to local storage.
    localStorage.clear();
    // Create observable with logIn() and then subscribe to it 
    // *Subscribing to observable make the call to the API
    authService.logIn(
      userData.username, 'letmein!'
    ).subscribe(user => {
      expect(user).toBe(userData);
    });
    const request = httpMock.expectOne('http://localhost:8000/api/v1.0-pre-alpha/login');
    request.flush(userData);
    // Confirm that the expected data was written to local storage.
    expect(localStorage.getItem('v2go.user')).toBe(JSON.stringify(userData));
  });

  it('should allow a user to log out', () => {
    // Set up the data.
    const userData = {};
    // A successful logout should delete local storage data.
    localStorage.setItem('v2go.user', JSON.stringify({}));
    // Execute the function under test.
    authService.logOut().subscribe(user => {
      expect(user).toEqual(userData);
    });
    const request = httpMock.expectOne('http://localhost:8000/api/v1.0-pre-alpha/logout'); 
    request.flush(userData);
    // Confirm that the local storage data was deleted.
    expect(localStorage.getItem('v2go.user')).toBeNull();
  });

  it('should determine whether a user is logged in', () => {
    localStorage.clear();
    expect(User.getUser()).toBeFalsy();
    localStorage.setItem('v2go.user', JSON.stringify(
      UserFactory.create()
    ));
    expect(User.getUser()).toBeTruthy();
  });
});

