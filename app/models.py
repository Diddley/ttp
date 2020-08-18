from flask import current_app
from datetime import datetime
from hashlib import md5
from flask_login import UserMixin
from time import time
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import jwt
from app import db, login 


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    password_hash = db.Column(db.String(128))
    profile = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    comments =db.relationship('Comment', backref='author', lazy="dynamic")

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_password_reset_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256'
        ).decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Division(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    div_desc = db.Column(db.String(60), index = True, unique = True)
    clubs = db.relationship('Club', backref='member', lazy='dynamic')

    def __repr__(self):
        return '<Division {}>'.format(self.div_desc)


class Club(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    clb_name = db.Column(db.String(40), index = True, unique = True)
    clb_town = db.Column(db.String(40), index= True)
    clb_postcode = db.Column(db.String(10), index = True)
    division_id = db.Column(db.Integer, db.ForeignKey('division.id'))
    clb_badge =db.Column(db.String(40))
    clb_contract = db.Column(db.Boolean)
    clb_collab = db.Column(db.Boolean)
    clb_fundingapp = db.Column(db.Boolean)
    # clb_twinned_id = db.Column(db.Integer, db.ForeignKey('prison.id'))
    clb_contact = db.relationship('Contact', backref='contact', lazy='dynamic')
    clb_cohort = db.relationship('Cohort', backref='clb_cohort', lazy = 'dynamic')
    clb_media = db.relationship('Media', backref='clb_press', lazy = 'dynamic')

    def __repr__(self):
        return '<Club {}>'.format(self.clb_name)
    
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    con_firstname = db.Column(db.String(64))
    con_surname = db.Column(db.String(64), index = True)
    con_email = db.Column(db.String(120), index = True, unique = True)
    con_phone = db.Column(db.String(11), index = True)
    con_club = db.Column(db.Integer, db.ForeignKey('club.id'))

    def __repr__(self):
        return '<Contact {} {}>'.format(self.con_firstname, self.con_surname)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    cat_shortcode = db.Column(db.String(3), index=True, unique = True)
    cat_desc = db.Column(db.String(30), index = True, unique = True)
    cat_prison = db.relationship('Prison', backref='prison', lazy='dynamic')

    def __repr__(self):
        return '<Cat {}>'.format(self.cat_desc)

class Prison(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    prs_name = db.Column(db.String(120), index = True, unique = True)
    prs_town = db.Column(db.String(40), index = True)
    prs_category = db.Column(db.Integer, db.ForeignKey('category.id'))
    prs_cohort = db.relationship('Cohort', backref='prs_cohort', lazy="dynamic")
    prs_media = db.relationship('Media', backref='prs_press', lazy='dynamic')
    # prs_club = db.relationship('Club', backref='prs_club', lazy='dynamic')

    def __repr__(self):
        return '<Prison {}>'.format(self.prs_name)


class Cohort(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    coh_desc = db.Column(db.String(40))
    coh_clubid = db.Column(db.Integer, db.ForeignKey('club.id'))
    coh_prisonid = db.Column(db.Integer, db.ForeignKey('prison.id'))
    coh_startDate = db.Column(db.DateTime)
    coh_endDate = db.Column(db.DateTime)
    coh_deliveryDate = db.Column(db.DateTime)
    coh_tpi = db.Column(db.Boolean)
    coh_comment = db.relationship('Comment', backref='owner', lazy= "dynamic")
    coh_kit = db.relationship('Kit', backref='wearer', lazy='dynamic')
    coh_funding = db.relationship('Funding', backref='funded', lazy='dynamic')
    
    def __repr__(self):
        return '<Cohort {}>'.format(self.coh_desc)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index = True, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    cohort_id = db.Column(db.Integer, db.ForeignKey('cohort.id'))
    fnd_id = db.Column(db.Integer, db.ForeignKey('funding.id'))
    med_id = db.Column(db.Integer, db.ForeignKey('media.id'))

    def __repr__(self):
        return '<Comment {}>'.format(self.body)

class Kit(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    kit_cohortid = db.Column(db.Integer, db.ForeignKey('cohort.id'))
    kit_numSmall = db.Column(db.Integer)
    kit_numMedium = db.Column(db.Integer) 
    kit_numLarge = db.Column(db.Integer)
    kit_date = db.Column(db.DateTime, index=True, default = datetime.today())

    def __repr__(self):
        return '<Kit S {} M {} L {}>'.format(self.kit_numSmall, self.kit_numMedium, self.kit_numLarge)

class Funding(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fnd_cohort = db.Column(db.Integer, db.ForeignKey('cohort.id'))
    fnd_date = db.Column(db.DateTime, index=True, default = datetime.today())
    fnd_amount = db.Column(db.Float)
    fnd_comment = db.relationship('Comment', backref='fnd_owner', lazy='dynamic')

    def __repr__(self):
        return '<Funding {} £ {}>'.format(self.fnd_cohort, self.fnd_amount)
        

class Media(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    med_clubid = db.Column(db.Integer, db.ForeignKey('club.id'))
    med_prisonid = db.Column(db.Integer, db.ForeignKey('prison.id'))
    med_date = db.Column(db.DateTime)
    med_medium = db.Column(db.String(40))
    med_publication = db.Column(db.String(40))
    med_link = db.Column(db.String(120))
    med_author = db.Column(db.String(60))
    med_comment = db.relationship('Comment', backref='med_owner', lazy = 'dynamic')

    def __repr__(self):
        return '<Media {}>'.format(self.med_publication)