import * as faker               from 'faker';

import { User }                       from '../services/auth.service';
// import { SearchStationsService }      from '../services/search-stations.service'
import { ChargingStation }      from '../data_classes/chargingStation';


export class UserFactory {
  static create(data?: object): User {
    return User.create(Object.assign({
      id        : faker.random.number(),
      username  : faker.internet.email(),
      first_name: faker.name.firstName(),
      last_name : faker.name.lastName(),
      group     : 'DRIVER',

    }, data));
  }
}

export class CStationFactory {
  static create(data?: object): ChargingStation {
    return ChargingStation.create(Object.assign({
      id    : faker.random.uuid(),
      nk    : faker.random.alphaNumeric(32),
      name  : faker.name.firstName()

      // pick_up_address: faker.address.streetAddress(),
      // drop_off_address: faker.address.streetAddress(),
      // status: 'REQUESTED',
      // driver: UserFactory.create({group: 'driver'}),
      // rider: UserFactory.create()
    }, data));
  }
}