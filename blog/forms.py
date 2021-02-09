from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed,FileRequired
from wtforms import StringField,PasswordField,SubmitField,BooleanField,TextAreaField,IntegerField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from blog.models import User,Category,Book,Customerregister
from flask_login import current_user
class RegistrationForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    confirm_password=PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField('Sign Up')

    def validate_username(self,username):
        user=User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('The Username Exist')
    
    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('The Email Exist')

class LoginForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    submit=SubmitField('Login')




class UpdateAccountForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
    email=StringField('Email',validators=[DataRequired(),Email()])
    image=FileField('Update Profile',validators=[FileAllowed(['jpg','png'])])
    submit=SubmitField('Update')

    def validate_username(self,username):
        if username.data != current_user.username:
            user=User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('The Username Exist')
    
    def validate_email(self,email):
        if email.data !=current_user.email:
            user=User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('The Email Exist')
class BookForm(FlaskForm):
    name=StringField('Name',validators=[DataRequired()])
    page=IntegerField('Page',validators=[DataRequired()])
    price=IntegerField('Price',validators=[DataRequired()])
    much=IntegerField('How Much',validators=[DataRequired()])
    jold=IntegerField('jold',default=0)
    desc=TextAreaField('Description',validators=[DataRequired()])
    image1=FileField('Image 1',validators=[FileRequired(),FileAllowed(['jpg','png','gif','jpeg'])])
    submit=SubmitField('Add')

class CategoryForm(FlaskForm):
    name=StringField('Name',validators=[DataRequired()])
    submit=SubmitField('Post')
    def validate_name(self, name):
        if name.data != self.name:
            category = Category.query.filter_by(name=self.name.data).first()
            if category is not None:
                raise ValidationError('Please use a different name.')

class CustomerregisterForm(FlaskForm):
    username=StringField('Name',validators=[DataRequired()])
    lastname=StringField('LastName',validators=[DataRequired()])
    phone=IntegerField('Phone',validators=[DataRequired()])
    add=TextAreaField('Addrass',validators=[DataRequired()])
    image1=FileField('Image 1',validators=[FileRequired(),FileAllowed(['jpg','png','gif','jpeg'])])
    nic=IntegerField('Nic',validators=[DataRequired()])
    hour=IntegerField('Hour',validators=[DataRequired()])
    day=IntegerField('Day',validators=[DataRequired()])
    month=IntegerField('Month',validators=[DataRequired()])
    year=IntegerField('Year',validators=[DataRequired()])
    price=IntegerField('Price',validators=[DataRequired()])
    submit=SubmitField('Add')

   

class RentbookcustomerForm(FlaskForm):
    nic=IntegerField('Nic',validators=[DataRequired()])
    hour=IntegerField('Hour',validators=[DataRequired()])
    day=IntegerField('Day',validators=[DataRequired()])
    month=IntegerField('Mont',validators=[DataRequired()])
    year=IntegerField('Year',validators=[DataRequired()])
    bookname=StringField('Book Name',validators=[DataRequired()])
    bookpage=StringField('BookPage',validators=[DataRequired()])
    submit=SubmitField('Add')