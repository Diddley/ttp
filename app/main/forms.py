from flask import request
# from flask_uploads import UploadSet, IMAGES, configure_uploads, patch_request_class
from flask_wtf import FlaskForm, Form
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SelectField, SelectMultipleField, SubmitField, TextAreaField, BooleanField, SelectField, IntegerField, FloatField, FormField, TextAreaField, HiddenField, RadioField, Label
from wtforms.fields.core import Field, FieldList
from wtforms.fields.html5 import DateField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, Optional, Regexp
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms_alchemy import ModelForm, ModelFieldList, model_form_factory
from wtforms_alchemy.fields import ModelFormField
from app.models import Academic, CohortFunding, User, Division, Club, Contact, Prison, Category, Cohort, Comment, Kit, Funding, Media, Course, Probation, Stock, KitItem, KitOrder, stockItem, Inventory
from app import db, images
from datetime import datetime

# -------- NEW/CREATE forms ---------------------


class NewDivisionForm(FlaskForm):
    division = StringField('Division', validators=[DataRequired()])
    submit = SubmitField('Add Division')

    def validate_division(self, division):
        div_name = Division.query.filter_by(div_desc=division.data).first()
        if div_name is not None:
            raise ValidationError('This Division is already in the system')


class NewCourseForm(FlaskForm):
    course = StringField('Course', validators=[DataRequired()])
    submit = SubmitField('Add Course')

    def validate_course(self, course):
        course_name = Course.query.filter_by(course_type=course.data).first()
        if course_name is not None:
            raise ValidationError('A course with this name already exists.')


class NewCohFundForm(FlaskForm):
    fund_source = StringField('Funding Source', validators=[DataRequired()])
    submit = SubmitField('Add Funding Source')

    def validate_course(self, funding):
        fund_source = CohortFunding.query.filter_by(
            cf_desc=funding.data).first()
        if fund_source is not None:
            raise ValidationError(
                'A funding source with this name already exists.')


class NewAcademicForm(FlaskForm):
    inst = StringField('Institution', validators=[DataRequired()])
    submit = SubmitField('Add Academic Institution')

    def validate_course(self, inst):
        inst_name = Academic.query.filter_by(aca_desc=inst.data).first()
        if inst_name is not None:
            raise ValidationError(
                'An institution  with this name already exists.')


class NewClubForm(FlaskForm):
    clubname = StringField('Club Name', validators=[DataRequired()])
    club_town = StringField('Town', validators=[DataRequired()])
    club_postcode = StringField('PostCode', validators=[DataRequired()])
    club_division = QuerySelectField('Division', validators=[DataRequired(
    )], query_factory=lambda: Division.query, get_label="div_desc")
    club_contract = BooleanField('Signed Contract Agreement Received')
    club_collab = BooleanField('Signed Collaboration Agreement Received')
    club_fundingapp = BooleanField('Funding Application Received')
    club_badge = FileField('Upload Badge', validators=[
        FileAllowed(images, 'Images only!')])
    submit = SubmitField('Add Club')

    def validate_clubname(self, clubname):
        club = Club.query.filter_by(clb_name=clubname.data).first()
        if club is not None:
            raise ValidationError('This club is already in the system.')


class NewContactForm(FlaskForm):
    con_firstname = StringField('First Name', validators=[DataRequired()])
    con_surname = StringField('Surname')
    con_title = StringField('Job Title', validators=[Optional()])
    con_email = StringField('Email', validators=[DataRequired(), Email()])
    email2 = StringField('Verify Email', validators=[DataRequired(), EqualTo(
        'con_email', message="The email addresses do not match")])
    con_phone = StringField('Phone', validators=[Length(max=20)])
    con_club = QuerySelectField('Club', validators=[Optional()], query_factory=lambda: Club.query.order_by(
        'clb_name'), get_label="clb_name", allow_blank=True)
    con_prs = QuerySelectField('Prison', validators=[Optional(
    )], query_factory=lambda: Prison.query.order_by('prs_name'), get_label="prs_name", allow_blank=True, default='prison.prs_name')
    con_prob = QuerySelectField('Probation Service', validators=[Optional(
    )], query_factory=lambda: Probation.query.order_by('prob_name'), get_label="prob_name", allow_blank=True)
    submit = SubmitField('Add Contact')

    def validate_contact_email(self, con_email):
        email = Contact.query.filter_by(con_email=con_email.data).first()
        if email is not None:
            raise ValidationError(
                'A contact with this email address is already in the system')


class NewCategoryForm(FlaskForm):
    cat_shortcode = StringField('Short Code', validators=[DataRequired()])
    cat_desc = StringField('Category', validators=[DataRequired()])
    submit = SubmitField('Add Category')

    def validate_shortcode(self, cat_shortcode):
        cat_sc = Category.query.filter_by(
            cat_shortcode=cat_shortcode.data).first()
        if cat_sc is not None:
            raise ValidationError('This code has already been used')

    def validate_category(self, cat_desc):
        cat = Category.query.filter_by(cat_desc=cat_desc.data).first()
        if cat is not None:
            raise ValidationError('This category already exists')


class NewPrisonForm(FlaskForm):
    prs_name = StringField('Prison Name', validators=[DataRequired()])
    prs_town = StringField('Town', validators=[DataRequired()])
    prs_postcode = StringField('PostCode', validators=[DataRequired()])
    prs_cat = QuerySelectField('Category', validators=[DataRequired(
    )], query_factory=lambda: Category.query, get_label="cat_desc")
    prs_upshot = BooleanField('Upshot')
    submit = SubmitField('Add Prison')

    def validate_prison(self, prs_name):
        pris = Prison.query.filter_by(prs_name=prs_name.data).first()
        if pris is not None:
            raise ValidationError('This Prison already exists!')


class NewProbServiceForm(FlaskForm):
    prob_name = StringField('Probation Service Name',
                            validators=[DataRequired()])
    prob_town = StringField('Town', validators=[DataRequired()])
    prob_postcode = StringField('PostCode', validators=[DataRequired()])
    submit = SubmitField('Add Probation Service')

    def validate_probservice(self, prob_name):
        prob = Probation.query.filter_by(prob_name=prob_name.data).first()
        if prob is not None:
            raise ValidationError('This Probation Service already exists!')


class NewCohortForm(FlaskForm):
    coh_desc = StringField('Cohort Name (optional)')
    coh_club = QuerySelectField('Club', validators=[DataRequired(
    )], query_factory=lambda: Club.query.order_by(Club.clb_name.asc()), get_label="clb_name")
    coh_prison = QuerySelectField('Prison', validators=[Optional(
    )], query_factory=lambda: Prison.query.order_by(Prison.prs_name.asc()), get_label="prs_name", allow_blank=True)
    coh_prob = QuerySelectField('Probation Services', validators=[Optional(
    )], query_factory=lambda: Probation.query.order_by(Probation.prob_name.asc()), get_label="prob_name", allow_blank=True)
    coh_startDate = DateField('Start Date', validators=[
                              DataRequired()], format='%Y-%m-%d', default=datetime.utcnow)
    coh_endDate = DateField('End Date', validators=[
                            Optional()], format='%Y-%m-%d')
    coh_course = QuerySelectField('Course', validators=[
    ], query_factory=lambda: Course.query, get_label="course_type")
    coh_parts = IntegerField('Number of participants',
                             validators=[DataRequired()])
    coh_freq = StringField('Frequency', validators=[DataRequired()])
    coh_funds = QuerySelectField('Funding', validators=[DataRequired(
    )], query_factory=lambda: CohortFunding.query.order_by(CohortFunding.cf_desc.asc()), get_label="cf_desc")
    coh_aca = QuerySelectField('Academic Partner', validators=[DataRequired(
    )], query_factory=lambda: Academic.query.order_by(Academic.aca_desc.asc()), get_label="aca_desc")
    submit = SubmitField('Create Cohort')

    def validate_date(self, coh_startDate, coh_endDate):
        if coh_endDate:
            if datetime.date(coh_endDate.data) < datetime.date(coh_startDate.data):
                raise ValidationError('End date should be after Start Date')

    def validate_entity(self, coh_prison, coh_prob):
        pris = coh_prison.data
        prob = coh_prob.data
        if not pris and not prob:
            raise ValidationError(
                'Please select either a Prison or Probabtion Service')


class NewCommentForm(FlaskForm):
    body = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Add Comment')


class CommentForm(FlaskForm):
    body = TextAreaField('Comment', validators=[DataRequired()])
    com_club = QuerySelectField('Club', validators=[Optional(
    )], query_factory=lambda: Club.query.order_by(Club.clb_name.asc()), get_label="clb_name", allow_blank=True)
    com_prs = QuerySelectField('Prison', validators=[Optional(
    )], query_factory=lambda: Prison.query.order_by(Prison.prs_name.asc()), get_label="prs_name", allow_blank=True)
    com_prob = QuerySelectField('Probabtion Services', validators=[Optional(
    )], query_factory=lambda: Probation.query.order_by(Probation.prob_name.asc()), get_label="prob_name", allow_blank=True)
    com_date = DateField('Due Date', validators=[
        Optional()], format='%Y-%m-%d')
    submit = SubmitField('Add Comment')

    def __init__(self, id, source, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.id = id
        self.source = source


class NewMediaForm(FlaskForm):
    med_clubid = QuerySelectField('Club', validators=[Optional(
    )], query_factory=lambda: Club.query, get_label="clb_name")
    med_prisonid = QuerySelectField('Prison', validators=[Optional(
    )], query_factory=lambda: Prison.query, get_label="prs_name", allow_blank=True)
    med_probid = QuerySelectField('Probabtion Services', validators=[Optional(
    )], query_factory=lambda: Probation.query, get_label="prob_name", allow_blank=True)
    med_date = DateField('Date', default=datetime.utcnow)
    med_medium = SelectField('Medium', choices=[('TV', 'TV'), ('Online', 'Online'),  ('National Radio', 'National Radio'), (
        'Regional Radio', 'Regional Radio'),  ('National Paper', 'National Paper'), ('Regional Paper', 'Regional Paper')])
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


class NewStockItemForm(FlaskForm):
    item_sku = StringField('SKU', validators=[DataRequired()])
    item_desc = StringField('Description', validators=[DataRequired()])
    item_size = StringField('Size', validators=[DataRequired()])
    item_qty = StringField('Opening Stock', validators=[Optional()])
    submit = SubmitField('Add Item')

    def validate_sku(self, item_sku):
        item = stockItem.query.filter_by(sku=item_sku.data).first()
        if item is not None:
            raise ValidationError('This SKU already exists!')


class NewLinkForm(FlaskForm):
    lnk_club = QuerySelectField('Club', validators=[Optional(
    )], query_factory=lambda: Club.query.order_by(Club.clb_name.asc()), get_label="clb_name")
    lnk_prs = QuerySelectField('Prison', validators=[Optional(
    )], query_factory=lambda: Prison.query.order_by(Prison.prs_name.asc()), get_label="prs_name", allow_blank=True)
    lnk_prob = QuerySelectField('Probation Service', validators=[Optional(
    )], query_factory=lambda: Probation.query.order_by(Probation.prob_name.asc()), get_label="prob_name", allow_blank=True)
    submit = SubmitField('Create Link')


# ---------- EDIT/UPDATE forms ---------------

class EditCommentForm(FlaskForm):
    referer = HiddenField('refer')
    body = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Edit Comment')

    def __init__(self, id, *args, **kwargs):
        super(EditCommentForm, self).__init__(*args, **kwargs)
        self.id = id


class EditContactForm(FlaskForm):
    con_firstname = StringField('First Name', validators=[DataRequired()])
    con_surname = StringField('Surname')
    con_title = StringField('Job Title', validators=[Optional()])
    con_email = StringField('Email', validators=[DataRequired(), Email()])
    email2 = StringField('Verify Email', validators=[DataRequired(), EqualTo(
        'con_email', message="The email addresses do not match")])
    con_phone = StringField('Phone', validators=[Length(max=20)])
    submit = SubmitField('Update')

    def __init__(self, id, *args, **kwargs):
        super(EditContactForm, self).__init__(*args, **kwargs)
        self.id = id

    def validate_contact_email(self, con_email):
        email = Contact.query.filter_by(con_email=con_email.data).first()
        if email is not None:
            raise ValidationError(
                'A contact with this email address is already in the system')


class EditClubForm(FlaskForm):
    clubname = StringField('Club Name', validators=[DataRequired()])
    club_town = StringField('Town')
    club_postcode = StringField('PostCode')
    club_division = QuerySelectField('Division', validators=[DataRequired(
    )], query_factory=lambda: Division.query, get_label="div_desc")
    club_contract = BooleanField('Signed Contract Agreement Received')
    club_collab = BooleanField('Signed Collaboration Agreement Received')
    club_fundingapp = BooleanField('Funding Application Received')
    club_badge = FileField('Upload Badge', validators=[
        FileAllowed(images, 'Images only!')])
    submit = SubmitField('Save Changes')

    def __init__(self, id, *args, **kwargs):
        super(EditClubForm, self).__init__(*args, **kwargs)
        self.id = id


class EditPrisonForm(FlaskForm):
    prs_name = StringField('Prison Name', validators=[DataRequired()])
    prs_town = StringField('Town', validators=[DataRequired()])
    prs_postcode = StringField('PostCode', validators=[DataRequired()])
    prs_cat = QuerySelectField('Category', validators=[DataRequired(
    )], query_factory=lambda: Category.query, get_label="cat_desc")
    prs_upshot = BooleanField('Upshot')
    submit = SubmitField('Save Changes')

    def __init__(self, id, *args, **kwargs):
        super(EditPrisonForm, self).__init__(*args, **kwargs)
        self.id = id


class EditProbationForm(FlaskForm):
    prob_name = StringField('Probation Service Name',
                            validators=[DataRequired()])
    prob_town = StringField('Town', validators=[DataRequired()])
    prob_postcode = StringField('PostCode', validators=[DataRequired()])
    submit = SubmitField('Save Changes')

    def __init__(self, id, *args, **kwargs):
        super(EditProbationForm, self).__init__(*args, **kwargs)
        self.id = id


class EditCohortForm(FlaskForm):
    coh_desc = StringField('Cohort Name (optional)', validators=[Optional()])
    coh_club = QuerySelectField('Club', validators=[DataRequired(
    )], query_factory=lambda: Club.query, get_label="clb_name")
    coh_prison = QuerySelectField('Prison', validators=[Optional(
    )], query_factory=lambda: Prison.query, get_label="prs_name", allow_blank=True)
    coh_probserv = QuerySelectField('Probation Service', validators=[Optional(
    )], query_factory=lambda: Probation.query, get_label="prob_name", allow_blank=True)
    coh_startDate = DateField('Start Date', validators=[
                              DataRequired()], format='%Y-%m-%d')
    coh_endDate = DateField('End Date', validators=[
                            Optional()], format='%Y-%m-%d')
    coh_freq = StringField('Frequency', validators=[DataRequired()])
    coh_course = QuerySelectField(
        'Course', query_factory=lambda: Course.query, get_label="course_type")
    coh_participants = IntegerField(
        'Participants', validators=[DataRequired()])
    coh_grads = IntegerField('Graduates', validators=[Optional()])
    coh_freq = StringField('Frequency', validators=[DataRequired()])
    coh_funds = QuerySelectField('Funding', validators=[DataRequired(
    )], query_factory=lambda: CohortFunding.query.order_by(CohortFunding.cf_desc.asc()), get_label="cf_desc")
    coh_aca = QuerySelectField('Academic Partner', validators=[DataRequired(
    )], query_factory=lambda: Academic.query.order_by(Academic.aca_desc.asc()), get_label="aca_desc")

    submit = SubmitField('Save Changes')

    def __init__(self, id, *args, **kwargs):
        super(EditCohortForm, self).__init__(*args, **kwargs)
        self.id = id

    def validate_date(self, coh_startDate, coh_endDate):
        if coh_endDate.data:
            if coh_endDate.data < coh_startDate.data:
                raise ValidationError('End Date should be after Start Date')

    def validate_entity(self, coh_prison, coh_probserv):
        pris = coh_prison.data
        prob = coh_probserv.data
        if not pris and not prob:
            raise ValidationError(
                'Please select either a Prison or a Probation Service')


class TPIForm(FlaskForm):
    coh_tpi = BooleanField('')


BaseModelForm = model_form_factory(FlaskForm)


class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session


# class UpdateItemForm(ModelForm):
#     class Meta:
#         model = stockItem


# class UpdateStockForm(ModelForm):
#     class Meta:
#         model = Inventory
#         include_foreign_keys = True
#         include = ['sku']

# class UpdateItemForm(FlaskForm):
#     item_desc = QuerySelectField('Item', validators=[DataRequired(
#     )], query_factory=lambda: stockItem.query.group_by(stockItem.item_desc), get_label="item_desc")
#     item_size = QuerySelectField('Size', validators=[DataRequired(
#     )], query_factory=lambda: stockItem.query.group_by(stockItem.item_size), get_label="item_size")


# class UpdateStockForm(FlaskForm):
#     stock_item = FormField(UpdateItemForm)
#     item_qty = IntegerField('Qty', validators=[DataRequired()])
#     submit = SubmitField('Update Stock')

# class UpdateStockForm(FlaskForm):
#     item_desc = SelectField('Item', choices=[])
#     item_size = SelectField('Size', choices=[])
#     item_qty = IntegerField('Qty', validators=[DataRequired()])
#     submit = SubmitField('Update Stock')

class UpdateItemForm(FlaskForm):
    stock_desc = SelectField(
        'Stock Item', validators=[DataRequired()])
    stock_qty = IntegerField('Qty', validators=[DataRequired()])
    submit = SubmitField('Update Stock')

    def __init__(self, *args, **kwargs):
        super(UpdateItemForm, self).__init__(*args, **kwargs)
        self.stock_desc.choices = [(si.item_sku, si.item_desc + ' (' + si.item_size + ')')
                                   for si in stockItem.query.all()]


class BatchUpdateItemForm(Form):
    stock_qty = IntegerField('Qty', validators=[Optional()])


class UpdateStockForm(FlaskForm):
    items = FieldList(FormField(BatchUpdateItemForm), min_entries=1)
    submit = SubmitField('Update Stock')


# ---- DELETE form --------------


class DeleteForm(FlaskForm):
    submit = SubmitField('Confirm')

    def __init__(self, id, *args, **kwargs):
        super(DeleteForm, self).__init__(*args, **kwargs)
        self.id = id


class DeleteCommentForm(FlaskForm):
    referer = HiddenField('refer')
    body = StringField('Comment', validators=[DataRequired()])
    submit = SubmitField('Delete Comment')

    def __init__(self, id, *args, **kwargs):
        super(DeleteCommentForm, self).__init__(*args, **kwargs)
        self.id = id
