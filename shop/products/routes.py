from flask import render_template,session, request,redirect,url_for,flash,current_app
from shop import app,db,photos, search
from .models import Category,Addproduct, Banner
from .forms import Addproducts, Addbanner, Addcat
import secrets
import os


def categories():
    categories = Category.query.join(Addproduct,(Category.id == Addproduct.category_id)).all()
    return categories


@app.route('/')
def home():
    page = request.args.get('page',1, type=int)
    products = Addproduct.query.filter(Addproduct.stock > 0).order_by(Addproduct.price.desc()).paginate(page=page, per_page=30)
    banners = Banner.query.all()
    return render_template('products/index.html', products=products,categories=categories(), banners=banners)


@app.route('/result')
def result():
    searchword = request.args.get('q')
    products = Addproduct.query.msearch(searchword, fields=['name','desc'] , limit=30)
    return render_template('products/result.html',products=products, categories=categories())


@app.route('/product/<int:id>')
def single_page(id):
    product = Addproduct.query.get_or_404(id)
    return render_template('products/single_page.html',product=product,categories=categories())


@app.route('/categories/<int:id>')
def get_category(id):
    page = request.args.get('page',1, type=int)
    get_cat = Category.query.filter_by(id=id).first_or_404()
    get_cat_prod = Addproduct.query.filter_by(category=get_cat).paginate(page=page, per_page=30)
    return render_template('products/index.html',get_cat_prod=get_cat_prod,categories=categories(),get_cat=get_cat)


@app.route('/addcat', methods=['GET', 'POST'])
def addcat():
    if 'email' not in session:
        flash('Login first please','danger')
        return redirect(url_for('login'))
    form = Addcat(request.form)
    if request.method =='POST':
        name = form.name.data
        image_category = photos.save(request.files.get('image_category'))
        addcat = Category(name=name, image_category=image_category)
        db.session.add(addcat)
        db.session.commit()
        return redirect(url_for('addcat'))
    return render_template('products/addbrand.html', form=form, title='Add Category')


@app.route('/updatecat/<int:id>', methods=['GET','POST'])
def updatecat(id):
    if 'email' not in session:
        flash('Login first please','danger')
        return redirect(url_for('login'))
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
        return redirect(url_for('admin'))
    form.name.data = category.name
    return render_template('products/addbrand.html', form=form, title='Update Category')



@app.route('/deletecat/<int:id>', methods=['POST'])
def deletecat(id):
    if 'email' not in session:
        flash('Login first please','danger')
        return redirect(url_for('login'))
    category = Category.query.get_or_404(id)
    if request.method =="POST":
        try:
            os.unlink(os.path.join(current_app.root_path, "static/product_images/" + category.image_category))
        except Exception as e:
            print(e)
        db.session.delete(category)
        db.session.commit()
        flash(f'The product {category.name} was delete from your record','success')
        return redirect(url_for('admin'))
    flash(f'Can not delete the product','success')
    return redirect(url_for('admin'))
    

@app.route('/addbanner', methods=['GET', 'POST'])
def addbanner():
    if 'email' not in session:
        flash('Login first please','danger')
        return redirect(url_for('login'))
    form = Addbanner(request.form)
    if request.method =='POST':
        name = form.name.data
        image_banner = photos.save(request.files.get('image_banner'))
        addbanner = Banner(name=name, image_banner=image_banner)
        db.session.add(addbanner)
        db.session.commit()
        return redirect(url_for('addbanner'))
    return render_template('products/addbanner.html', form=form, title='Add Banner')


@app.route('/updatebanner/<int:id>', methods=['GET','POST'])
def updatebanner(id):
    if 'email' not in session:
        flash('Login first please','danger')
        return redirect(url_for('login'))
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
        return redirect(url_for('admin'))
    form.name.data = banner.name
    return render_template('products/addbanner.html', form=form, title='Update Banner')


@app.route('/deletebanner/<int:id>', methods=['POST'])
def deletebanner(id):
    if 'email' not in session:
        flash('Login first please','danger')
        return redirect(url_for('login'))
    banner = Banner.query.get_or_404(id)
    if request.method =="POST":
        try:
            os.unlink(os.path.join(current_app.root_path, "static/product_images/" + banner.image_banner))
        except Exception as e:
            print(e)
        db.session.delete(banner)
        db.session.commit()
        flash(f'The product {banner.name} was delete from your record','success')
        return redirect(url_for('admin'))
    flash(f'Can not delete the product','success')
    return redirect(url_for('admin'))


@app.route('/addproduct', methods=['GET','POST'])
def addproduct():
    if 'email' not in session:
        flash('Login first please','danger')
        return redirect(url_for('login'))
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
        return redirect(url_for('admin'))
    return render_template('products/addproduct.html', form=form, title='Add a Product', categories=categories)




@app.route('/updateproduct/<int:id>', methods=['GET','POST'])
def updateproduct(id):
    if 'email' not in session:
        flash('Login first please','danger')
        return redirect(url_for('login'))
    form = Addproducts(request.form)
    product = Addproduct.query.get_or_404(id)
    categories = Category.query.all()
    category = request.form.get('category')
    if request.method =="POST":
        product.name = form.name.data
        product.price = form.price.data
        product.discount = form.discount.data
        product.stock = form.stock.data
        product.desc = form.discription.data
        product.category_id = category
        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/product_images/" + product.image_1))
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
            except:
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
        flash('The product was updated','success')
        db.session.commit()
        return redirect(url_for('admin'))
    form.name.data = product.name
    form.price.data = product.price
    form.discount.data = product.discount
    form.stock.data = product.stock
    form.discription.data = product.desc
    category = product.category.name
    return render_template('products/addproduct.html', form=form, title='Update Product',getproduct=product, categories=categories)


@app.route('/deleteproduct/<int:id>', methods=['POST'])
def deleteproduct(id):
    if 'email' not in session:
        flash('Login first please','danger')
        return redirect(url_for('login'))
    product = Addproduct.query.get_or_404(id)
    if request.method =="POST":
        try:
            os.unlink(os.path.join(current_app.root_path, "static/product_images/" + product.image_1))
        except Exception as e:
            print(e)
        db.session.delete(product)
        db.session.commit()
        flash(f'The product {product.name} was delete from your record','success')
        return redirect(url_for('admin'))
    flash(f'Can not delete the product','success')
    return redirect(url_for('admin'))
