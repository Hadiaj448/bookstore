from flask import render_template,redirect,flash,url_for,request,Response,session,current_app
from blog import app,db,photos
import secrets,os
from PIL import Image
from blog.forms import RegistrationForm,LoginForm,UpdateAccountForm,BookForm,CategoryForm,CustomerregisterForm,RentbookcustomerForm
from blog.models import User,user_datastore,Book,Category,Customerregister,Rentbookcustomer
from flask_login import login_user,logout_user
from datetime import datetime
from flask_security import  login_required,roles_accepted,current_user





@app.route('/')
def index():
    #admin_role=user_datastore.find_or_create_role('admin')
    #user_datastore.add_role_to_user(current_user,admin_role)
    #db.session.commit()
    books=Book.query.order_by(Book.date.desc())
    categories=Category.query.join(Book,(Category.id==Book.category_id)).all()
    return render_template('index.html',books=books,categories=categories)


@app.route('/category/<int:id>')
def get_category(id):
    category=Book.query.filter_by(category_id=id)    
    categories=Category.query.join(Book,(Book.id==Book.category_id)).all()
    return render_template('index.html',category=category,categories=categories)





@app.route('/addbook',methods=['GET','POST'])
@roles_accepted('admin')
@login_required
def AddBook():
    categories=Category.query.all()
    form=BookForm()
    if form.validate_on_submit():
        name=form.name.data
        page=form.page.data
        price=form.price.data
        much=form.much.data
        jold=form.jold.data
        desc=form.desc.data
        category=request.form.get('category')
        image1=photos.save(request.files.get('image1'),name=secrets.token_hex(10)+".")
        add=Book(name=name,page=page,price=price,much=much,jold=jold,desc=desc,image1=image1,category_id=category)
        db.session.add(add)
        db.session.commit()
        flash(f'Product Created Successfully','success')
        return redirect(url_for('index'))
    return render_template('addbook.html',form=form,categories=categories)

@app.route('/books',methods=['GET','POST'])
@login_required
def books():
    books=Book.query.all()
    return render_template('books.html',books=books)



@app.route('/updatebook/<int:id>',methods=['GET','POST'])
@roles_accepted('admin')
@login_required
def updatebook(id):
    book=Book.query.get_or_404(id)
    form=BookForm()
    if form.validate_on_submit():
        book.name=form.name.data
        book.page=form.page.data
        book.price=form.price.data
        book.much=form.much.data
        book.jold=form.jold.data
        book.desc=form.desc.data
        if request.files.get('image1'):
            try:
                os.unlink(os.path.join(current_app.root_path,'static/img/'+book.image1))
                book.image1=photos.save(request.files.get('image1'),name=secrets.token_hex(10)+'.')
        
            except:
                book.image1=photos.save(request.files.get('image1'),name=secrets.token_hex(10)+'.')

        flash(f'Book Successfully Updated','success')
        db.session.commit()
        return redirect(url_for('books',book_id=book.id))
    elif request.method=='GET':
        form.name.data=book.name
        form.page.data=book.page
        form.price.data=book.price
        form.much.data=book.much
        form.jold.data=book.jold
        form.desc.data=book.desc
    return render_template('updatebook.html',form=form )


@app.route('/deletebook/<int:id>',methods=['GET','POST'])
@roles_accepted('admin')
@login_required
def deletebook(id):
    book=Book.query.get_or_404(id)
    os.remove(os.path.join(current_app.root_path,'static/img/'+book.image1))
    db.session.delete(book)
    db.session.commit()
    flash('Product Successfully Deleted','success')
    return redirect(url_for('books'))

@app.route('/addcategory',methods=['GET','POST'])
@roles_accepted('admin')
@login_required
def addcategory():
    form=CategoryForm()
    if form.validate_on_submit():
        name=form.name.data
        category=Category(name=name)
        db.session.add(category)
        db.session.commit()
        flash(f'Category Created Successfully','success')
        return redirect(url_for('index'))
    return render_template('addcategory.html',form=form)

@app.route('/categories',methods=['GET','POST'])
@login_required
def categories():
    categories=Category.query.all()
    return render_template('categories.html',categories=categories)




@app.route('/updatecategory/<int:id>',methods=['GET','POST'])
@roles_accepted('admin')
@login_required
def updatecategory(id):
    form=CategoryForm()
    updatecategory=Category.query.get_or_404(id)
    category=request.form.get('name')
    if request.method=='POST':
        updatecategory.name=category
        flash(f'Category Successfully Updated','success')
        db.session.commit()
        return redirect(url_for('categories'))
    elif request.method=='GET':
        form.name.data=updatecategory.name
    return render_template('updatecategory.html',form=form)

@roles_accepted('admin')
@app.route('/deletecategory/<int:id>',methods=['GET','POST'])
@login_required
def deletecategory(id):
    deletecategory=Category.query.get_or_404(id)
    db.session.delete(deletecategory)
    db.session.commit()
    flash('Category Successfully Deleted','success')
    return redirect(url_for('categories'))


@app.route('/customer',methods=['GET','POST'])
@roles_accepted('admin')
@login_required
def customer():
    form=CustomerregisterForm()
    if form.validate_on_submit():
        username=form.username.data
        lastname=form.lastname.data
        phone=form.phone.data
        add=form.add.data
        image1=photos.save(request.files.get('image1'),name=secrets.token_hex(10)+".")
        nic=form.nic.data
        hour=form.hour.data
        day=form.day.data
        month=form.month.data
        year=form.year.data
        price=form.price.data
        add=Customerregister(username=username,lastname=lastname,phone=phone,add=add,image1=image1,nic=nic,hour=hour,day=day,month=month,year=year,price=price)
        db.session.add(add)
        db.session.commit()
        flash(f'Product Created Successfully','success')
        return redirect(url_for('index'))
    return render_template('customer.html',form=form)



@app.route('/customers',methods=['GET','POST'])
@login_required
def customers():
    customers=Customerregister.query.all()
    return render_template('customers.html',customers=customers)

@app.route('/updatecustomer/<int:id>',methods=['GET','POST'])
@roles_accepted('admin')
@login_required
def updatecustomer(id):
    customer=Customerregister.query.get_or_404(id)
    form=CustomerregisterForm()
    if form.validate_on_submit():
        customer.username=form.username.data
        customer.lastname=form.lastname.data
        customer.phone=form.phone.data
        customer.add=form.add.data
        if request.files.get('image1'):
            try:
                os.unlink(os.path.join(current_app.root_path,'static/img/'+customer.image1))
                customer.image1=photos.save(request.files.get('image1'),name=secrets.token_hex(10)+'.')
        
            except:
                customer.image1=photos.save(request.files.get('image1'),name=secrets.token_hex(10)+'.')
        customer.nic=form.nic.data
        customer.hour=form.hour.data
        customer.day=form.day.data
        customer.month=form.month.data
        customer.year=form.year.data
        customer.price=form.price.data
        flash(f'Book Successfully Updated','success')
        db.session.commit()
        return redirect(url_for('customers',customer_id=customer.id))
    elif request.method=='GET':
        form.username.data=customer.username
        form.lastname.data=customer.lastname
        form.phone.data=customer.phone
        form.add.data=customer.add
        form.nic.data=customer.nic
        form.hour.data=customer.hour
        form.day.data=customer.day
        form.month.data=customer.month
        form.year.data=customer.year
        form.price.data=customer.price
    return render_template('updatecustomer.html',form=form )
@roles_accepted('admin')
@app.route('/deletecustomer/<int:id>',methods=['GET','POST'])
@login_required
def deletecustomer(id):
    customer=Customerregister.query.get_or_404(id)
    os.remove(os.path.join(current_app.root_path,'static/img/'+customer.image1))
    db.session.delete(customer)
    db.session.commit()
    flash('Product Successfully Deleted','success')
    return redirect(url_for('customers'))



@app.route('/rent',methods=['GET','POST'])
@roles_accepted('admin')
@login_required
def rent():
    form=RentbookcustomerForm()
    if form.validate_on_submit():
        nic=form.nic.data
        hour=form.hour.data
        day=form.day.data
        month=form.month.data
        year=form.year.data
        bookname=form.bookname.data
        bookpage=form.bookpage.data
        add=Rentbookcustomer(nic=nic,hour=hour,day=day,month=month,year=year,bookname=bookname,bookpage=bookpage)
        db.session.add(add)
        db.session.commit()
        flash(f'Product Created Successfully','success')
        return redirect(url_for('index'))
    return render_template('rent.html',form=form)


@app.route('/rents',methods=['GET','POST'])
@login_required
def rents():
    rents=Rentbookcustomer.query.all()
    return render_template('rents.html',rents=rents)

@app.route('/updaterent/<int:id>',methods=['GET','POST'])
@roles_accepted('admin')
@login_required
def updaterent(id):
    rent=Rentbookcustomer.query.get_or_404(id)
    form=RentbookcustomerForm()
    if form.validate_on_submit():
        rent.nic=form.nic.data
        rent.hour=form.hour.data
        rent.day=form.day.data
        rent.month=form.month.data
        rent.year=form.year.data
        rent.bookname=form.bookname.data
        rent.bookpage=form.bookpage.data
        flash(f'Book Successfully Updated','success')
        db.session.commit()
        return redirect(url_for('rents',rent_id=rent.id))
    elif request.method=='GET':
        form.nic.data=rent.nic
        form.hour.data=rent.hour
        form.day.data=rent.day
        form.month.data=rent.month
        form.year.data=rent.year
        form.bookname.data=rent.bookname
        form.bookpage.data=rent.bookpage
    return render_template('updaterent.html',form=form )


@app.route('/deleterent/<int:id>',methods=['GET','POST'])
@roles_accepted('admin')
@login_required
def deleterent(id):
    customer=Rentbookcustomer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    flash('Product Successfully Deleted','success')
    return redirect(url_for('rents'))


@app.route('/single_page/<int:id>')
def single_page(id):
    book=Book.query.get_or_404(id)
    return render_template('single_page.html',book=book)



@app.route('/register',methods=['GET','POST'])

def register():

    form=RegistrationForm()
    if form.validate_on_submit():
        user=User(username=form.username.data,email=form.email.data,password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account Created Successfully','success')
        return redirect(url_for('index'))
    return render_template('register.html',title='Register',form=form)

@app.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data,password=form.password.data).first()
        if user:
            login_user(user)
            flash(f'Welcome You Successfully loged in','success')
            return redirect(url_for('index'))
        else:
            flash(f'Login Unsuccessfull Try again','danger')
    return render_template('login.html',form=form,title='Login')

def save_photo(picture):
    random=secrets.token_hex(8)
    _,ext=os.path.splitext(picture.filename)
    name=random+ext
    Path=os.path.join(app.root_path,'static/img',name)
    output=(400,400)
    i=Image.open(picture)
    i.thumbnail(output)
    i.save(Path)
    return name

@app.route('/account',methods=['GET','POST'])

@login_required
def account():
    form=UpdateAccountForm()
    if form.validate_on_submit():
        if form.image.data:
            photo=save_photo(form.image.data)
            current_user.image=photo
        current_user.username=form.username.data
        current_user.email=form.email.data
        db.session.commit()
        flash('Successfully Updated','success')
        return redirect(url_for('index'))
    elif request.method=='GET':
        form.username.data=current_user.username
        form.email.data=current_user.email
    image=url_for('static',filename='img/'+current_user.image)
    return render_template('account.html',title='Account',image=image,form=form)




@app.route('/profile')
def profile():
    return render_template('profile.html',title=' Profile')    
        

@app.route('/about')
def about():
    
    return render_template('about.html',title='About')
    
@login_required
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
    







