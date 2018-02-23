A REST API to serve air quality data from a database of monitoring sites in the UK's automatic monitoring network.   

It is built on the Python framework Flask and the Flask-SQLAlchemy extension. 

The project is used to provide hourly mean air pollution measurements since September 2017 at www.air-aware.com


Getting Started
---------------


**Prerequisites**

Python 3.4, pip, virtualenv

**1. Clone or copy repository**

**2. Set up Virtual Environment**

Create a virtual environment named aurn-venv:

    $ virtualenv aurn-venv

Activate the virtual environment:

    $ source aurn-venv/bin/activate
    (aurn-venv) $

Use *pip* to install requirements:

    (aurn-venv) $ pip install requirements.txt

Verify that packages have been installed:

    (aurn-venv) $ pip freeze
    Flask==0.12
    Flask_SQLAlchemy==2.1
    flask-marshmallow==0.8.0
    pytz==2017.2
    flask-migrate==2.1.1
    requests==2.13.0
    beautifulsoup4==4.6.0

**3. Push Flask application context**

Run the following commands in Python within the virtual environment:

    >>> from app import create_app()

    >>> create_app().app_context().push()


Create and populate a database using the create_db() and update_db() functions.

    >>> from app.data.hourly import create_db, update_db

    >>> create_db()

    >>> update_db()

The create_db() function creates the database schema. The update_db() function runs the webscraping script and inserts the air quality data in the 'data' table. This should be set up to run on an hourly basis; n.b. the webpage https://uk-air.defra.gov.uk/latest/currentlevels updates at 40 minutes past the hour.


**4. Configure and run the API**

After ensuring correct settings within app/config, the database can be queried through the API after running the server:

    $ python run.py
