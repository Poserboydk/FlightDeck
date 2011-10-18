.. _install:

Installation
============


Requirements
------------
FligtDeck depends on:
 * Python 2.6
 * MySQL
 * git

We also suggest:
 * virtualenv
 * `virtualenvwrapper <http://www.doughellmann.com/docs/virtualenvwrapper/>`_


Installing
----------

It's outside the scope of this document, but we suggest you do all your work
from within a virtualenv so your python packages don't conflict with others on
the system.  Now's the time to get in your virtualenv!

If you're going to be contributing, please fork http://github.com/mozilla/FlightDeck
before continuing so you can push code to your own branches.  Then, download the
code, substituting your name::

    git clone git@github.com:{your-username}/FlightDeck.git  # if you're not a developer, just use "mozilla" for your-username
    cd FlightDeck

Install submodules::

    git submodule update --init --recursive

Install any compiled libraries::

    pip install -r requirements/compiled.txt

Configure the site by creating a settings_local.py in your root.  Anything you
put in here will override the defaults in settings.py.  An example follows, note
the first line is required::

    from settings import *

    DEBUG = True
    TEMPLATE_DEBUG = DEBUG

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': '',
            'USER': '',
            'PASSWORD': '',
            'HOST': '',
            'OPTIONS': {
                'init_command': 'SET storage_engine=InnoDB'
            },
            'TEST_CHARSET': 'utf8',
            'TEST_COLLATION': 'utf8_general_ci',

        }
    }

    UPLOAD_DIR = "/tmp/flightdeck"

    SESSION_COOKIE_SECURE = False

    ES_DISABLED = True # enable when ES daemon is running
    ES_HOSTS = ['127.0.0.1:9201']
    ES_INDEX = 'flightdeck'

    CACHES['default']['BACKEND'] =
    'django.core.cache.backends.locmem.LocMemCache'

If this is a brand new installation you'll need to configure a database as
well.  This command will build the structure::

    ./manage.py syncdb
    
If you're using Elastic Search locally then be sure to setup the ES index
mappings and index all your packages

    ./manage.py cron setup_mapping
    ./manage.py cron index_all

FlightDeck needs to know about all the SDKs you have availalbe.  This command
will make it look for them and initialize the database::

    ./manage.py add_core_lib jetpack-sdk-0.8

If you're writing code and would like to add some test data to the database
you can load some fixtures::

    ./manage.py loaddata users packages

You're all done!

Using Apache
------------

.. note::
    This isn't needed to run it locally. Simply use ``./manage.py
    runserver``

Production environments will expect to be running through another webserver.
Some example Apache configurations follow.

An example Apache .conf::

    <VirtualHost *:80>
        ServerAdmin your@mail.com
        ServerName flightdeck.some.domain

        <Directory /path/to/FlightDeck/apache/>
            Order deny,allow
            Allow from all
            Options Indexes FollowSymLinks
        </Directory>

        <Location "/adminmedia">
            SetHandler default
        </Location>
        Alias /adminmedia /path/to/FlightDeck/flightdeck/vendor/lib/python/django/contrib/admin/media

        <Location "/media/tutorial">
            SetHandler default
        </Location>
        Alias /media/tutorial /path/to/FlightDeck/flightdeck/apps/tutorial/media

        <Location "/media/api">
            SetHandler default
        </Location>
        Alias /media/api /path/to/FlightDeck/flightdeck/apps/api/media

        <Location "/media/jetpack">
            SetHandler default
        </Location>
        Alias /media/jetpack /path/to/FlightDeck/flightdeck/jetpack/media

        <Location "/media">
            SetHandler default
        </Location>
        Alias /media /path/to/FlightDeck/flightdeck/media

        LogLevel warn
        ErrorLog  /path/to/FlightDeck/logs/apache_error.log
        CustomLog /path/to/FlightDeck/logs/apache_access.log combined

        WSGIDaemonProcess flightdeck user=www-data group=www-data threads=25
        WSGIProcessGroup flightdeck

        WSGIScriptAlias / /path/to/FlightDeck/apache/config_local.wsgi
    </VirtualHost>

An example Apache WSGI configuration::

    import sys
    import os
    import site

    VIRTUAL_ENV = '/path/to/virtual/environment'
    PROJECT_PATH = '/path/to/projects/FlightDeck'

    # All directories which should on the PYTHONPATH
    ALLDIRS = [
	    os.path.join(VIRTUAL_ENV, 'lib/python2.6/site-packages'),
	    PROJECT_PATH,
	    os.path.join(PROJECT_PATH, 'flightdeck'),
    ]

    # Remember original sys.path.
    prev_sys_path = list(sys.path)

    # Add each new site-packages directory.
    for directory in ALLDIRS:
        site.addsitedir(directory)

    # add the app's directory to the PYTHONPATH
    # apache_configuration= os.path.dirname(__file__)
    # project = os.path.dirname(apache_configuration)
    # workspace = os.path.dirname(project)
    # sys.path.append(workspace)

    for s in ALLDIRS:
	    sys.path.append(s)

    # reorder sys.path so new directories from the addsitedir show up first
    new_sys_path = [p for p in sys.path if p not in prev_sys_path]
    for item in new_sys_path:
	    sys.path.remove(item)
	    sys.path[:0] = new_sys_path

    os.environ['VIRTUAL_ENV'] = VIRTUAL_ENV
    os.environ['CUDDLEFISH_ROOT'] = VIRTUAL_ENV
    os.environ['PATH'] = "%s:%s/bin" % (os.environ['PATH'], VIRTUAL_ENV)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'flightdeck.settings'

    import django.core.handlers.wsgi
    application = django.core.handlers.wsgi.WSGIHandler()


Recipes
===============


Import live database dump
-------------------------

How to import a database dump from live

    [sudo] mysql flightdeck < flightdeck_dump.sql
    
If you run into an error when importing large sql dump files, you may need to
 restart your mysqld process with this parameter.  

    mysqld --max_allowed_packet=32M
    
The database dump might be missing a row in django_sites table, so if you get a
django error saying "Site matching query does not exist" when you hit the login
page then insert a row into django_site.

    insert into django_site (id,domain,name) values (1,'example.com','example')
    
After importing the data, you will need to rebuild your ES index.


Rebuilding Elastic Search index
-------------------------------

Need to delete your Elastic Search index and start over?

    curl -XDELETE 'http://localhost:9201/flightdeck'
    ./manage.py cron setup_mapping
    ./manage.py cron index_all
    
    
Create a local super user account
---------------------------------

If you imported your database then you will need to create a user.

    ./manage.py createsuperuser
    
    