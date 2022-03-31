from datetime import datetime

from Blog_website import db, login_manager, bcrypt
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(40), unique = True)
    email = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    blogs = db.relationship('Blog', backref='blog_author', lazy='dynamic') 
    comments = db.relationship('Comment', backref='comment_author', lazy=True)

    def __repr__(self):
        return f'User id:{self.id} is:{self.name}'

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def verify_password(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)


class Blog(UserMixin, db.Model):
    __tablename__ = 'blogs'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(length=30), nullable=False, unique=True)
    content = db.Column(db.Text(), nullable=False)
    blog_date = db.Column(db.DateTime(), default=datetime.utcnow())
    author_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    blog_comments = db.relationship('Comment', backref='comment_id', lazy='dynamic')


    def __repr__(self):
        return f'Blog id:{self.id} is from:{self.author_id}'


class Comment(UserMixin, db.Model):
    __tablename__= 'comments'
    id= db.Column(db.Integer(), primary_key=True)
    body = db.Column(db.Text(), nullable=False)
    blog_date = db.Column(db.DateTime(), default=datetime.utcnow())
    author_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    blog_id = db.Column(db.Integer(), db.ForeignKey('blogs.id'))


    def __repr__(self):
        return f'Blog id:{self.id} is from:{self.author_id}'
