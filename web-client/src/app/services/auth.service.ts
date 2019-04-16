import { Injectable } from '@angular/core';

export class User {
  // Data model to store user info (a JSON-serialized string returned by API) in the UI
  constructor(
    public id?: number,
    public username?: string,
    public first_name?: string,
    public last_name?: string,
    public group?: string,
    public photo?: any
  ) {}

  // Convenience method to handle the conversion from JSON to data object 
  static create(data: any): User { 
    return new User(
      data.id,
      data.username,
      data.first_name,
      data.last_name,
      data.group,
      data.photo
    );
  }
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  constructor() { }
}