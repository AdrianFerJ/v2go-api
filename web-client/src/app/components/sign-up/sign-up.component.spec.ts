import {
  HttpClientTestingModule, HttpTestingController
} from '@angular/common/http/testing';
import { TestBed, ComponentFixture } from '@angular/core/testing';
import { Router } from '@angular/router';
import { RouterTestingModule } from '@angular/router/testing';
import { FormsModule } from '@angular/forms';

import { AuthService } from '../../services/auth.service';
import { UserFactory } from '../../testing/factories';
import { SignUpComponent } from './sign-up.component';

fdescribe('SignUpComponent', () => {
  let component: SignUpComponent;
  let fixture: ComponentFixture<SignUpComponent>;
  let router: Router;
  let httpMock: HttpTestingController;
  
  // Initialized our variables and configured the testing module:
  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [
        FormsModule,
        HttpClientTestingModule,
        RouterTestingModule.withRoutes([])
      ],
      declarations: [ SignUpComponent ],
      providers: [ AuthService ]
    });
    fixture = TestBed.createComponent(SignUpComponent);
    component = fixture.componentInstance;
    router = TestBed.get(Router);
    httpMock = TestBed.get(HttpTestingController);
  });

  it('should allow a user to sign up for an account', () => {
    // set up a facke/mock backend to respond to client the way the server API should
    // .. enables development and testing without runing django
    const spy = spyOn(router, 'navigateByUrl');
    // Create user
    const user = UserFactory.create();
    component.user = {
      username: user.username,
      firstName: user.first_name,
      lastName: user.last_name,
      password: 'letmein!',
      group: user.group,      
    };
    // Send data to server (or intercepted by httpMock if not running in docker)
    component.onSubmit();
    // const request = httpMock.expectOne('/api/sign_up/');
    // request.flush(user);
    // expect(spy).toHaveBeenCalledWith('/log-in');
  });

});