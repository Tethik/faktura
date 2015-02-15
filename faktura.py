from flask import Flask, request, render_template, send_file
import pdfkit

app = Flask(__name__)
# app.config.from_pyfile("faktura.cfg")
app.config.Debug = True

@app.route('/')
def hello():
    return "hello"

@app.route('/list')
def list():
    pass

@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/render', methods=['GET', 'POST'])
def render():
    pdfkit.from_string(render_template('render.html'), 'out.pdf')
    return send_file('out.pdf')


if __name__ == '__main__':
    app.debug = True
    app.run()
