from datetime import datetime     # select = selects the posts in one go
from flaskblog import db, login_manager, app              #joined = the query of two table will be combined and the relationship will return posts with no query
from flask_login import UserMixin       
from itsdangerous import TimedJSONWebSignatureSerializer as serializer
                                                 # dynamic = want to select all ,(we want to use (all())). we can also use filter
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="common.jpg")
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship("Post", backref="author", lazy=True)  
    posts_liked = db.relationship("LikePost", backref="author_id_like", lazy=True) 
    
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

    def __repr__(self):
        return f"{self.username}, {self.email}, {self.password}, posts posted by him{self.posts}, number of posts liked by him{self.posts_liked}"                                                              
                                                                    

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    post_image = db.Column(db.String(100), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    post_like = db.relationship("LikePost", backref="author_post_id", lazy=True)

    def __repr__(self):
         return f"{self.content}, this post was posted by {User.query.filter_by(id=self.user_id).first().username}, this post was liked by {User.query.filter_by(id=self.post_like).first().username}"

class LikePost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)
    
    def __repr__(self):
        return f"{self.post_id} <- This posts was posted by {User.query.filter_by(id=self.post_id).first().username}  and this post was liked by {User.query.filter_by(id=self.user_id).first().username}"
     