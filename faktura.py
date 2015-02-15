from flask import Flask, request, render_template, send_file, redirect, make_response
import pdfkit
from datetime import datetime
from uuid import uuid4
from decimal import Decimal
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile("faktura.cfg")
db = SQLAlchemy(app)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    street = db.Column(db.String(250))
    city = db.Column(db.String(100))
    zip = db.Column(db.String(10))

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True) #would like a guid here..
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    customer = db.relationship('Customer', backref=db.backref('invoices', lazy='dynamic'))
    reference_id = db.Column(db.Integer)
    created = db.Column(db.DateTime)
    due = db.Column(db.DateTime)
    total_tax = db.Column(db.Float)
    total_value = db.Column(db.Integer)
    rows = db.relationship('InvoiceRow', backref='invoice', lazy='dynamic')

    def __init__(self):
        self.due = datetime.now()
        self.reference_id = 1337
        self.created = datetime.now()
        self.customer = Customer()
        self.rows = []
        self.total_tax = 0
        self.total_value = 0

class InvoiceRow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(250))
    tax = db.Column(db.Float)
    value = db.Column(db.Integer)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'))

    def __init__(self, description, vat, cost):
        self.description = description
        self.tax = vat
        self.value = cost

@app.route('/')
def hello():
    return "hello"

@app.route('/list')
def list():
    invoices = Invoice.query.all()
    print(invoices)
    return render_template('list.html', invoices=invoices)

@app.route('/show/<int:invoice_id>')
def show(invoice_id):
    invoice = Invoice.query.filter_by(id=invoice_id).first()
    print(invoice)
    return render_template('show.html', invoice=invoice)

@app.route('/show/<int:invoice_id>/pdf')
def pdf(invoice_id): # acl..
    return send_file('pdfs/{}.pdf'.format(invoice_id))

@app.route('/create', methods=['POST','GET'])
def create():
    if request.method == 'POST':
        invoice = invoice_from_form(request.form)
        db.session.add(invoice.customer)
        db.session.add(invoice)
        # db.session.add(invoice.rows)
        db.session.commit()
        pdf = pdf_from_invoice(invoice)
        with open('pdfs/{}.pdf'.format(invoice.id), 'wb') as f:
            f.write(pdf)
        return redirect('/show/{}'.format(invoice.id))
    else:
        return render_template('create.html')

def invoice_from_form(form):
    invoice = Invoice()
    invoice.customer.name = form["customerName"]
    invoice.customer.street = form["customerStreet"]
    invoice.customer.city = form["customerCity"]
    invoice.customer.zip = form["customerZip"]

    for i in range(len(form.getlist("description"))):
        desc, tax, value = form.getlist("description")[i], form.getlist("tax")[i], form.getlist("value")[i]
        tax = Decimal("0." + tax.replace("%",""))
        invoice.rows.append(InvoiceRow(desc, tax, value))
        invoice.total_value += int(value)
        invoice.total_tax += int(value) * tax
    return invoice

def pdf_from_invoice(invoice):
    html = render_template('render.html', invoice=invoice)
    pdf = pdfkit.from_string(html, False)
    return pdf


@app.route('/render', methods=['POST'])
def render():
    invoice = invoice_from_form(request.form)
    pdf = pdf_from_invoice(invoice)

    response = make_response(pdf)
    response.headers['Content-Type'] = "application/pdf"
    return response


if __name__ == '__main__':
    app.debug = True
    db.create_all()
    app.run()
