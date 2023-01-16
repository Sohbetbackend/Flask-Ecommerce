from flask import render_template,session, request,redirect,url_for,flash,current_app,make_response
from flask_login import login_required, current_user, logout_user, login_user
from flask_babel import _
from shop import app,db,photos, search,bcrypt,login_manager
from .forms import CustomerRegisterForm, CustomerLoginFrom
from .model import Register,CustomerOrder
from shop.products.models import Category, Addproduct
import secrets
import os
import json


def categories():
    categories = Category.query.join(Addproduct,(Category.id == Addproduct.category_id)).all()
    return categories


@app.route('/customer/register', methods=['GET','POST'])
def customer_register():
    form = CustomerRegisterForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        register = Register(name=form.name.data, password=hash_password, contact=form.contact.data, address=form.address.data)
        db.session.add(register)
        flash(_('Welcome! Thank you for registering'))
        db.session.commit()
        return redirect(url_for('customerLogin'))
    return render_template('customer/register.html', form=form)


@app.route('/customer/login', methods=['GET','POST'])
def customerLogin():
    form = CustomerLoginFrom()
    if form.validate_on_submit():
        user = Register.query.filter_by(contact=form.contact.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash(_('You are login now!'))
            next = request.args.get('next')
            return redirect(next or url_for('home'))
        flash(_('Incorrect email and password'))
        return redirect(url_for('customerLogin'))

    return render_template('customer/login.html', form=form)


@app.route('/customer/logout')
def customer_logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/customer/<name>', methods=['GET', 'POST'])
@login_required
def aboutCustomer(name):
    user = Register.query.filter_by(name=name).first_or_404()
    return render_template('customer/aboutcustomer.html', user=user, categories=categories())


def updateshoppingcart():
    for key, shopping in session['Shoppingcart'].items():
        session.modified = True
        del shopping['image']
    return updateshoppingcart


@app.route('/getorder')
@login_required
def get_order():
    if current_user.is_authenticated:
        customer_id = current_user.id
        updateshoppingcart
        try:
            order = CustomerOrder(customer_id=customer_id,orders=session['Shoppingcart'], customer=current_user)
            db.session.add(order)
            db.session.commit()
            session.pop('Shoppingcart')
            flash(_('Your order has been sent successfully'))
            return redirect(url_for('home'))
        except Exception as e:
            print(e)
            flash(_('Some thing went wrong while get order'))
            return redirect(url_for('getCart'))


@app.route('/admin/zakazlar', methods=['GET', 'POST'])
def zakazlar():
    if 'email' not in session:
        return redirect(url_for('login'))
    orders = CustomerOrder.query.order_by(CustomerOrder.id.desc()).all()
    return render_template('customer/zakazlar.html', orders=orders, categories=categories())


@app.route('/admin/deletezakaz/<int:id>', methods=['GET','POST'])
def deletezakaz(id):
    zakaz = CustomerOrder.query.get_or_404(id)
    if request.method=="POST":
        db.session.delete(zakaz)
        flash(_("The zakaz was sent from shop to address"))
        db.session.commit()
        return redirect(url_for('zakazlar'))
    flash(_("The zakaz can't be  deleted from your database"))
    return redirect(url_for('admin'))


@app.route('/language/<language>')
def set_language(language=None):
	session['language'] = language
	if language == 'en':
		language == 'en'
	else:
		language == 'tk'
	return redirect(request.referrer)
