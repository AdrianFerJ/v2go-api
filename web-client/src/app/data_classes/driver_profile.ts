import { User } from '../data_classes/user';
import { Vehicle } from './vehicle';
import { Reservation } from './reservation';

export interface DriverInfo {
  user: User;
  evs: Vehicle[];
  reservations: Reservation[];
}
