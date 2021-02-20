# social_webproject-python_flask PLATO


Project plato is a python web development project done with flask library, the specification in the flask extension library were used in this project.
I have used bootstap, css, javascript, fontawesome and some other extension to design frontend and backend is completely developed by python. 
Read below to know more :point_down:

# Features in this website

* Secured registeration and Login
* User account security
* features in account page
* User post accessibility
* Password reset capability by email
* Backend works

# Secured Registeration

![alt text](https://github.com/sainath-murugan/social_webproject-python_flask/blob/main/plato/register.JPG)

![alt text](https://github.com/sainath-murugan/social_webproject-python_flask/blob/main/plato/login_fail.JPG)

Python's flask extension gives a great capability to manage login and register page. I have used `Flask-WTF` to manage login and register forms and `Flask-WTF` protects the login and register page from `CSRF` attack by using `hidden_tag()` feature. The `wtforms.validators` module in `wtforms` provides Classes like `DataRequired`, `Length`, `Email`, `EqualTo` and `ValidationError` to manage forms. The classes checks for valid username, Email and password in forms and gives alert for the user if there is any validation error. 

# User account security

![alt text](https://github.com/sainath-murugan/social_webproject-python_flask/blob/main/plato/database.JPG)

 user's account security is one of the important thing to manage.  Flask library gives the flexibility to manage it. I have used `Bcrypt` class in `flask_bcrypt` to store the `hash` value of the password in the database. so, the user's password can't be access by anybody in the database.
 
 ```python
  if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
 ```
 
 # features in account page
 
 ![alt text](https://github.com/sainath-murugan/social_webproject-python_flask/blob/main/plato/account.JPG)
 
  As it was a clone of social website i have developed some specification in user account page to increase the accessibilty to user.
  The account page dispalys the last visit of the user in the website and also displays the total post posted by the user in the current account. 
 ```python
    last_login =  datetime.now().strftime("%d-%m-%Y %I:%M:%S-%p")
 ```
The total post posted by the user is generated by the pagination object

 ```python
   posts = Post.query.filter_by(author=current_user).paginate()
 ```
 ![alt text](https://github.com/sainath-murugan/social_webproject-python_flask/blob/main/plato/remove%20post.JPG)
 
 When a new user is registed in PLATO the account page Provied a default image to the user. The user can aslo update his profile and aslo can remove his current profile when ever he/she needs. so when the current profile removed the default image will be diaplayed in account page.
 
  ```python
  if not os.path.exists(paths):
        image_file = url_for("static", filename="profile_pics/common_dp/common.jpg")
        current_user.image_file = image_file
        db.session.commit()
        return render_template("account.html", image_file=image_file, last_login=last_login, posts=posts)
    else:      
        image_file = url_for("static", filename="profile_pics/"+ f"{str(current_user.username)}/" + current_user.image_file)
        return render_template("account.html", image_file=image_file, last_login=last_login, posts=posts)
 ```
 I have used  `PIL` library in the python to resize the image. And i have used `secrets` library to  `hash` the image name and store the  `hash` name in the database and orginal JPG image will be stored in i folder using  `OS` library in python. This will reduce the buffering in the database. I have used `SQLAlchemy` to manage database.
 
```python
 def save_picture(form_picture):
    
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    directory = current_user.username
    parent_directory = "flaskblog/static/profile_pics/"
    paths = parent_directory + str(directory)
    
    if not os.path.exists(paths):
        os.makedirs(paths, mode=0o666)
    picture_path = os.path.join(app.root_path, "static/profile_pics/"+str(directory), picture_fn) 
   
    
    output_size = (800, 800) 
    image_sizing = Image.open(form_picture)
    image_sizing.thumbnail(output_size)
    image_sizing.save(picture_path)
    
    return picture_fn
 ```
# User post accessibility

The current user can modify any changes in his post by eding or deleting it. But the current user can't edit or delete the post of other users. The database checks for correct author of the post.

 ![alt text](https://github.com/sainath-murugan/social_webproject-python_flask/blob/main/plato/user_post.JPG)
 
 The delete and edit option is only visible for the current user. It will give more flexibility to the current user
 
 ![alt text](https://github.com/sainath-murugan/social_webproject-python_flask/blob/main/plato/new_post.JPG)
 ![alt text](https://github.com/sainath-murugan/social_webproject-python_flask/blob/main/plato/edit%20post.JPG)
 
# security for user's post

 ![alt text](https://github.com/sainath-murugan/social_webproject-python_flask/blob/main/plato/403.JPG)
 
 
```python
def edit(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
        
        
def delete(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
```


If the current user tries to edit or delete the other user's post, the website will throw a 403 forbidden error in browser. This specification can be achived by `abort` function in flask. so the users post in the database can be secured

# Password reset capability bt email
At any time the user can forgot his/her password so, the password reseting capability is developed in this project. `flask_mail` library provides `Mail` class it is used to send automatic mail from the server.

```python
app.config["MAIL_SERVER"] = "smtp.googlemail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
mail = Mail(app)
```

The link for the password reset it to be validate only for 0-30 min to ensure security. so `itsdangerous` module in `flask` provides `TimedJSONWebSignatureSerializer` class it generates a hashed link. The link validates only for 30 minuted, after 30 minutes it expire automatically. so no other person can use it after 30 minutes including the user also.


```python
 def get_reset_token(self, expires_sec=1800):
        s = serializer(app.config['SECRET_KEY'])
        return s.dumps({"user_id": self.id}).decode("utf-8")
    
    @staticmethod
    def verify_reset_token(token):
        s = serializer(app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token)["user_id"]
        except:
            return None
        return User.query.get(user_id)
```
After changing the password the `hashed` data of the password is stored in database for the user.

 ![alt text](https://github.com/sainath-murugan/social_webproject-python_flask/blob/main/plato/password%20Reset.JPG)
 ![alt text](https://github.com/sainath-murugan/social_webproject-python_flask/blob/main/plato/password%20Reset_page.JPG)
 
 # Backend Works
 Backend is always a technical field to concentrate while develop a website. In plato i have increased some features in backend proccessing to manage the website easily for the administrator
 
 
 ```python
def save_picture(form_picture):
    
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    directory = current_user.username
    parent_directory = "flaskblog/static/profile_pics/"
    paths = parent_directory + str(directory)
    
    if not os.path.exists(paths):
        os.makedirs(paths, mode=0o666)
    picture_path = os.path.join(app.root_path, "static/profile_pics/"+str(directory), picture_fn) 
   
    
    output_size = (800, 800) 
    image_sizing = Image.open(form_picture)
    image_sizing.thumbnail(output_size)
    image_sizing.save(picture_path)
    
    return picture_fn

@app.route("/update_account",  methods=["GET","POST"])
@login_required
def update_account():
   
    form = UpdateAccount()
    if form.validate_on_submit():
       
        oldname = current_user.username
        parent_directory_1 = "flaskblog/static/profile_pics/"
        parent_directory_2 = "flaskblog/static/post_picture/"
        old_path_1 = parent_directory_1 + str(oldname)
        old_path_2 = parent_directory_2 + str(oldname)
        current_user.username = form.username.data
        new_path_1 = parent_directory_1 + str(current_user.username)
        new_path_2 = parent_directory_2 + str(current_user.username)
        if os.path.exists(old_path_1):       
            os.rename(old_path_1, new_path_1) 
        if os.path.exists(old_path_2):       
            os.rename(old_path_2, new_path_2)      
        current_user.email = form.email.data
        if form.picture.data:  
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file       
        db.session.commit()
        flash("your account has been updated", "success")
        return redirect(url_for("home"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    directory = current_user.username
    parent_directory = "flaskblog/static/profile_pics/"
    paths = parent_directory + str(directory)
    if not os.path.exists(paths):
        image_file = url_for("static", filename="profile_pics/common_dp/common.jpg")
        current_user.image_file = image_file
        db.session.commit()
        return render_template("update_account.html", form=form, image_file=image_file)
    else:
       image_file = url_for("static", filename="profile_pics/"+ f"{str(current_user.username)}/" + current_user.image_file)
       return render_template("update_account.html", form=form, image_file=image_file)
```
If the user is trying to update his profile picture, I have used `OS` module in python to create a seperate directory for him to store his profile pic. The directory is created automatically by `OS` module in the name of the current user's username and the profile pic address is stored in database. so python crabs the address from the database and displays the  profile in the website.

The important think to be noticed is, that the profile pic directory is created in the name of the current user's username. so, whenever the user updates his username, the database will commit the change. so the current user's directory name also to be updated. so I have also developed the code for that, whenever the user change his username his directories name is also changed. This technique is used in post also, `OS` creates a seperate folder for the user to store the post. The image's size to be stored in server need to be reduced, it is done by `PIL` Library in python.

  ```python
  {% if post.author.image_file ==  "/static/profile_pics/common_dp/common.jpg" %}
              <img id="image" class="rounded-circle article-img"  src="{{  url_for('static', filename='profile_pics/common_dp/common.jpg') }}">           
            {% elif post.author.image_file ==  "common.jpg" %}
              <img id="image" class="rounded-circle article-img"  src="{{  url_for('static', filename='profile_pics/common_dp/common.jpg') }}">    
            {% elif post.author.image_file %}
              <img id="image" class="rounded-circle article-img"  src="{{  url_for('static', filename='profile_pics/'+ post.author.username + '/'+  post.author.image_file) }}">
            {% endif %}
 ```           
 # seperate folder for post
  ![alt text](https://github.com/sainath-murugan/social_webproject-python_flask/blob/main/plato/post%20data.JPG)
 # seperate folder for Profile
  ![alt text](https://github.com/sainath-murugan/social_webproject-python_flask/blob/main/plato/post%20file.JPG)
  
  # Post 
  
  The user can post image and content seperatley, the image file posted is displayed by some `Bootstrap class`, to align it correctly
  
   ![alt text](https://github.com/sainath-murugan/social_webproject-python_flask/blob/main/plato/home.JPG)
   ![alt text](https://github.com/sainath-murugan/social_webproject-python_flask/blob/main/plato/home_image.JPG)
   
   
   # File allowed
   
  ```python
   class PostForm(FlaskForm):

    content = TextAreaField("write something", validators=[DataRequired()])
    post_image = FileField(validators=[FileAllowed(["jpg", "png"])])
    submit = SubmitField("Post")
  ```
   With the help of `FileAllowed` class in `flask_wtf.file` extension, It only `png` and `JPG` files to be uploaded by the users, if other files are tried to uploded by the user it will show the error message in the browser.
   
   ![alt text](https://github.com/sainath-murugan/social_webproject-python_flask/blob/main/plato/file_allowed.JPG)
   
   
