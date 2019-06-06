import { Component, OnInit }    from '@angular/core';
import { AuthService }    from '../../services/auth.service';
import { User } from '../../data_classes/user';

@Component({
  selector: 'app-landing',
  templateUrl: './landing.component.html',
  styleUrls: ['./landing.component.css']
})

export class LandingComponent {
  constructor(private authService: AuthService) {}
  getUser(): User {
    return User.getUser();
  }
  isDriver(): boolean {
    return User.isDriver();
  }
  logOut(): void {
    this.authService.logOut().subscribe(() => {}, (error) => {
      console.error(error);
    });
  }
}
