from flask import render_template,session, request,redirect,url_for,flash, current_app
from shop import db,bcrypt, photos
from .forms import RegistrationForm,LoginForm, Addcat, Addbanner, Addproducts
from .models import User
from shop.products.models import Addproduct,Category, Banner
from shop.customers.model import Customer
from shop.admin import bp
import os, secrets


@bp.route('/admin/')
def admin():
    if 'email' not in session:
        flash(f'Please firstly login','danger')
        return redirect(url_for('AD.login'))
    products = Addproduct.query.all()
    return render_template('admin/index.html', title='Admin page',products=products)


@bp.route('/admin/categories')
def categories():
    if 'email' not in session:
        flash(f'Please firstly login','danger')
        return redirect(url_for('AD.login'))
    categories = Category.query.order_by(Category.id.desc()).all()
    return render_template('admin/brand.html', title='categories',categories=categories)


@bp.route('/admin/banners')
def banners():
    if 'email' not in session:
        flash(f'Please firstly login','danger')
        return redirect(url_for('AD.login'))
    banners = Banner.query.order_by(Banner.id.desc()).all()
    return render_template('admin/banner.html', title='banners',banners=banners)


@bp.route('/admin/customers')
def customers():
    if 'email' not in session:
        flash(f'Please firstly login','danger')
        return redirect(url_for('AD.login'))
    customers = Customer.query.order_by(Customer.id.desc()).all()
    return render_template('admin/customers.html', customers=customers, title='Customers')


@bp.route('/admin/register', methods=['GET', 'POST'])
def register():
    # if 'email' not in session:
    #     flash(f'Please firstly login','danger')
    #     return redirect(url_for('login'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = User(name=form.name.data,email=form.email.data,
                    password=hash_password)
        db.session.add(user)
        flash(f'welcome {form.name.data} Thanks for registering','success')
        db.session.commit()
        return redirect(url_for('AD.login'))
    return render_template('admin/register.html',title='Register user', form=form)


@bp.route('/admin/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['email'] = form.email.data
            flash(f'welcome {form.email.data} you are logedin now','success')
            return redirect(url_for('AD.admin'))
        else:
            flash(f'Wrong email and password', 'success')
            return redirect(url_for('AD.login'))
    return render_template('admin/login.html',title='Login page',form=form)


@bp.route('/admin/logout')
def admin_logout():
    session.clear()
    return redirect(url_for('products.home'))


@bp.route('/deletecustomer/<int:id>', methods=['POST'])
def deletecustomer(id):
    if 'email' not in session:
        flash("Login first please", "danger")
        return redirect(url_for("AD.login"))
    customer = Customer.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(customer)
        db.session.commit()
        return redirect(url_for('AD.admin'))
    flash(f'Can not delete the customer','warning')
    return redirect(url_for('AD.admin'))


@bp.route('/admin/addcat', methods=['GET', 'POST'])
def addcat():
    if 'email' not in session:
        flash('Login first please','danger')
        return redirect(url_for('AD.login'))
    form = Addcat(request.form)
    if request.method =='POST':
        name = form.name.data
        image_category = photos.save(request.files.get('image_category'))
        addcat = Category(name=name, image_category=image_category)
        db.session.add(addcat)
        db.session.commit()
        return redirect(url_for('AD.addcat'))
    return render_template('products/addbrand.html', form=form, title='Add Category')


@bp.route('/admin/updatecat/<int:id>', methods=['GET','POST'])
def updatecat(id):
    if 'email' not in session:
        flash('Login first please','danger')
        return redirect(url_for('AD.login'))
    form = Addcat(request.form)
    category = Category.query.get_or_404(id)
    if request.method =="POST":
        category.name = form.name.data
        if request.files.get('image_category'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/product_images/" + category.image_category))
                category.image_category = photos.save(request.files.get('image_category'))
            except:
                category.image_category = photos.save(request.files.get('image_category'))
        flash('The product was updated','success')
        db.session.commit()
        return redirect(url_for('AD.admin'))
    form.name.data = category.name
    return render_template('products/addbrand.html', form=form, title='Update Category')


@bp.route('/admin/deletecat/<int:id>', methods=['POST'])
def deletecat(id):
    if 'email' not in session:
        flash('Login first please','danger')
        return redirect(url_for('AD.login'))
    category = Category.query.get_or_404(id)
    if request.method =="POST":
        try:
            os.unlink(os.path.join(current_app.root_path, "static/product_images/" + category.image_category))
        except Exception as e:
            print(e)
        db.session.delete(category)
        db.session.commit()
        flash(f'The product {category.name} was delete from your record','success')
        return redirect(url_for('AD.admin'))
    flash(f'Can not delete the product','success')
    return redirect(url_for('AD.admin'))


@bp.route('/addbanner', methods=['GET', 'POST'])
def addbanner():
    if 'email' not in session:
        flash('Login first please','danger')
        return redirect(url_for('AD.login'))
    form = Addbanner(request.form)
    if request.method =='POST':
        name = form.name.data
        image_banner = photos.save(request.files.get('image_banner'))
        addbanner = Banner(name=name, image_banner=image_banner)
        db.session.add(addbanner)
        db.session.commit()
        return redirect(url_for('AD.addbanner'))
    return render_template('products/addbanner.html', form=form, title='Add Banner')


@bp.route('/updatebanner/<int:id>', methods=['GET','POST'])
def updatebanner(id):
    if 'email' not in session:
        flash('Login first please','danger')
        return redirect(url_for('AD.login'))
    form = Addbanner(request.form)
    banner = Banner.query.get_or_404(id)
    if request.method =="POST":
        banner.name = form.name.data
        if request.files.get('image_banner'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/product_images/" + banner.image_banner))
                banner.image_banner = photos.save(request.files.get('image_banner'))
            except:
                banner.image_banner = photos.save(request.files.get('image_banner'))
        flash('The product was updated','success')
        db.session.commit()
        return redirect(url_for('AD.admin'))
    form.name.data = banner.name
    return render_template('products/addbanner.html', form=form, title='Update Banner')


@bp.route('/deletebanner/<int:id>', methods=['POST'])
def deletebanner(id):
    if 'email' not in session:
        flash('Login first please','danger')
        return redirect(url_for('AD.login'))
    banner = Banner.query.get_or_404(id)
    if request.method =="POST":
        try:
            os.unlink(os.path.join(current_app.root_path, "static/product_images/" + banner.image_banner))
        except Exception as e:
            print(e)
        db.session.delete(banner)
        db.session.commit()
        flash(f'The product {banner.name} was delete from your record','success')
        return redirect(url_for('AD.admin'))
    flash(f'Can not delete the product','success')
    return redirect(url_for('AD.admin'))


@bp.route('/addproduct', methods=['GET','POST'])
def addproduct():
    if 'email' not in session:
        flash('Login first please','danger')
        return redirect(url_for('AD.login'))
    form = Addproducts(request.form)
    categories = Category.query.all()
    if request.method=="POST"and 'image_1' in request.files:
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        desc = form.description.data
        category = request.form.get('category')
        image_1 = photos.save(request.files.get('image_1'))
        addproduct = Addproduct(name=name,price=price,discount=discount,stock=stock,desc=desc,category_id=category,image_1=image_1)
        db.session.add(addproduct)
        flash(f'The product {name} was added in database','success')
        db.session.commit()
        return redirect(url_for('AD.admin'))
    return render_template('products/addproduct.html', form=form, title='Add a Product', categories=categories)


@bp.route('/updateproduct/<int:id>', methods=['GET','POST'])
def updateproduct(id):
    if 'email' not in session:
        flash('Login first please','danger')
        return redirect(url_for('AD.login'))
    form = Addproducts(request.form)
    product = Addproduct.query.get_or_404(id)
    categories = Category.query.all()
    category = request.form.get('category')
    if request.method =="POST":
        product.name = form.name.data
        product.price = form.price.data
        product.discount = form.discount.data
        product.stock = form.stock.data
        product.desc = form.description.data
        product.category_id = category
        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/product_images/" + product.image_1))
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
            except:
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
        flash('The product was updated','success')
        db.session.commit()
        return redirect(url_for('AD.admin'))
    form.name.data = product.name
    form.price.data = product.price
    form.discount.data = product.discount
    form.stock.data = product.stock
    form.description.data = product.desc
    category = product.category.name
    return render_template('products/addproduct.html', form=form, title='Update Product',getproduct=product, categories=categories)


@bp.route('/deleteproduct/<int:id>', methods=['POST'])
def deleteproduct(id):
    if 'email' not in session:
        flash('Login first please','danger')
        return redirect(url_for('AD.login'))
    product = Addproduct.query.get_or_404(id)
    if request.method =="POST":
        try:
            os.unlink(os.path.join(current_app.root_path, "static/product_images/" + product.image_1))
        except Exception as e:
            print(e)
        db.session.delete(product)
        db.session.commit()
        flash(f'The product {product.name} was delete from your record','success')
        return redirect(url_for('AD.admin'))
    flash(f'Can not delete the product','success')
    return redirect(url_for('AD.admin'))
