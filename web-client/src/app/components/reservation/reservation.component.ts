import { Component, OnInit, Input } from '@angular/core';
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

  @Input() availability: Availability;
  @Input() evNk: string;
  @Input() chargingStation: ChargingStation;

  reservation$: Observable<Reservation>;
  reservation: Reservation;

  constructor(private reservationService: ReservationService) { }

  ngOnInit() {}

  public makeReservation() {
    this.reservation$ = this.reservationService.makeReservation(this.evNk, this.availability.nk);
  }
}
