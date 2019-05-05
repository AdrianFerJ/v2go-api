import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { DriverInfo } from '../../data_classes/driver_profile';
import { DriverProfileService } from '../../services/driver-profile.service';

@Component({
  selector: 'app-driver',
  templateUrl: './driver.component.html',
  styleUrls: ['./driver.component.css']
})
export class DriverComponent implements OnInit {
  driver$: Observable<DriverInfo>;
  driver: DriverInfo;

  constructor(private driverProfileService: DriverProfileService) { }

  ngOnInit() {
    this.getInfo();
  }

  getInfo() {
    this.driver$ = this.driverProfileService.getProfileInfo();
    console.log(this.driver);
  }
}
