import { Component, OnInit } from '@angular/core';
import { VehicleService } from '../../../app/services/api.service';
import { Validators, FormGroup, FormControl } from '@angular/forms';

@Component({
  selector: 'app-vehicle',
  templateUrl: './vehicle.component.html',
  styleUrls: ['./vehicle.component.css']
})
export class VehicleComponent implements OnInit {
  onSubmit(value: any): void {
    const nickname = value.nickname;
    const model = value.model;
    const manufacturer = value.manufacturer;
    const year = value.year;
    const chargerType = value.chargerType;

    this.vehicleService.createVehicle(nickname, model,
      manufacturer, year, chargerType)
      .subscribe(() => {
        console.log('Created Vehicle successfully');
      }, (error) => {
        console.error('Failed', error);
      });
  }

  constructor(private vehicleService: VehicleService) { }

  ngOnInit() {
  }
}
