from faktura import app
from flask import request, render_template, send_file, redirect, make_response
from faktura.models import db, Customer, Invoice
from faktura.breadcrumbs import breadcrumbs


@app.route('/customer/<int:customer_id>')
def show_customer(customer_id):
    customer = Customer.query.filter_by(id=customer_id).first()
    return render_template('customers/show.html', customer=customer, breadcrumbs=breadcrumbs("Main Menu","Customers"))


@app.route('/customers')
def customers():
    customers = Customer.query.all()
    return render_template('customers/list.html', customers=customers, breadcrumbs=breadcrumbs("Main Menu"))

@app.route('/customer/create', methods=["POST", "GET"])
def create_customer():
    if request.method == "GET":
        return render_template('customers/create.html', breadcrumbs=breadcrumbs("Main Menu","Customers"))

    form = request.form
    customer = Customer()
    customer.name = form["customerName"]
    customer.street = form["customerStreet"]
    customer.zip = form["customerZip"]
    customer.city = form["customerCity"]
    db.session.add(customer)
    db.session.commit()
    return redirect('/customer/{}'.format(customer.id))
