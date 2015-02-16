from faktura import app
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

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