from blog import db,app
from datetime import datetime
from blog import login_manager
from flask_login import UserMixin
from flask_security import Security, SQLAlchemyUserDatastore,UserMixin, RoleMixin
from flask_security.forms import RegisterForm
from wtforms.validators import ValidationError

from wtforms import StringField

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
#Roles And User Relationship
roles_users = db.Table('roles_users',db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))
#Role For Admin
class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),unique=True)
    email=db.Column(db.String(120),unique=True,nullable=False)
    image=db.Column(db.String(20),nullable=False,default='zero.jpg')
    password=db.Column(db.String(60),nullable=False)
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,backref=db.backref('users', lazy='dynamic'))
    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image}')"

class ExtendedRegisterForm(RegisterForm):
    username=StringField('username')
    def validate_username(self,username):
        user=User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('The Username Exist')
# Setup For Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore,register_form=ExtendedRegisterForm)


class Book(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(80),nullable=False)
    page=db.Column(db.String(80),nullable=False)
    price=db.Column(db.Integer,nullable=False)
    much=db.Column(db.Integer,nullable=False)
    jold=db.Column(db.Integer,nullable=False,default=0)
    desc=db.Column(db.Text,nullable=False)

    category_id=db.Column(db.Integer,db.ForeignKey('category.id'))
    category=db.relationship('Category',backref=db.backref('categories',lazy=True))

    date=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    image1=db.Column(db.String(150),nullable=False,default='image.jpg')
    def __repr__(self):
        return f"Book('{self.name}','{self.price}')"


class Category(db.Model):
    id=db.Column(db.Integer,primary_key=True,unique=True)
    name=db.Column(db.String(20),nullable=False)
    def __repr__(self):
        return f"Category('{self.name}')"


class Customerregister(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20))
    lastname=db.Column(db.String(100))
    phone=db.Column(db.Integer,nullable=False)
    add=db.Column(db.Text,nullable=False)
    image1=db.Column(db.String(150),nullable=False,default='image.jpg')
    nic=db.Column(db.Integer,nullable=False)
    hour=db.Column(db.Integer,nullable=False)
    day=db.Column(db.Integer,nullable=False)
    month=db.Column(db.Integer,nullable=False)
    year=db.Column(db.Integer,nullable=False)
    price=db.Column(db.Integer,nullable=False)
    date=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)


class Rentbookcustomer(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    nic=db.Column(db.Integer,nullable=False)
    hour=db.Column(db.Integer,nullable=False)
    day=db.Column(db.Integer,nullable=False)
    month=db.Column(db.Integer,nullable=False)
    year=db.Column(db.Integer,nullable=False)
    bookname=db.Column(db.String(100),nullable=False)
    bookpage=db.Column(db.Integer,nullable=False)
    date=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)

        