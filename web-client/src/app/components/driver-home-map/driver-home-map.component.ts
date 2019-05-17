import { Component, OnInit }    from '@angular/core';
import { ActivatedRoute }       from '@angular/router';
import { SearchStationsService} from '../../services/search-stations.service'
import { STATIONS}              from '../../data_classes/mock_cs'
import { ChargingStation }      from '../../data_classes/chargingStation';

class Marker {
  constructor(
    public lat: number,
    public lng: number,
    public label?: string
  ) {}
}

@Component({
  selector: 'app-driver-home-map',
  templateUrl: './driver-home-map.component.html',
  styleUrls: ['./driver-home-map.component.css']
})
export class DriverHomeMapComponent implements OnInit {

  stationsList: ChargingStation[];

  lat = 45.5070394;
  lng = -73.5651293;
  xlat= 0;
  xlng= 0;
  zoom = 13;
  markers: Marker[];

  constructor(
    private searchService: SearchStationsService,
    // Use ActivateRout (from StationsListResolver)
    private route: ActivatedRoute,
    //TODO add googleMapsService
    // private googleMapsService: GoogleMapsService,
  ) { }

  ngOnInit() {
    // Get User location from browser
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition((position: Position) => {
        this.xlat = position.coords.latitude;
        this.xlng = position.coords.longitude;
        console.log('### USER LAT, LNG:', this.xlat, this.xlng)
        this.markers = [
          new Marker(this.lat, this.lng, 'D')
        ];
      });
    }

    // Get CS near me (Should pass my location)
    // this.findStations();
    this.route.data
      .subscribe((data: {stationsList: ChargingStation[]}) => this.stationsList = data.stationsList);

    // Display CS in map
    console.log('*'.repeat(200), this.stationsList)
    if (this.stationsList) {
      for (let station of this.stationsList) {
        console.log(station.nk); 
        // this.markers = [
        //   new Marker(station.lat, station.lng, 'STATION X')
        // ];
      } 
    }

    //TODO Get user this.driver (OR this.User) = User.getUser();
  }

  // findStations() method uses searchService to call api/find-station
  // .. the Service returns an observable, subscribing to it emit the array of CSs
  findStations(): void {
    this.searchService.findStations()
        .subscribe(stationsList => this.stationsList = stationsList); 
  }

}
