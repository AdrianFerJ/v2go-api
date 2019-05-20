import { Component, OnInit, Input } from '@angular/core';
import { Observable } from 'rxjs';
import { Reservation } from '../../data_classes/reservation';
import { ChargingStation } from '../../data_classes/chargingStation';
import { EventCS } from '../../data_classes/event_cs';
import { ReservationService } from '../../../app/services/api.service';

@Component({
  selector: 'app-reservation',
  templateUrl: './reservation.component.html',
  styleUrls: ['./reservation.component.css']
})
export class ReservationComponent implements OnInit {

  @Input() eventCs: EventCS;
  @Input() evNk: string;
  @Input() chargingStation: ChargingStation;

  isReserved = false;

  constructor(private reservationService: ReservationService) { }

  ngOnInit() { }

  public makeReservation() {
    this.reservationService.makeReservation(this.evNk, this.eventCs.nk)
      .subscribe(() => {
        this.isReserved = true;
      }, (error) => {
        console.error(error);
      });
  }
}
