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

  stationsList: ChargingStation[];

  constructor(private searchCSservice: SearchStationsService) { }

  ngOnInit() {
    this.findStations();
  }

  // findStations(): void {
  //   this.stationsList = this.searchCSservice.findStations();
  // }

  // Method uses searchService to call api/find-station
  // .. the Service returns an observable, subscribing to it emit the array of CSs
  findStations(): void {
    this.searchCSservice.findStations()
        .subscribe(stationsList => this.stationsList = stationsList);
  }

}
