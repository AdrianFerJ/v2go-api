import { Component, OnInit }    from '@angular/core';
import { SearchStationsService} from '../../services/search-stations.service'
import { STATIONS}              from '../../data_classes/mock_cs'
import { ChargingStation }      from '../../data_classes/chargingStation';

@Component({
  selector: 'app-driver-home-map',
  templateUrl: './driver-home-map.component.html',
  styleUrls: ['./driver-home-map.component.css']
})
export class DriverHomeMapComponent implements OnInit {

  stationsList = STATIONS;

  constructor() { }

  ngOnInit() {
    // SearchStationsService
  }

}
