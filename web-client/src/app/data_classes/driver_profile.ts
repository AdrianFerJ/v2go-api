import { User } from '../services/auth.service';
import { Vehicle } from './vehicle';
import { Reservation } from './reservation';

export interface DriverInfo {
  user: User;
  evs: Vehicle[];
  reservations: Reservation[];
}
