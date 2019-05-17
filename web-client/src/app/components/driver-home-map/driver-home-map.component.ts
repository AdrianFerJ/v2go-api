import { Component, OnInit } from '@angular/core';
import { SearchStationsService } from '../../services/api.service';
import { ChargingStation } from '../../data_classes/chargingStation';
import { Observable } from 'rxjs';

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
  // Default values for Point of Interest (poi) coordinates is MTL
  poiLat: number = 45.508048;
  poiLng: number = -73.568025;
  zoom = 13;
  markers: Marker[];
  driver: Marker;

  constructor(
    private searchService: SearchStationsService,
  ) { }

  ngOnInit() {
    this.searchStationsNearMe();
  }

  /**
   * Method uses searchService (observer) to call api/find-station. Returns an array of CSs
   */
  findStations(lat, lng): void {
    this.searchService.findStations(lat, lng)
      .subscribe(stationsList => {
        this.stationsList = stationsList;
      });
  }
  /**
   * Method get stations near User's location (navigator, if not avail, use MTL coords)
   * then, displays user ans CS on map.
   */
  searchStationsNearMe(): void {
    getCurrentPosition.subscribe( position => {
      console.log('## POSITION (52): ', position);
      this.poiLat = position.coords.latitude;
      this.poiLng = position.coords.longitude;
      // Get stations near User's location
      this.findStations(this.poiLat, this.poiLng);
    }, error => {
      console.log('# ERROR at searchStationsNearMe(). Message: ', error);
      // Get stations near default MTL coords
      this.findStations(this.poiLat, this.poiLng);
    });
  }

  /**
   *  Method to create a marker and display user locaiton on map
   */
  displayUser(position) {
    this.poiLat = position.coords.latitude;
    this.poiLng = position.coords.longitude;
    // Display Driver
    // this.driver = new Marker(this.lat, this.lng, 'D')
    this.markers = [
      new Marker(this.poiLat, this.poiLng, 'D')
    ];
    // let location = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
    // this.map.panTo(location);

    // if (!this.marker) {
    //   this.marker = new google.maps.Marker({
    //     position: location,
    //     map: this.map,
    //     title: 'Got you!'
    //   });
    // }
    // else {
    //   this.marker.setPosition(location);
    // }
  }
}

/**
 *  Observable gets current user geolocation from navigator.
 */
const getCurrentPosition = new Observable<Position>(observer => {
  if ('geolocation' in navigator) {
    navigator.geolocation.getCurrentPosition(
      position => {
        console.log('## POSITION (98): ', position);
        observer.next(position);
      },
      navigatorError => { observer.error(navigatorError); },
      {maximumAge: 600000, timeout: 5000, enableHighAccuracy: true}
    );
  } else {
    observer.error('Geolocation not available');
  }
});

/**
 * Observable streams user geolocation from navigator.
 * Check: https://angular.io/guide/observables#basic-usage-and-terms
 */
const streamUserPosition = new Observable((observer) => {
  // Get the next and error callbacks. These will be passed in when
  // the consumer subscribes.
  const {next, error} = observer;
  let watchId;
  // Simple geolocation API check provides values to publish
  if ('geolocation' in navigator) {
    watchId = navigator.geolocation.watchPosition(next, error);
  } else {
    error('Geolocation not available');
  }
  // When the consumer unsubscribes, clean up data ready for next subscription.
  return {unsubscribe() { navigator.geolocation.clearWatch(watchId); }};
});
