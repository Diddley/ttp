from flask import request
from flask_uploads import UploadSet, IMAGES, configure_uploads, patch_request_class
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SelectField, SubmitField, DateField, TextAreaField, BooleanField, SelectField, IntegerField, FloatField, FormField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, Optional, Regexp
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from app.models import User, Division, Club, Contact, Prison, Category, Cohort, Comment, Kit, Funding, Media, Course, Probation
from app import db, images
from datetime import datetime




class NewDivisionForm(FlaskForm):
    division = StringField('Division', validators = [DataRequired()])
    submit = SubmitField('Add Division')

    def validate_division(self, division):
        div_name = Division.query.filter_by(div_desc=division.data).first()
        if div_name is not None:
            raise ValidationError('This Division is already in the system')




class NewClubForm(FlaskForm):
    clubname = StringField('Club Name', validators = [DataRequired()])
    club_town = StringField('Town', validators = [DataRequired()])
    club_postcode = StringField('PostCode', validators =[DataRequired()])
    club_division = QuerySelectField('Division', validators=[DataRequired()], query_factory=lambda : Division.query, get_label="div_desc")
    club_contract = BooleanField('Signed Contract Agreement Received')
    club_collab = BooleanField('Signed Collaboration Agreement Received')
    club_fundingapp = BooleanField('Funding Application Received')
    club_badge = FileField('Upload Badge', validators=[FileAllowed(images, 'Images only!')])
    submit = SubmitField('Add Club')

    def validate_clubname(self, clubname):
        club = Club.query.filter_by(clb_name = clubname.data).first()
        if club is not None:
            raise ValidationError('This club is already in the system.')


class NewContactForm(FlaskForm):
    con_firstname = StringField('First Name', validators=[DataRequired()])
    con_surname = StringField('Surname')
    con_email = StringField('Email', validators = [DataRequired(), Email()])
    email2 = StringField('Verify Email', validators = [DataRequired(), EqualTo('con_email', message="The email addresses do not match")])
    con_phone = StringField('Phone', validators=[DataRequired()])
    con_club = QuerySelectField('Club', validators=[Optional()], query_factory=lambda : Club.query.order_by('clb_name'), get_label="clb_name", allow_blank=True)
    con_prs = QuerySelectField('Prison', validators=[Optional(
    )], query_factory=lambda: Prison.query.order_by('prs_name'), get_label="prs_name", allow_blank=True, default='prison.prs_name')
    con_prob = QuerySelectField('Probation Service', validators=[Optional()], query_factory=lambda: Probation.query.order_by('prob_name'), get_label="prob_name", allow_blank=True)
    submit = SubmitField('Add Contact')

    def validate_contact_email(self, con_email):
        email = Contact.query.filter_by(con_email=con_email.data).first()
        if email is not None:
            raise ValidationError('A contact with this email address is already in the system')



class NewCategoryForm(FlaskForm):
    cat_shortcode = StringField('Short Code', validators = [DataRequired()])
    cat_desc = StringField('Category', validators = [DataRequired()])
    submit = SubmitField('Add Category')

    def validate_shortcode(self, cat_shortcode):
        cat_sc = Category.query.filter_by(cat_shortcode=cat_shortcode.data).first()
        if cat_sc is not None:
            raise ValidationError('This code has already been used')

    def validate_category(self, cat_desc):
        cat = Category.query.filter_by(cat_desc=cat_desc.data).first()
        if cat is not None:
            raise ValidationError('This category already exists')

class NewPrisonForm(FlaskForm):
    prs_name = StringField('Prison Name', validators = [DataRequired()])
    prs_town = StringField('Town', validators=[DataRequired()])
    prs_postcode = StringField('PostCode', validators =[DataRequired()])
    prs_cat = QuerySelectField('Category', validators=[DataRequired()], query_factory=lambda : Category.query, get_label="cat_desc")
    submit = SubmitField('Add Prison')
    
    def validate_prison(self, prs_name):
        pris = Prison.query.filter_by(prs_name=prs_name.data).first()
        if pris is not None:
            raise ValidationError('This Prison already exists!')


class NewProbServiceForm(FlaskForm):
    prob_name = StringField('Probation Service Name', validators=[DataRequired()])
    prob_town = StringField('Town', validators=[DataRequired()])
    prob_postcode = StringField('PostCode', validators=[DataRequired()])
    submit = SubmitField('Add Probation Service')

    def validate_probservice(self, prob_name):
        prob = Probabtion.query.filter_by(prob_name = prob_name.data).first()
        if prob is not None:
            raise ValidationError('This Probation Service already exists!')


class NewCohortForm(FlaskForm):
    coh_desc = StringField('Cohort Name (optional)')
    coh_club = QuerySelectField('Club', validators=[DataRequired()], query_factory=lambda : Club.query, get_label="clb_name")
    coh_prison = QuerySelectField('Prison', validators=[Optional()], query_factory=lambda : Prison.query, get_label="prs_name", allow_blank=True)
    coh_prob = QuerySelectField('Probation Services', validators=[Optional()], query_factory=lambda:Probation.query, get_label="prob_name", allow_blank=True)
    coh_startDate = DateField('Start Date',validators=[DataRequired()], format='%Y-%m-%d', default=datetime.utcnow)
    coh_endDate = DateField('End Date', validators=[
                            DataRequired()], format='%Y-%m-%d')
    coh_course = QuerySelectField('Course', validators=[], query_factory=lambda : Course.query, get_label="course_type")
    coh_parts = IntegerField('Number of participants', validators=[DataRequired()])
    submit = SubmitField('Create Cohort')

    def validate_date(self, coh_startDate, coh_endDate):
        if date(coh_endDate.data) < date(coh_startDate.data):
            raise ValidationError('End date should be after Start Date')
    
    def validate_entity(self, coh_prison, coh_prob):
        pris = coh_prison.data
        prob = coh_prob.data
        if not pris and not prob:
            raise ValidationError('Please select either a Prison or Probabtion Service')

class NewCommentForm(FlaskForm):
    body = TextAreaField('Comment', validators=[Length(min=0, max=140)])
    submit = SubmitField('Add Comment')



class EditCohortForm(FlaskForm):
    coh_desc = StringField('Cohort Name (optional)')
    coh_club = StringField('Club')
    coh_prison = StringField('Prison')
    coh_probserv = StringField('Probation Service')
    coh_startDate = DateField('Start Date', validators=[
                              DataRequired()], format='%Y-%m-%d', default=datetime.utcnow)
    coh_endDate = DateField('End Date', validators=[DataRequired()])
    coh_course = QuerySelectField('Course')
    coh_participants = IntegerField('Participants')
    coh_grads = IntegerField('Graduates')
    coh_tpi = BooleanField('TPI')
    submit = SubmitField('Edit Cohort')

    def __init__(self, id, *args, **kwargs):
        super(EditCohortForm, self).__init__(*args, **kwargs)
        self.id = id

class TPIForm(FlaskForm):
    coh_tpi = BooleanField('')

class NewMediaForm(FlaskForm):
    med_clubid = QuerySelectField('Club', validators=[Optional()], query_factory=lambda : Club.query, get_label="clb_name")
    med_prisonid = QuerySelectField('Prison', validators=[Optional()], query_factory= lambda : Prison.query, get_label="prs_name", allow_blank=True)
    med_probid = QuerySelectField('Probabtion Services', validators=[Optional()], query_factory=lambda:Probation.query, get_label="prob_name", allow_blank=True)
    med_date = DateField('Date', default=datetime.utcnow)
    med_medium = SelectField('Medium', choices=[('TV','TV'), ('Online','Online'),  ('National Radio','National Radio'), ('Regional Radio', 'Regional Radio'),  ('National Paper', 'National Paper'), ('Regional Paper', 'Regional Paper') ])
    med_publication = StringField('Publication')
    med_link = StringField('Link')
    med_author = StringField('Author')
    # med_comment = FormField(NewCommentForm)
    submit = SubmitField('Add Media')


class NewKitForm(FlaskForm):
    kit_small = IntegerField('Small')
    kit_medium = IntegerField('Medium')
    kit_large = IntegerField('Large')
    kit_date = DateField('Date', default=datetime.utcnow)
    submit = SubmitField('Add Kit')


class NewFundingForm(FlaskForm):
    fnd_date = DateField('Date', default=datetime.utcnow)
    fnd_amount = FloatField('Amount £')
    # fnd_comment = FormField(NewCommentForm)
    submit = SubmitField('Assign Funds')





        


