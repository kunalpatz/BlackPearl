from database.db import db


class App(db.Document):
    name = db.StringField(required=True, unique=True)
    email = db.StringField(required=True, unique=True)
    user = db.StringField(required=True, unique=True)
    site = db.StringField(required=True)
    key = db.StringField(required=True)

class Data(db.Document):
    exec_date = db.DateTimeField(required=True)
    ip = db.StringField(required=True)
    continent = db.StringField()
    country = db.StringField()
    last_analysis_results = db.DictField()
    last_analysis_stats = db.DictField()
    regional_internet_registry = db.StringField()
    whois = db.StringField()
    # genres = db.ListField(db.StringField(), required=True)

class Domain(db.Document):
    exec_date = db.DateTimeField(required=True)
    domain = db.StringField()
    categories = db.DictField()
    last_analysis_results = db.DictField()
    last_analysis_stats = db.DictField()
    popularity_ranks = db.DictField()
    registrar = db.StringField()
    whois = db.StringField()


