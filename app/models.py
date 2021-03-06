from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    api_key = db.Column(db.String(64), unique=True, index=True)
    site_entry = db.relationship('Site', backref='user', lazy='dynamic')

    def __str__(self):
        return self.name


class Site(db.Model):
    __tablename__ = 'sites'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    site_code = db.Column(db.String(10), unique=True)
    region = db.Column(db.String(100))
    type = db.Column(db.String(100))
    latitude = db.Column(db.String(50))
    longitude = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    hourly_data = db.relationship('HourlyData', backref='owner', lazy='dynamic')
    exceedence = db.relationship('Exceedence', backref='site', lazy='dynamic')

    @property
    def defra_url(self):
        return 'https://uk-air.defra.gov.uk/networks/site-info?site_id=' + self.site_code

    @property
    def map_url(self):
        return 'https://maps.google.co.uk/?q=' + self.latitude + self.longitude

    def __str__(self):
        return self.site_code


class DataMixin(object):
    ozone = db.Column(db.String(10), nullable=False)
    no2 = db.Column(db.String(10), nullable=False)
    so2 = db.Column(db.String(10), nullable=False)
    pm25 = db.Column(db.String(10), nullable=False)
    pm10 = db.Column(db.String(10), nullable=False)


class HourlyData(DataMixin, db.Model):
    __tablename__ = 'hourlydata'
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(20), nullable=False)
    site_id = db.Column(db.Integer, db.ForeignKey('sites.id'), nullable=False)
    exceedence = db.relationship('Exceedence', backref='data_entry', lazy='dynamic')

    @classmethod
    def recent(cls):
        year_clauses = []
        month_clauses = []
        month = datetime.today().month
        year = datetime.today().year
        year_clauses.append(cls.time.ilike('%{}%'.format(year)))
        if month < 4:
            year_clauses.append(cls.time.ilike('%{}%'.format(year - 1)))
            for i in range(4 - month):
                month_clauses.append(cls.time.ilike('%/{}/%'.format(12 - i)))
        for i in range (1, month + 1):
            month_clauses.append(cls.time.ilike('%/{}/%'.format(str(i).zfill(2))))
        return cls.query.filter(and_(or_(*month_clauses), or_(*year_clauses)))

    @property
    def high_pm10(self):
        try:
            if int(self.pm10) > 50:
                return True
        except ValueError:
            return


class Exceedence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    site_id = db.Column(db.Integer, db.ForeignKey('sites.id'), nullable=False)
    hourly_data_id = db.Column(db.Integer, db.ForeignKey('hourlydata.id'), nullable=False)
