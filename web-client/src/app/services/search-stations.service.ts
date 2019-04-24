import { Injectable }   from '@angular/core';

import { User }         from './auth.service';

export class ChargingStation {
  constructor(
    public id?: number,
    public nk?: string,
    public name?: string,
    public external_id?: string,
    public charge_level?: string,
    public tarif_text?: string,
    public address?: string,
    public city?: string,
    public province?: string,
    public country?: string,
    public postal_code?: string,
    public lat?: number,
    public lng?: number,
    public geo_location?: any,
    public created?: string,
    public updated?: string,
    public cs_host?: number,
    public calendar?: number,
  ) {}

    
}

@Injectable({
  providedIn: 'root'
})
export class SearchStationsService {

  constructor() { }
}
