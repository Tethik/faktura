#Todo
* (Bug) Fix CSRF protection on the preview functionality. Currently it breaks if you preview an invoice, since no new token is generated.
* Validation of input
* No CDN for best offline compatibility.
  - The Google Font is the only issue at the moment
* Mailing
  - New field to customer (or perhaps a Contact object?)
  - Functionality to send forgot-password email to user
  - Functionality to send invoice email to customer.
  - As a part of initial setup.
* Templating Editor
  - Dynamic/static variables, how?
  - Preview functionality
  - Perhaps mock data for previews
