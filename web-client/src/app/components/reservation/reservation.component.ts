import { Component, OnInit } from '@angular/core';
import { ReservationService } from '../../services/reservation.service';
import { Observable } from 'rxjs';
import { Reservation } from '../../data_classes/reservation';
import { ChargingStation } from '../../data_classes/chargingStation';
import { Availability } from '../../data_classes/availability';

@Component({
  selector: 'app-reservation',
  templateUrl: './reservation.component.html',
  styleUrls: ['./reservation.component.css']
})
export class ReservationComponent implements OnInit {

  reservation$: Observable<Reservation>;
  reservation: Reservation;
  availability: Availability;
  eventCsNk: string;
  evNk: string;
  chargingStation: ChargingStation;

  constructor(private reservationService: ReservationService) { }

  ngOnInit() {}

  public makeReservation() {
    this.reservation$ = this.reservationService.makeReservation(this.evNk, this.eventCsNk);
  }
}
