import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';

import { environment } from '../environments/environment';
import { AgmCoreModule } from '@agm/core';

import { AuthService } from './services/auth.service';
import { SearchStationsService } from './services/api.service';

import { AppComponent } from './app.component';
import { SignUpComponent } from './components/sign-up/sign-up.component';
import { LogInComponent } from './components/log-in/log-in.component';
import { LandingComponent } from './components/landing/landing.component';
import { DriverComponent } from './components/driver/driver.component';
import { DriverHomeMapComponent } from './components/driver-home-map/driver-home-map.component';
import { ReservationComponent } from './components/reservation/reservation.component';
import { VehicleComponent } from './components/vehicle/vehicle.component';

// TODO move appRoutes to a separate Module
//  .. https://angular.io/tutorial/toh-pt5#add-the-approutingmodule
const appRoutes: Routes = [
  { path: 'sign-up', component: SignUpComponent },
  { path: 'log-in', component: LogInComponent },
  // {
  //   //TODO ADD group based restriction IsDriver
  //   // canActivate: [ IsDriver ],
  //   // children: [
  //   //   { path: 'map',
  //   //     component: DriverHomeMapComponent,
  //   //   },
  //   //   // {
  //   //   //   path: 'my-account',
  //   //   //   component: DriverComponent
  //   //   // },
  //   // ]
  //   path: 'driver',
  //   component: DriverComponent,
  // },
  { path: 'driver', component: DriverComponent },
  {
    path: 'map',
    component: DriverHomeMapComponent,
  },
  { path: 'reservation', component: ReservationComponent },
  { path: 'add-vehicle', component: VehicleComponent },
  { path: '', component: LandingComponent }
  // TODO add a pageNotFound Component
  // { path: '**', component: PageNotFoundComponent }
];

@NgModule({
  imports: [
    BrowserModule,
    HttpClientModule,
    FormsModule,
    RouterModule.forRoot(
      appRoutes,
      { enableTracing: true } // <-- debugging purposes only
    ),
    AgmCoreModule.forRoot({
      apiKey: environment.GOOGLE_API_KEY
    })
  ],
  declarations: [
    AppComponent,
    SignUpComponent,
    LogInComponent,
    LandingComponent,
    DriverComponent,
    DriverHomeMapComponent,
    ReservationComponent,
    VehicleComponent
  ],
  providers: [
    AuthService,
    SearchStationsService,
  ],
  bootstrap: [AppComponent]
})

export class AppModule { }
