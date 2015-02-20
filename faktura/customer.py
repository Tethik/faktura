from faktura import app
from flask import request, render_template, send_file, redirect, make_response, jsonify
from faktura.models import db, Customer, Invoice
from faktura.breadcrumbs import breadcrumbs

@app.route('/customer/<int:customer_id>/json')
def json_customer(customer_id):
    customer = Customer.query.filter_by(id=customer_id).first()
    return jsonify(customer=customer.to_json())

@app.route('/customer/<int:customer_id>', methods=["GET", "POST"])
def show_customer(customer_id):
    customer = Customer.query.filter_by(id=customer_id).first()
    invoices = Invoice.query.filter_by(customer_id=customer_id).order_by(Invoice.id.desc()).all()
    if request.method == "POST":
        form = request.form
        customer.name = form["customerName"]
        customer.street = form["customerStreet"]
        customer.zip = form["customerZip"]
        customer.city = form["customerCity"]
        customer.reference = form["customerReference"]
        db.session.commit()

    return render_template('customers/show.html', customer=customer,  invoices=invoices, breadcrumbs=breadcrumbs("Main Menu","Customers"))

@app.route('/customer/<int:customer_id>/delete', methods=["GET", "POST"])
def delete_customer(customer_id):
    customer = Customer.query.filter_by(id=customer_id).first()
    if request.method == "POST":
        db.session.delete(customer)
        db.session.commit()
        return redirect("/customers")
    return render_template('customers/delete.html', customer=customer,  breadcrumbs=breadcrumbs("Main Menu","Customers"))


@app.route('/customers')
def customers():
    query = request.args.get('query', '').strip()
    page = int(request.args.get('p', 0))

    q = Customer.query.filter(Customer.name.like('{}%'.format(query))).limit(10).offset(10*page)
    count = q.count()
    customers = q.all()

    return render_template('customers/list.html', customers=customers, breadcrumbs=breadcrumbs("Main Menu"), query=query, count=count, page=page)

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
    customer.reference = request.form["customerReference"]
    db.session.add(customer)
    db.session.commit()
    return redirect('/customer/{}'.format(customer.id))
