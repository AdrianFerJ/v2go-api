import { Component, OnInit }    from '@angular/core';
import { SearchStationsService} from '../../services/search-stations.service'

@Component({
  selector: 'app-driver-home-map',
  templateUrl: './driver-home-map.component.html',
  styleUrls: ['./driver-home-map.component.css']
})
export class DriverHomeMapComponent implements OnInit {

  constructor() { }

  ngOnInit() {
    SearchStationsService
  }

}
