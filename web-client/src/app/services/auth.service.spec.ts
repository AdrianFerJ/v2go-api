
import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';

import { AuthService } from './auth.service';



fdescribe('AuthService', () => {
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
