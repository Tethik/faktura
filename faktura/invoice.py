from faktura import app
from flask import request, render_template, send_file, redirect, make_response
from faktura.models import db, Customer, Invoice, InvoiceRow, TemplateVariable
from decimal import Decimal
from faktura.breadcrumbs import breadcrumbs
from datetime import datetime
import pdfkit
import os



@app.route('/invoices')
def list():
    query = request.args.get('query', '').strip()
    page = int(request.args.get('p', 0))

    q = Invoice.query.filter(Customer.name.like('{}%'.format(query))).limit(10).offset(10*page)
    count = q.count()
    invoices = q.all()

    return render_template('invoices/list.html', invoices=invoices, breadcrumbs=breadcrumbs("Main Menu"), count=count, page=page, query=query)

@app.route('/invoice/<int:invoice_id>')
def show(invoice_id):
    invoice = Invoice.query.filter_by(id=invoice_id).first()
    return render_template('invoices/show.html', invoice=invoice, breadcrumbs=breadcrumbs("Main Menu","Invoices"))

@app.route('/invoice/<int:invoice_id>/delete', methods=["GET","POST"])
def delete_invoice(invoice_id):
    invoice = Invoice.query.filter_by(id=invoice_id).first()
    if request.method == "POST":
        db.session.delete(invoice)
        db.session.commit()
        return redirect('/invoices')
    return render_template('invoices/delete.html', invoice=invoice, breadcrumbs=breadcrumbs("Main Menu","Invoices"))

@app.route('/invoice/<int:invoice_id>/pdf')
def pdf(invoice_id): # acl..
    pdfdir = app.config["PDF_DIRECTORY"]
    return send_file('{}/{}.pdf'.format(pdfdir, invoice_id))

@app.route('/invoice/create/for_customer/<int:customer_id>', methods=['POST','GET'])
def create_for_customer(customer_id):
    customer = Customer.query.filter(Customer.id == customer_id).first()
    if request.method == "GET":
        return render_template('invoices/create_invoice_details.html', customer=customer, breadcrumbs=breadcrumbs("Main Menu","Invoices"))
    # POST
    invoice = invoice_from_form(request.form)
    invoice.customer = customer
    db.session.add(invoice)
    pdf = pdf_from_invoice(invoice)
    pdfdir = app.config["PDF_DIRECTORY"]
    if not os.path.isabs(pdfdir):
        pdfdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), pdfdir)

    with open('{}/{}.pdf'.format(pdfdir, invoice.id), 'wb') as f:
        f.write(pdf)
    db.session.commit()
    return redirect('/invoice/{}'.format(invoice.id))


@app.route('/invoice/create', methods=['POST','GET'])
def create():
    if request.method == 'GET':
        customers = db.session.query(Customer.id, Customer.name).all() # bottleneck
        return render_template('invoices/create.html', customers=customers, breadcrumbs=breadcrumbs("Main Menu","Invoices"))

    customer_id = int(request.form["customer_id"])
    if customer_id < 0: # new customerorm
        customer = Customer()
        customer.name = request.form["customerName"]
        customer.street = request.form["customerStreet"]
        customer.city = request.form["customerCity"]
        customer.zip = request.form["customerZip"]
        db.session.add(customer)
        db.session.commit()
        customer_id = customer.id

    return redirect("/invoice/create/for_customer/{}".format(customer_id))




def invoice_from_form(form):
    invoice = Invoice()
    invoice.due = datetime.strptime(form["duedate"], "%Y-%m-%d")
    # invoice.customer.name = form["customerName"]
    # invoice.customer.street = form["customerStreet"]
    # invoice.customer.city = form["customerCity"]
    # invoice.customer.zip = form["customerZip"]

    for i in range(len(form.getlist("description"))):
        desc, tax, value = form.getlist("description")[i], form.getlist("tax")[i], form.getlist("value")[i]
        tax = Decimal("0." + tax.replace("%",""))
        invoice.rows.append(InvoiceRow(desc, tax, value))
        invoice.total_value += int(value)
        invoice.total_tax += int(value) * tax
    return invoice

def template_vars():
    return dict((item.key, item.value) for item in TemplateVariable.query.all())

def pdf_from_invoice(invoice):
    html = render_template('invoices/render.html', invoice=invoice, **template_vars())
    pdf = pdfkit.from_string(html, False)
    return pdf

@app.route('/invoice/render/<int:customer_id>', methods=['POST'])
def render(customer_id):
    invoice = invoice_from_form(request.form)
    invoice.customer = Customer.query.filter(Customer.id ==  customer_id).first()
    pdf = pdf_from_invoice(invoice)
    response = make_response(pdf)
    response.headers['Content-Type'] = "application/pdf"
    return response
