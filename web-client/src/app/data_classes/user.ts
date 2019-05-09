export class User {
  // Data model to store user info (a JSON-serialized string returned by API) in the UI
  constructor(
    public id?: number,
    public username?: string,
    public first_name?: string,
    public last_name?: string,
    public group?: string,
  ) {}

  // Convenience method to handle the conversion from JSON to data object
  static create(data: any): User {
    return new User(
      data.id,
      data.username,
      data.first_name,
      data.last_name,
      data.group,
    );
  }
  // Convinience method to check if user is logged in
  static getUser(): User {
    const userData = localStorage.getItem('v2go.user');
    if (userData) {
      return User.create(JSON.parse(userData));
    }
    return null;
  }
  // Determines whether the user belongs to the group (DRIVER)
  static isDriver(): boolean {
    const user = User.getUser();
    if (user === null) {
      return false;
    }
    return user.group === 'driver';
  }
}
