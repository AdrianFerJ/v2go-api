// TODO find out import error of platform-browser
import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';  
// import { HttpClientModule, HttpClientXsrfModule } from '@angular/common/http';  
import { HttpClientModule } from '@angular/common/http';  

import { AuthService } from './services/auth.service';  

import { AppComponent } from './app.component';
import { SignUpComponent } from './components/sign-up/sign-up.component';
import { LogInComponent } from './components/log-in/log-in.component';
import { LandingComponent } from './components/landing/landing.component';

@NgModule({
  declarations: [
    AppComponent,
    SignUpComponent,
    LogInComponent,
    LandingComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    // HttpClientXsrfModule,
    FormsModule,
    RouterModule.forRoot([
      { path: 'sign-up', component: SignUpComponent },
      { path: 'log-in', component: LogInComponent },
      { path: '', component: LandingComponent }
    ], { useHash: true })
  ],
  providers: [ 
    AuthService,
    // HttpXsrfInterceptor, 
    // { provide: HTTP_INTERCEPTORS, useExisting: HttpXsrfInterceptor, multi: true },
    // { provide: HttpXsrfTokenExtractor, useClass: HttpXsrfCookieExtractor },
    // { provide: XSRF_COOKIE_NAME, useValue: 'XSRF-TOKEN' },
    // { provide: XSRF_HEADER_NAME, useValue: 'X-XSRF-TOKEN' }
  ],
  bootstrap: [ AppComponent ]
})
  
export class AppModule { }
