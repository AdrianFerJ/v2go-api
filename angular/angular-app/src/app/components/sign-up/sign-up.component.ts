import { Component } from '@angular/core';
import { Router } from '@angular/router';

import { AuthService } from '../../services/auth.service';

class UserData {
  constructor(
    public username?: string,
    public firstName?: string,
    public lastName?: string,
    public password1?: string,
    public password2?: string
    // public group?: string,
  ) {}
}

@Component({
  selector: 'app-sign-up',
  templateUrl: './sign-up.component.html',
  styleUrls: ['./sign-up.component.css']
})
export class SignUpComponent {
  user: UserData = new UserData();
  constructor(
    private router: Router,
    private authService: AuthService
  ) {}

  onSubmit(): void {
    this.authService.signUp(
      this.user.username,
      this.user.firstName,
      this.user.lastName,
      this.user.password1,
      this.user.password2
      // this.user.group,
    ).subscribe(() => {
      debugger
      this.router.navigateByUrl('/log-in');
    }, (error) => {
      console.error(error);
    });
  }
}