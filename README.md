# faktura
Simple invoicing webapplication using HTML templates.

# Installation
I recommend using a virtualenv. [See this guide for a great explanation.](http://docs.python-guide.org/en/latest/dev/virtualenvs/)

Requirements are collected in the requirements.txt file.
` pip install -r requirements.txt `

You'll also need `wkhtmltopdf`, which is used by pdfkit.
`apt-get install wkhtmltopdf` or your equivalent packagemanager.

Configuration can be done in the faktura.cfg file, where you can change the sql uri used by sqlalchemy. By default it will use a sqllite database, so you don't have to do anything. Generated pdfs are saved in the `pdfs/`folder for now.

# Demo Usage
To start the http-server as a standalone flask application:
`python runserver.py`

After you've got the application running, simply navigate to http://127.0.0.1:5000



# Todo
See [TODO.md](TODO.md). Ideas at [IDEAS.md](IDEAS.md)

# Credits
Thanks to the following libs for doing basically all my work for me:
* [Flask](http://flask.pocoo.org/)
* [flask-sqlalchemy](http://flask-sqlalchemy.pocoo.org/)
* [pdfkit](https://pypi.python.org/pypi/pdfkit)
* [skeleton css framework](http://getskeleton.com)
* [flat circle-icons from elegantthemes.com] (http://www.elegantthemes.com/blog/freebie-of-the-week/beautiful-flat-icons-for-free)
