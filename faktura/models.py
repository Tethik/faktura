from faktura import app
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask.ext.login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
import uuid

db = SQLAlchemy(app)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    street = db.Column(db.String(250))
    city = db.Column(db.String(100))
    zip = db.Column(db.String(10))
    reference = db.Column(db.String(250))
    organisation_number = db.Column(db.String(100))
    vat_number = db.Column(db.String(100))

    def to_json(self):
        return dict(name=self.name,
            street=self.street,
            id=self.id,
            city=self.city,
            zip=self.zip,
            reference=self.reference,
            organisation_number=self.organisation_number,
            vat_number=self.vat_number
        )

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True) #would like a guid here..
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    customer = db.relationship('Customer',
        backref=db.backref('invoices', lazy='dynamic', cascade='all, delete-orphan'))
    reference_id = db.Column(db.Integer)
    created = db.Column(db.DateTime)
    due = db.Column(db.DateTime)
    total_tax = db.Column(db.Float)
    total_value = db.Column(db.Integer)
    rows = db.relationship('InvoiceRow',
        backref='invoice', lazy='dynamic', cascade='all, delete-orphan')
    total_after_tax = db.Column(db.Float)
    link_token = db.Column(db.String(255))

    def __init__(self):
        self.due = datetime.now()
        self.reference_id = 1337
        self.created = datetime.now()
        self.rows = []
        self.total_tax = 0
        self.total_value = 0
        self.total_after_tax = 0
        self.link_token = str(uuid.uuid4())

class InvoiceRow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(250))
    tax = db.Column(db.Float)
    value = db.Column(db.Integer)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'))

    def __init__(self, description, vat, cost):
        self.description = description
        self.tax = vat
        self.value = int(cost)
        self.value_with_tax = self.value + vat*self.value

class TemplateVariable(db.Model):
    key = db.Column(db.String(100),  primary_key=True)
    value = db.Column(db.String(250))

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def to_json(self):
        return dict(key=self.key, value=self.value)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    email = db.Column(db.String(255))
