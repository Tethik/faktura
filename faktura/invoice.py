from faktura import app
from flask import request, render_template, send_file, redirect, make_response
from faktura.models import db, Customer, Invoice, InvoiceRow
from decimal import Decimal
from faktura.breadcrumbs import breadcrumbs
import pdfkit
import os



@app.route('/invoices')
def list():
    invoices = Invoice.query.all()
    print(invoices)
    return render_template('invoices/list.html', invoices=invoices, breadcrumbs=breadcrumbs("Main Menu"))

@app.route('/invoice/<int:invoice_id>')
def show(invoice_id):
    invoice = Invoice.query.filter_by(id=invoice_id).first()
    print(invoice)
    return render_template('invoices/show.html', invoice=invoice, breadcrumbs=breadcrumbs("Main Menu","Invoices"))

@app.route('/invoice/<int:invoice_id>/pdf')
def pdf(invoice_id): # acl..
    pdfdir = app.config["PDF_DIRECTORY"]
    return send_file('{}/{}.pdf'.format(pdfdir, invoice_id))

@app.route('/invoice/create', methods=['POST','GET'])
def create():
    if request.method == 'POST':
        invoice = invoice_from_form(request.form)
        db.session.add(invoice.customer)
        db.session.add(invoice)
        pdf = pdf_from_invoice(invoice)
        pdfdir = app.config["PDF_DIRECTORY"]
        if not os.path.isabs(pdfdir):
            pdfdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), pdfdir)

        with open('{}/{}.pdf'.format(pdfdir, invoice.id), 'wb') as f:
            f.write(pdf)
        db.session.commit()
        return redirect('/show/{}'.format(invoice.id))
    else:
        return render_template('invoices/create.html', breadcrumbs=breadcrumbs("Main Menu","Invoices"))

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
    html = render_template('invoices/render.html', invoice=invoice)
    pdf = pdfkit.from_string(html, False)
    return pdf

@app.route('/invoice/render', methods=['POST'])
def render():
    invoice = invoice_from_form(request.form)
    pdf = pdf_from_invoice(invoice)
    response = make_response(pdf)
    response.headers['Content-Type'] = "application/pdf"
    return response
