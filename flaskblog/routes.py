from flask import render_template, request, redirect, url_for, flash, abort
from flaskblog.models import User, Post, LikePost
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccount, PostForm, ResetPasswordForm, RequestResetForm
from flaskblog import app, db, bcrypt, mail
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime
import secrets
from PIL import Image
import os
import shutil
from flask_mail import Message

@app.route("/")
@app.route("/home")
def home():
    page = request.args.get("page", 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template("home.html", posts=posts)
@app.route("/register", methods=["GET","POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"your account have been created, you can able to login now ", "success")
        return redirect(url_for("home"))
    return render_template("register.html", form=form)

@app.route("/login", methods=["GET","POST"])
def login():
    
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=True)
                flash(f"your have successfully logged in", "success")
                next_page = request.args.get("next")
                if next_page:
                    return redirect(next_page)
                else:
                    return redirect(url_for("home"))
            else:
                flash(f"login unsuccessfull please check your username and email", "danger")
                return redirect(url_for("home"))
    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    logout_user()  
    return redirect(url_for("home"))
  

@app.route("/account",  methods=["GET","POST"])
@login_required
def account():
    
    posts = Post.query.filter_by(author=current_user).paginate()
    last_login =  datetime.now().strftime("%d-%m-%Y %I:%M:%S-%p")
    directory = current_user.username
    parent_directory = "flaskblog/static/profile_pics/"
    paths = parent_directory + str(directory)
    if not os.path.exists(paths):
        image_file = url_for("static", filename="profile_pics/common_dp/common.jpg")
        current_user.image_file = image_file
        db.session.commit()
        return render_template("account.html", image_file=image_file, last_login=last_login, posts=posts)
    else:      
        image_file = url_for("static", filename="profile_pics/"+ f"{str(current_user.username)}/" + current_user.image_file)
        return render_template("account.html", image_file=image_file, last_login=last_login, posts=posts)


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


@app.route("/remove-profile")
@login_required
def remove_profile():
    directory = current_user.username
    parent_directory = "flaskblog/static/profile_pics/"
    paths = parent_directory + str(directory)
    if not os.path.exists(paths):
        flash("you have not updated your profile image to remove it", "danger")
        return redirect(url_for("home"))
    else:   
        dir = current_user.username
        path = os.path.join(parent_directory, dir)
        shutil.rmtree(path)
        return redirect(url_for("account"))


def save_post_image(form_picture):
    
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    directory = current_user.username
    parent_directory = "flaskblog/static/post_picture/"
    paths = parent_directory + str(directory)
    
    if not os.path.exists(paths):
        os.makedirs(paths, mode=0o666)
    picture_path = os.path.join(app.root_path, "static/post_picture/"+ str(directory), picture_fn) 
   
    
    basewidth = 300
    image = Image.open(form_picture)
    wpercent = (basewidth/float(image.size[0]))
    hsize = int((float(image.size[1])*float(wpercent)))
    image = image.resize((basewidth, hsize), Image.ANTIALIAS)
    image.save(picture_path)
    
    return picture_fn        

@app.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        if form.post_image.data:
            picture_file = save_post_image(form.post_image.data)
            post = Post(content=form.content.data, author=current_user, post_image=picture_file)
            db.session.add(post)
            db.session.commit()
        else:
            post = Post(content=form.content.data, author=current_user)
            db.session.add(post)
            db.session.commit()
        flash("post created", "success")
        return redirect(url_for("home"))
    return render_template("new_post.html", form=form)


@app.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def edit(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if request.method == "POST":
        if form.validate_on_submit:
            post.content = form.content.data
            db.session.commit()
            flash("your post has been upadted", "success")
            return redirect(url_for("home"))
    elif request.method == "GET":
        form.content.data = post.content
    return render_template("update_post.html", form=form)


@app.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("your post has been deleted", "success")
    return redirect(url_for('home'))


@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get("page", 1, type=int) 
    user = User.query.filter_by(username=username).first_or_404()  #if we give current_user object it will show current user's post, so we want to filter by username
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template("user_posts.html", posts=posts, user=user)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message("Password reset request", sender="demoappflask@gmail.com", recipients=[user.email])
    msg.body =f"""
To reset your password visit the following
link {url_for("reset_token", token=token, _external=True)}  
if you did not make he request then simply ignore it"""
      
    mail.send(msg)

@app.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect('home')
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email is sent with to reset your password check your inbox", "primary")
        return redirect(url_for("home"))
    return render_template("reset_request.html",  form=form)



@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    user = User.verify_reset_token(token)
    if user is None:
        flash("that is an invalid or expired token", "warning")
        return redirect(url_for("reset_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")          
        user.password = hashed_password
        db.session.commit()
        flash(f"your password has successfully changed please login ", "success")
        return redirect(url_for("home"))
    return render_template("reset_token.html", form=form)

#errors

@app.errorhandler(404)
def error_404(error):
    return render_template("404.html"), 404

@app.errorhandler(403)
def error_403(error):
    return render_template("403.html"), 403

@app.errorhandler(500)
def error_500(error):
    return render_template("500.html"), 500