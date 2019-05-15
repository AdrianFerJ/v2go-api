import { Component, OnInit }      from '@angular/core';
import { ActivatedRoute }         from '@angular/router';
import { SearchStationsService }  from '../../services/api.service'
import { STATIONS}                from '../../data_classes/mock_cs'
import { ChargingStation }        from '../../data_classes/chargingStation';
import { Observable }             from 'rxjs';

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
  //45.582745599999996 -71.57268479999999
  xlat = 45.508048;
  xlng = -73.568025;
  zoom = 13;
  markers: Marker[];
  driver: Marker;

  constructor(
    private searchService: SearchStationsService,
    // Use ActivateRout (from StationsListResolver)
    private route: ActivatedRoute,
  ) { }

  ngOnInit() {

    this.searchStationsNearMe();

    // Get CS near me USING RESOLVER. 
    // TODO UPDATE router to pass user location (currently using hardcoded value)
    // this.route.data
    //   .subscribe((data: {stationsList: ChargingStation[]}) => this.stationsList = data.stationsList);

    // Display CS in map
    // if (this.stationsList) {
    //   console.log('*'.repeat(200), this.stationsList)
    //   for (let station of this.stationsList) {
    //     // this.markers = [
    //     //   new Marker(station.lat, station.lng, 'STATION X')
    //     // ];
    //   } 
    // } else {
    //   console.log('?'.repeat(10), "NO stationsList!!")
    // }

    //TODO Get user this.driver (OR this.User) = User.getUser();
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
      this.xlat = position.coords.latitude;
      this.xlng = position.coords.longitude;
      // Get stations near User's location
      this.findStations(this.xlat, this.xlng);
    }, error => { 
      //TODO this should be a notification
      console.log(error);
      // Get stations near default MTL coords
      this.findStations(this.xlat, this.xlng);
    });
  }

  /**
   *  Method to create a marker and display user locaiton on map
   */
  displayUser(position) {
    this.xlat = position.coords.latitude;
    this.xlng = position.coords.longitude;
    
    // Display Driver
    // this.driver = new Marker(this.lat, this.lng, 'D')
    this.markers = [
      new Marker(this.xlat, this.xlng, 'D')
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
const getCurrentPosition = new Observable(observer => {
  if ('geolocation' in navigator) {
    navigator.geolocation.getCurrentPosition(
      position => { 
        observer.next(position); 
      }, 
      navigatorError => { observer.error(navigatorError) },
      {maximumAge:600000, timeout:5000, enableHighAccuracy: true} 
    );
  } else {
    observer.error('Geolocation not available');
  }
  // observer.complete();
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
    debugger;
  } else {
    error('Geolocation not available');
  }
  // When the consumer unsubscribes, clean up data ready for next subscription.
  return {unsubscribe() { navigator.geolocation.clearWatch(watchId); }};
});
