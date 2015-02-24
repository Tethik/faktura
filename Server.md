#Server Setup
This is a mini how-to for setting up the application on a typical debian vps.

##virtualenv
The recommended way of doing things is using a virtualenv. Extract/Clone
the project directory where you want to then create a virtualenv in the same
place. I found that debian-stable does not support python3.3 needed for
Flask, but the application thankfully runs just as well under python2.7.

```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```


##wkhtlmtopdf and a virtual x-server

Wkhtlmtopdf needs an x-server to run. For this we use xvfb.
```
apt-get install xvfb
```

Copy the following file to `/etc/init.d/xvfb`
```
XVFB=/usr/bin/Xvfb
XVFBARGS=":0 -screen 0 1024x768x24 -ac +extension GLX +render -noreset"
PIDFILE=/var/run/xvfb.pid
case "$1" in
  start)
    echo -n "Starting virtual X frame buffer: Xvfb"
    start-stop-daemon --chuid www-data --start --quiet --pidfile $PIDFILE --make-pidfile --background --exec $XVFB -- $XVFBARGS
    echo "."
    ;;
  stop)
    echo -n "Stopping virtual X frame buffer: Xvfb"
    start-stop-daemon --chuid www-data --stop --quiet --pidfile $PIDFILE
    echo "."
    ;;
  restart)
    $0 stop
    $0 start
    ;;
  *)
        echo "Usage: /etc/init.d/xvfb {start|stop|restart}"
        exit 1
esac

exit 0
```

Start the service using `service xvfb start`. This service will run a virtual x
screen on the www-data user typically used by apache for wkhtmltopdf to use.


##Apache setup

First, create a .wsgi file in the same directory as the `runserver.py` file.
You can use the following script as a basis. Change `path` to where you extracted the project. If you're not using a virtualenv, comment out or
remove the two lines under `#activate virtualenv`.

```python
import sys
import os

path = '/usr/local/lib/faktura.blacknode.se'
sys.path.insert(0, path)

# activate virtualenv
activate_this = os.path.expanduser(path+"/venv/bin/activate_this.py")
execfile(activate_this, dict(__file__=activate_this))

os.environ["DISPLAY"] = ":0"

from faktura import app as application
from faktura.models import db
application.config.from_pyfile(path+"/faktura.cfg")
db.create_all()
```

Set up your apache with the WSGIScriptAlias directive
```
WSGIScriptAlias / /<path to application directory>/faktura.wsgi
```

As an example, which might be helpful if you haven't configured a python web app before, my own virtualhost looks like this:
```
<IfModule mod_ssl.c>
<VirtualHost *:443>
        ServerAdmin webmaster@blacknode.se
        ServerName faktura.blacknode.se
        ServerAlias faktura.blacknode.se

        WSGIScriptAlias / /usr/local/lib/faktura.blacknode.se/faktura.wsgi

        <Directory /usr/local/lib/faktura.blacknode.se>
                Order deny,allow
                Allow from all
        </Directory>

        ErrorLog ${APACHE_LOG_DIR}/faktura.error.log

        # Possible values include: debug, info, notice, warn, error, crit,
        # alert, emerg.
        LogLevel warn

        CustomLog ${APACHE_LOG_DIR}/faktura.access.log combined

        # SSLstuff
        SSLEngine on
        SSLProtocol all -SSLv2 -SSLv3
        SSLHonorCipherOrder on
        SSLCipherSuite "EECDH+ECDSA+AESGCM EECDH+aRSA+AESGCM EECDH+ECDSA+SHA384 EECDH+ECDSA+SHA256 EECDH+aRSA+SHA384 EECDH+aRSA+SHA256 EECDH EDH+aRSA RSA+3DES !RC4 !aNULL !eNULL !LOW !MD5 !EXP !PSK !SRP !DSS"

        SSLCertificateFile /etc/ssl/certs/faktura.signed.crt
        SSLCertificateKeyFile /etc/ssl/private/faktura.pem
        SSLCertificateChainFile /etc/ssl/certs/blacknode.dev.signed.crt

        Header set Strict-Transport-Security max-age=15552000
</VirtualHost>
</IfModule>
```

###Sources:
For the init.d script: https://coderwall.com/p/tog9eq/using-wkhtmltopdf-and-an-xvfb-daemon-to-render-html-to-pdf
