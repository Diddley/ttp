from datetime import datetime, date
from flask import render_template, flash, redirect, url_for, jsonify, current_app, request
from flask_login import current_user, login_required
from app import db
from app.main.forms import NewClubForm, NewDivisionForm, NewContactForm, NewCategoryForm, NewPrisonForm, NewCohortForm, EditCohortForm, NewCommentForm, TPIForm, NewMediaForm, NewFundingForm
from app.models import User, Club, Division, Contact, Category, Prison, Cohort, Comment, Media, Funding
from app.main import bp

@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()

@bp.route('/', methods = ['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html', title = 'Home')


@bp.route('/clubs')
def clubs():
    page = request.args.get('page',1, type=int)
    clubs = Club.query.order_by(Club.name.asc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False)   
    next_url = url_for('main.clubs', page = clubs.next_num) if clubs.has_next else None
    prev_url = url_for('main.clubs', page = clubs.prev_num) if clubs.has_prev else None
    return render_template('club.html', title = 'Clubs', clubs = clubs.items, next_url = next_url, prev_url = prev_url)


@bp.route('/contacts')
def contacts():
    page = request.args.get('page', 1, type=int)
    contacts = Contact.query.join(Club).order_by(Club.name.asc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for(
        'main.contacts', page=contacts.next_num) if contacts.has_next else None
    prev_url = url_for(
        'main.contacts', page=contacts.prev_num) if contacts.has_prev else None
    return render_template('contact.html', title='Contacts', contacts = contacts.items, next_url=next_url, prev_url=prev_url)

@bp.route('/prisons')
def prisons():
    page = request.args.get('page', 1, type=int)
    prisons = Prison.query.join(Category).order_by(Prison.prs_name.asc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for(
        'main.prisons', page=prisons.next_num) if prisons.has_next else None
    prev_url = url_for(
        'main.prisons', page=prisons.prev_num) if prisons.has_prev else None
    return render_template('prison.html', title = 'Prisons', prisons = prisons.items, next_url=next_url, prev_url=prev_url)

@bp.route('/cohorts')
def cohorts():
    page = request.args.get('page', 1, type=int)
    cohorts = Cohort.query.order_by(Cohort.coh_startDate.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for(
        'main.cohorts', page=cohorts.next_num) if cohorts.has_next else None
    prev_url = url_for(
        'main.cohorts', page=cohorts.prev_num) if cohorts.has_prev else None
    return render_template('cohort.html', title='Cohorts', cohorts = cohorts.items, next_url=next_url, prev_url=prev_url)


@bp.route('/cohort/<id>')
@login_required
def cohort(id):
    cohort = Cohort.query.filter_by(id=id).first_or_404()
    funding = Funding.query.filter_by(fnd_cohort=id).all()
    totalfunding = 0
    for fund in funding:
        totalfunding+=float(fund.fnd_amount)
    # form = TPIForm()
    page = request.args.get('page', 1, type=int)
    comments = cohort.coh_comment.order_by(Comment.timestamp.desc()).paginate(
        page, current_app.config['COMMENTS_PER_PAGE'], False)
    next_url = url_for('main.cohort', id=id, page = comments.next_num) if comments.has_next else None 
    prev_url = url_for('main.cohort', id=id, page = comments.prev_num) if comments.has_prev else None
    return render_template('cohortdetails.html', cohort=cohort, comments=comments.items, id=id, totalfunding=totalfunding, prev_url=prev_url, next_url=next_url)

    



@bp.route('/edit_cohort/<id>', methods = ['GET','POST'])
@login_required
def edit_cohort(id):
    cohort = Cohort.query.filter_by(id=id).first_or_404()
    form = EditCohortForm(cohort.id)
    if form.validate_on_submit():
        cohort = Cohort(
            coh_desc = form.coh_desc.data,
            coh_clubid = form.coh_club.data,
            coh_prisonid = form.coh_prison.data,
            coh_startDate = form.coh_startDate.data,
            coh_endDate = form.coh_endDate.data,
            coh_deliveryDate = form.coh_delDate.data if form.coh_delDate != "" else None,
            coh_tpi = form.coh_tpi.data
        )
      
        db.session.commit()
        flash('Your changes have been saved')
        return redirect(url_for('main.cohort', id=id))
    elif request.method == 'GET':
        form.coh_desc.data = cohort.coh_desc
        form.coh_club.data = cohort.clb_cohort.name
        form.coh_prison.data = cohort.prs_cohort.prs_name
        form.coh_startDate.data = cohort.coh_startDate
        form.coh_endDate.data = cohort.coh_endDate
        form.coh_delDate.data = cohort.coh_deliveryDate
        form.coh_tpi.data = cohort.coh_tpi
    return render_template('edit_cohort.html', title = 'Edit Cohort', form=form)


@bp.route('/media')
def media():
    page = request.args.get('page', 1, type=int)
    media = Media.query.order_by(Media.med_date.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for(
        'main.media', page=media.next_num) if media.has_next else None
    prev_url = url_for(
        'main.media', page=media.prev_num) if media.has_prev else None
    return render_template('media.html', title='Media', media=media.items, next_url=next_url, prev_url=prev_url)

@bp.route('/funding')
@login_required
def funding():
    page = request.args.get('page', 1, type=int)
    funds = Funding.query.order_by(Funding.fnd_date.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for(
        'main.funding', page=funds.next_num) if funds.has_next else None
    prev_url = url_for(
        'main.funding', page=funds.prev_num) if funds.has_prev else None
    return render_template('funding.html', title='Funding', funds=funds.items, next_url=next_url, prev_url=prev_url)


@bp.route('/admin')
@login_required
def admin():
    return render_template('admin.html', title = 'Admin')


@bp.route('/newclub', methods = ['GET', 'POST'])
@login_required
def newclub():
    form = NewClubForm()
    if form.validate_on_submit():
        division = form.club_division.data
        club = Club(name=form.clubname.data, town=form.club_town.data, division_id=division.id)
        db.session.add(club)
        db.session.commit()
        flash('You have successfully added ' + club.name)
        return redirect(url_for('main.clubs'))
    page = request.args.get('page', 1, type=int)
    clubs = Club.query.order_by(Club.name.asc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for(
        'main.clubs', page=clubs.next_num) if clubs.has_next else None
    prev_url = url_for(
        'main.clubs', page=clubs.prev_num) if clubs.has_prev else None
    return render_template('club.html', title = 'Add Club', clubs = clubs.items, next_url = next_url, prev_url = prev_url, form=form)


@bp.route('/newdivision', methods = ['GET', 'POST'])
def newdivision():
    form = NewDivisionForm()
    if form.validate_on_submit():
        div = Division(div_desc=form.division.data)
        db.session.add(div)
        db.session.commit()
        flash('You have successfully added a new Division')
        return redirect(url_for('main.admin'))
    return render_template('admin.html', title='Add Division', form=form)

@bp.route('/newcontact', methods = ['GET','POST'])
@login_required
def newcontact():
    form = NewContactForm()
    if form.validate_on_submit():
        club = form.con_club.data
        contact = Contact(
            con_firstname = form.con_firstname.data,
            con_surname = form.con_surname.data,
            con_email = form.con_email.data,
            con_phone = form.con_phone.data,
            con_club = club.id
            )
        db.session.add(contact)
        db.session.commit()
        flash('You have successfully added ' + contact.con_firstname)
        return redirect(url_for('main.contacts'))
    page = request.args.get('page', 1, type=int)
    contacts = Contact.query.join(Club).order_by(Club.name.asc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for(
        'main.contacts', page=contacts.next_num) if contacts.has_next else None
    prev_url = url_for(
        'main.contacts', page=contacts.prev_num) if contacts.has_prev else None
    return render_template('contact.html', title = 'Add a Contact', contacts= contacts.items, prev_url=prev_url, next_url=next_url, form = form)

@bp.route('/newcategory', methods = ['GET', 'POST'])
@login_required
def newcategory():
    form = NewCategoryForm()
    if form.validate_on_submit():
        cat = Category(
            cat_shortcode= form.cat_shortcode.data,
            cat_desc=form.cat_desc.data
            )
        db.session.add(cat)
        db.session.commit()
        flash('You have successfully add the Category ' + cat.cat_desc)
        return redirect(url_for('main.admin'))
    return render_template('admin.html', title = 'Add Category', form = form)

@bp.route('/newprison', methods = ['GET','POST'])
@login_required
def newprison():
    form = NewPrisonForm()
    if form.validate_on_submit():
        cat = form.prs_cat.data
        prs = Prison(
            prs_name = form.prs_name.data,
            prs_town = form.prs_town.data,
            prs_category =cat.id
        )
        db.session.add(prs)
        db.session.commit()
        flash('You have successfully add HMP ' + prs.prs_name)
        return redirect(url_for('main.prisons'))
    page = request.args.get('page', 1, type=int)
    prisons = Prison.query.join(Category).order_by(Prison.prs_name.asc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for(
        'main.prisons', page=prisons.next_num) if prisons.has_next else None
    prev_url = url_for(
        'main.prisons', page=prisons.prev_num) if prisons.has_prev else None
    return render_template('prison.html', title='Add Prison', prisons=prisons.items, next_url=next_url, prev_url=prev_url, form=form)


@bp.route('/newcohort', methods = ['GET','POST'])
@login_required
def newcohort():
    form = NewCohortForm()
    if form.validate_on_submit():
        club = form.coh_club.data
        prison = form.coh_prison.data
        cohort =  Cohort(
            coh_desc = form.coh_desc.data,
            coh_clubid = club.id,
            coh_prisonid = prison.id,
            coh_startDate = form.coh_startDate.data,
            coh_endDate = form.coh_endDate.data,
            coh_deliveryDate = form.coh_delDate.data,
            coh_tpi = False
        )
        db.session.add(cohort)
        db.session.commit()
        flash('You have successfully created the cohort')
        return redirect(url_for('main.cohorts'))
    page = request.args.get('page', 1, type=int)
    cohorts = Cohort.query.order_by(Cohort.coh_startDate.asc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for(
        'main.cohorts', page=cohorts.next_num) if cohorts.has_next else None
    prev_url = url_for(
        'main.cohorts', page=cohorts.prev_num) if cohorts.has_prev else None
    return render_template('cohort.html', title = 'Create a Cohort', cohorts=cohorts.items, prev_url=prev_url, next_url=next_url, form=form)

@bp.route('/newcomment/<source>/<sourceid>', methods = ['GET', 'POST'])
@login_required
def newcomment(source, sourceid):
    form = NewCommentForm()
    user = current_user
    if form.validate_on_submit():
        comment = Comment(
            body = form.body.data,
            timestamp = datetime.utcnow(),
            user_id = user.id,
            cohort_id = sourceid if source == 'cohort' else None,
            fnd_id=sourceid if source == 'funding' else None,
            med_id=sourceid if source == 'media' else None
        )
        db.session.add(comment)
        db.session.commit()
        flash('New comment added!')
        return redirect(url_for('main.'+source , id = sourceid))
    """ page = request.args.get('page', 1, type = int)
    comments = Comment.query.filter_by(cohort_id = sourceid).order_by(Comment.timestamp.desc()).paginate(
        page, current_app.config['COMMENTS_PER_PAGE'], False)
    next_url = url_for('main.cohort', id = sourceid, page = comments.next_num) if comments.has_next else None
    prev_url = url_for ('main.cohort', id = sourceid, page = comments.prev_num) if comments.has_prev else None """

    return render_template('testform.html', title = 'Cohort Details', form=form)


@bp.route('/newmedia', methods = ['GET','POST'])
@login_required
def newmedia():
    form = NewMediaForm()
    if form.validate_on_submit():
        club = form.med_clubid.data
        prison = form.med_prisonid.data
        media = Media(
            med_clubid = club.id,
            med_prisonid=prison.id,
            med_date = form.med_date.data,
            med_medium = form.med_medium.data,
            med_publication = form.med_publication.data,
            med_link = form.med_link.data,
            med_author = form.med_author.data
        )
        db.session.add(media)
        db.session.commit()
        flash('New media added')
        return redirect(url_for('main.media'))
    page = request.args.get('page', 1, type=int)
    media = Media.query.order_by(Media.med_date.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for(
        'main.media', page=media.next_num) if media.has_next else None
    prev_url = url_for(
        'main.media', page=media.prev_num) if media.has_prev else None
    return render_template('media.html', title='Media', media=media.items, next_url=next_url, prev_url=prev_url, form=form)


@bp.route('/newfunding/<cohortid>', methods = ['GET', 'POST'])
@login_required
def newfunding(cohortid):
    form = NewFundingForm()
    if form.validate_on_submit():
        funding=Funding(
            fnd_cohort = cohortid,
            fnd_date = form.fnd_date.data,
            fnd_amount = form.fnd_amount.data
        )
        db.session.add(funding)
        db.session.commit()
        flash('New funding assigned')
        return redirect(url_for('main.funding'))
    page = request.args.get('page', 1, type=int)
    funds = Funding.query.order_by(Funding.fnd_date.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for(
        'main.funding', page=funds.next_num) if funds.has_next else None
    prev_url = url_for(
        'main.funding', page=funds.prev_num) if funds.has_prev else None
    return render_template('funding.html', title='Funding', funds=funds.items, next_url=next_url, prev_url=prev_url, form=form)
