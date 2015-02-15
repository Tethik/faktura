from flask import Flask, request, render_template, send_file, redirect, make_response
import pdfkit
from datetime import datetime
from uuid import uuid4
from decimal import Decimal

app = Flask(__name__)
# app.config.from_pyfile("faktura.cfg")

class Customer:
    pass

class Invoice:
    def __init__(self):
        self.due = datetime.now()
        self.id = uuid4()
        self.reference_id = 1337
        self.created = datetime.now()
        self.customer = Customer()
        self.rows = []
        self.total_tax = 0
        self.total_cost = 0

class InvoiceRow:
    def __init__(self, description, vat, cost):
        self.description = description
        self.vat = vat
        self.cost = cost

@app.route('/')
def hello():
    return "hello"

@app.route('/list')
def list():
    pass

@app.route('/show/<invoice_id>')
def show(invoice_id):
    return render_template('show.html')

@app.route('/create')
def create():
    if request.method == 'POST':
        return redirect('/show/1337')
    else:
        return render_template('create.html')

def invoice_from_form(form):
    invoice = Invoice()
    invoice.customer.name = form["customerName"]
    invoice.customer.street = form["customerStreet"]
    invoice.customer.city = form["customerCity"]
    invoice.customer.zip = form["customerZip"]

    for i in range(len(form.getlist("description"))):
        desc, tax, value = form.getlist("description")[i], form.getlist("vat")[i], form.getlist("cost")[i]
        invoice.rows.append(InvoiceRow(desc, tax, value))
        invoice.total_cost += int(value)
        invoice.total_tax += int(value) * Decimal("0." + tax.replace("%",""))
    return invoice


@app.route('/render', methods=['POST'])
def render():
    invoice = invoice_from_form(request.form)

    html = render_template('render.html', invoice=invoice)
    pdf = pdfkit.from_string(html, False)
    response = make_response(pdf)
    response.headers['Content-Type'] = "application/pdf"
    return response


if __name__ == '__main__':
    app.debug = True
    app.run()
