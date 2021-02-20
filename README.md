# social_webproject-python_flask PLATO


Project plato is a python web development project done with flask library, the specification in the flask extension library were used in this project.
I have used bootstap, css, javascript, fontawesome and some other extension to design frontend and backend is completely developed by python. 
Read below to know more :point_down:

# Features in this website

* Secured registeration and Login
* User account security
* features in account page
* User post accessibility
* Password reset capability bt email
* Backend works

# Secured Registeration

![alt text](https://github.com/sainath-murugan/social_webproject-python_flask/blob/main/plato/register.JPG)

![alt text](https://github.com/sainath-murugan/social_webproject-python_flask/blob/main/plato/login_fail.JPG)

Python's flask extension gives a great capability to manage login and register page. I have used `Flask-WTF` to manage login and register forms and `Flask-WTF` protects the login and register page from `CSRF` attack by using `hidden_tag()` feature. The `wtforms.validators` module in `wtforms` provides Classes like `DataRequired`, `Length`, `Email`, `EqualTo` and `ValidationError` to manage forms. The classes checks for valid username, Email and password in forms and gives alert for the user if there is any validation error. 

# User account security

![alt text](https://github.com/sainath-murugan/social_webproject-python_flask/blob/main/plato/database.JPG)

 user's account security is one of the important thing to manage.  Flask library gives the flexibility to manage it. I have used `Bcrypt` class in `flask_bcrypt` to store the `hash` value of the password in the database. so, the user's password can't be access by anybody in the database.
 
 ```python
 
