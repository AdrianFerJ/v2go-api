import { ChargingStation }       from './chargingStation';
import { CStationFactory }       from '../testing/factories';

export const STATIONS: ChargingStation[] = [
  CStationFactory.create(), 
  CStationFactory.create()
//   { id: 11, nk: ???, name: 'Mr. Nice' },
//   { id: 12, nk: ???, name: 'Narco' },
];