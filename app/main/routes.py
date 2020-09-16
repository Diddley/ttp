from datetime import datetime, date
from flask import render_template, flash, redirect, url_for, jsonify, current_app, request
from flask_login import current_user, login_required
from app import db, images
from app.main.forms import NewClubForm, NewDivisionForm, NewContactForm, NewCategoryForm, NewPrisonForm, NewCohortForm, EditCohortForm, NewCommentForm, TPIForm, NewMediaForm, NewFundingForm, NewKitForm, NewProbServiceForm
from app.models import User, Club, Division, Contact, Category, Prison, Cohort, Comment, Media, Funding, Kit, Probation
from app.main import bp

@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()

@bp.route('/', methods = ['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    totalfunding = 0
    funding = Funding.query.all()
    for fund in funding:
        totalfunding += float(fund.fnd_amount)
    numclubs = Club.query.count()
    numprisons = Prison.query.count()
    numcohorts = Cohort.query.count()
    numprobs = Probation.query.count()
    people = Cohort.query.all()
    participants = 0
    graduates = 0
    for p in people:
        participants += int(p.coh_participants)
        if p.coh_grads:
                graduates += int(p.coh_grads)
    
    kit = Kit.query.all()
    tot_small = 0
    tot_medium = 0
    tot_large = 0
    tot_xlarge = 0
    for k in kit:
        if k.kit_numSmall:
            tot_small += k.kit_numSmall
        if k.kit_numMedium:
            tot_medium += k.kit_numMedium
        if k.kit_numLarge:
            tot_large += k.kit_numLarge
        if k.kit_numXlarge:
            tot_xlarge += k.kit_numXlarge
    tot_kit = tot_small+tot_large+tot_medium+tot_xlarge
    today = datetime.utcnow()
    page = request.args.get('page', 1, type=int)
    cohorts = Cohort.query.filter(Cohort.coh_startDate<=today, or_(Cohort.coh_endDate>today, Cohort.coh_endDate==None)).order_by(Cohort.coh_startDate.asc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.index', page=cohorts.next_num) if cohorts.has_next else None
    prev_url = url_for('main.index', page = cohorts.prev_num) if cohorts.has_prev else None
    return render_template('index.html', title = 'Home', today = today, cohorts=cohorts.items, numclubs=numclubs, numprisons=numprisons, numprobs=numprobs,
        numcohorts = numcohorts, participants = participants, graduates = graduates, totalfunding=totalfunding, tot_kit=tot_kit, tot_small=tot_small,
        tot_medium=tot_medium, tot_large = tot_large, tot_xlarge=tot_xlarge, next_url = next_url, prev_url=prev_url)


@bp.route('/clubs')
def clubs():
    page = request.args.get('page',1, type=int)
    clubs = Club.query.order_by(Club.clb_name.asc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False)   
    next_url = url_for('main.clubs', page = clubs.next_num) if clubs.has_next else None
    prev_url = url_for('main.clubs', page = clubs.prev_num) if clubs.has_prev else None
    #for club in clubs:
    #    flash(club.id)
    #    flash(club.clb_name)
    #contact = Contact.query.filter_by(con_club=clubs.items[0].id).all()
    #flash(contact[0].con_firstname)
    #contacts = Contact.query.filter_by(Contact.con_club is not None).all()
    #flash(contacts[0])
    return render_template('club.html', title = 'Clubs', clubs = clubs.items, next_url = next_url, prev_url = prev_url)


@bp.route('/club/<id>')
@login_required
def club(id):
    club = Club.query.filter_by(id=id).first_or_404()
    contacts = Contact.query.filter_by(con_club=id).all()
    cohorts = Cohort.query.filter_by(coh_clubid=id).all()

    page = request.args.get('page', 1, type=int)
    comments = club.clb_comment.order_by(Comment.timestamp.desc()).paginate(
        page, current_app.config['COMMENTS_PER_PAGE'], False)
    next_url = url_for('main.club', id=id, page = comments.next_num) if comments.has_next else None 
    prev_url = url_for('main.club', id=id, page = comments.prev_num) if comments.has_prev else None
    return render_template('clubdetails.html', title = club.clb_name, club = club, id=id, contacts=contacts, cohorts=cohorts, comments=comments.items,
         next_url=next_url, prev_url=prev_url)


@bp.route('/contacts')
def contacts():
    page = request.args.get('page', 1, type=int)
    contacts = Contact.query.order_by(Contact.con_surname.asc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for(
        'main.contacts', page=contacts.next_num) if contacts.has_next else None
    prev_url = url_for(
        'main.contacts', page=contacts.prev_num) if contacts.has_prev else None
    #flash(type(contacts))
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

@bp.route('/probservices')
def probservices():
    page = request.args.get('page', 1, type=int)
    probservices = Probation.query.order_by(Probation.prob_name.asc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for(
        'main.probservices', page=probservices.next_num) if probservices.has_next else None
    prev_url = url_for(
        'main.probservices', page=probservices.prev_num) if probservices.has_prev else None
    return render_template('probservice.html', title='Probation Services', probservices=probservices.items, next_url=next_url, prev_url=prev_url)


@bp.route('/cohort/<id>')
@login_required
def cohort(id):
    cohort = Cohort.query.filter_by(id=id).first_or_404()
    funding = Funding.query.filter_by(fnd_cohort=id).order_by(Funding.fnd_date.desc()).all()
    totalfunding = 0
    for fund in funding:
        totalfunding+=float(fund.fnd_amount)
    kit = Kit.query.filter_by(kit_cohortid=id).all()
    tot_small = 0
    tot_medium = 0
    tot_large = 0
    tot_xlarge = 0
    for k in kit:
        if k.kit_numSmall:
            tot_small += k.kit_numSmall
        if k.kit_numMedium:
            tot_medium += k.kit_numMedium
        if k.kit_numLarge:
            tot_large += k.kit_numLarge
        if k.kit_numXlarge:
            tot_xlarge += k.kit_numXlarge
    tot_kit = tot_small+tot_large+tot_medium+tot_xlarge
    page = request.args.get('page', 1, type=int)
    comments = cohort.coh_comment.order_by(Comment.timestamp.desc()).paginate(
        page, current_app.config['COMMENTS_PER_PAGE'], False)
    next_url = url_for('main.cohort', id=id, page = comments.next_num) if comments.has_next else None 
    prev_url = url_for('main.cohort', id=id, page = comments.prev_num) if comments.has_prev else None
    return render_template('cohortdetails.html', cohort=cohort, comments=comments.items, id=id, totalfunding=totalfunding, funding=funding,
    tot_kit=tot_kit, tot_small=tot_small, tot_medium=tot_medium, tot_large=tot_large, tot_xlarge=tot_xlarge, prev_url=prev_url, next_url=next_url)

    



@bp.route('/edit_cohort/<id>', methods = ['GET','POST'])
@login_required
def edit_cohort(id):
    cohort = Cohort.query.filter_by(id=id).first_or_404()
    form = EditCohortForm(cohort.id)
    if form.validate_on_submit():
        club = form.coh_club.data
        prison = form.coh_prison.data
        probservice = form.coh_probserv.data
        course = form.coh_course.data
        cohort = Cohort(
            coh_desc=form.coh_desc.data,
            coh_clubid=club.id,
            coh_prisonid=prison.id if prison else None,
            coh_probid=probservice.id if probservice else None,
            coh_startDate=form.coh_startDate.data,
            coh_endDate=form.coh_endDate.data,
            coh_course=course.id,
            coh_participants=form.coh_participants.data,
            coh_grads=form.coh_grads.data,
            coh_tpi=False
        )
      
        db.session.commit()
        flash('Your changes have been saved')
        return redirect(url_for('main.cohort', id=id))
    elif request.method == 'GET':
        form.coh_desc.data = cohort.coh_desc
        flash(cohort.coh_desc)
        form.coh_club.data = cohort.coh_clubid
        flash(cohort.clb_cohort.clb_name)
        if cohort.coh_prisonid: 
            form.coh_prison.data = cohort.coh_prisonid 
            flash(cohort.prs_cohort.prs_name)
        if cohort.coh_probid:
            form.coh_probserv.data = cohort.coh_probid 
            flash(cohort.prob_cohort.prob_name)
        form.coh_startDate.data = cohort.coh_startDate
        flash(cohort.coh_startDate)
        form.coh_endDate.data = cohort.coh_endDate
        flash(cohort.coh_endDate)
        form.coh_course.data = cohort.coh_course
        flash(cohort.course_owner.course_type)
        form.coh_participants.data = cohort.coh_participants
        flash(cohort.coh_participants)
        if cohort.coh_grads:
            form.coh_grads.data = cohort.coh_grads
            flash(cohort.coh_grads)
        form.coh_tpi.data = cohort.coh_tpi
        flash(cohort.coh_tpi)
    return render_template('form.html', title = 'Edit Cohort', cohort=cohort, form=form)

@bp.route('/toggletpi/<id>', methods = ['GET', 'POST'])
@login_required
def toggletpi(id):
    cohort = Cohort.query.filter_by(id=id).first_or_404()
    current_tpi = cohort.coh_tpi
    if current_tpi:
        new_tpi = False;
    else:
        new_tpi = True;
    
    cohort.coh_tpi = new_tpi
    
    db.session.commit()
    return redirect(url_for('main.cohort', id=id))
    

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
        filename = images.save(request.files['club_badge'])
        url = images.url(filename)
        club = Club(
            clb_name=form.clubname.data, 
            clb_town=form.club_town.data, 
            clb_postcode=form.club_postcode.data,
            division_id=division.id,
            clb_contract=form.club_contract.data,
            clb_collab=form.club_collab.data,
            clb_fundingapp=form.club_fundingapp.data,
            clb_badge=url
            )
        db.session.add(club)
        db.session.commit()
        flash('You have successfully added ' + club.clb_name)
        return redirect(url_for('main.clubs'))
    # page = request.args.get('page', 1, type=int)
    # clubs = Club.query.order_by(Club.clb_name.asc()).paginate(
    #     page, current_app.config['POSTS_PER_PAGE'], False)
    # next_url = url_for(
    #     'main.clubs', page=clubs.next_num) if clubs.has_next else None
    # prev_url = url_for(
    #     'main.clubs', page=clubs.prev_num) if clubs.has_prev else None
    return render_template('form.html', title = 'Add Club', form=form)


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
        prison = form.con_prs.data
        probservice = form.con_prob.data
        contact = Contact(
            con_firstname = form.con_firstname.data,
            con_surname = form.con_surname.data,
            con_email = form.con_email.data,
            con_phone = form.con_phone.data,
            con_club = club.id if club else None,
            con_prison = prison.id if prison else None,
            con_probation = probservice.id if probservice else None
            )
        db.session.add(contact)
        db.session.commit()
        flash('You have successfully added ' + contact.con_firstname)
        return redirect(url_for('main.contacts'))
    # page = request.args.get('page', 1, type=int)
    # contacts = Contact.query.join(Club).order_by(Club.clb_name.asc()).paginate(
    #     page, current_app.config['POSTS_PER_PAGE'], False)
    # next_url = url_for(
    #     'main.contacts', page=contacts.next_num) if contacts.has_next else None
    # prev_url = url_for(
    #     'main.contacts', page=contacts.prev_num) if contacts.has_prev else None
    return render_template('form.html', title = 'Add a Contact', form = form)

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
    # page = request.args.get('page', 1, type=int)
    # prisons = Prison.query.join(Category).order_by(Prison.prs_name.asc()).paginate(
    #     page, current_app.config['POSTS_PER_PAGE'], False)
    # next_url = url_for(
    #     'main.prisons', page=prisons.next_num) if prisons.has_next else None
    # prev_url = url_for(
    #     'main.prisons', page=prisons.prev_num) if prisons.has_prev else None
    return render_template('form.html', title='Add Prison', form=form)

@bp.route('/newprobservice', methods=['GET', 'POST'])
@login_required
def newprobservice():
    form = NewProbServiceForm()
    if form.validate_on_submit():
        prob = Probation(
            prob_name = form.prob_name.data,
            prob_town = form.prob_town.data,
            prob_postcode = form.prob_postcode.data
        )
        db.session.add(prob)
        db.session.commit()
        flash('You have successfully added ' + prob.prob_name + ' Probation Service.')
        return redirect(url_for('main.probservices'))
    return render_template('form.html', title='Add a Probation Service', form=form)



@bp.route('/newcohort', methods = ['GET','POST'])
@login_required
def newcohort():
    form = NewCohortForm()
    if form.validate_on_submit():
        club = form.coh_club.data
        prison = form.coh_prison.data
        probservice = form.coh_prob.data
        course = form.coh_course.data
        cohort =  Cohort(
            coh_desc = form.coh_desc.data,
            coh_clubid = club.id,
            coh_prisonid = prison.id if prison else None,
            coh_probid = probservice.id if probservice else None,
            coh_startDate = form.coh_startDate.data,
            coh_endDate = form.coh_endDate.data,
            coh_course = course.id,
            coh_participants = form.coh_parts.data,
            coh_tpi = False
        )
        db.session.add(cohort)
        db.session.commit()
        flash('You have successfully created the cohort')
        return redirect(url_for('main.cohorts'))
    #page = request.args.get('page', 1, type=int)
    #cohorts = Cohort.query.order_by(Cohort.coh_startDate.asc()).paginate(
    #    page, current_app.config['POSTS_PER_PAGE'], False)
    #next_url = url_for(
    #    'main.cohorts', page=cohorts.next_num) if cohorts.has_next else None
    #prev_url = url_for(
    #    'main.cohorts', page=cohorts.prev_num) if cohorts.has_prev else None
    return render_template('form.html', title = 'Create a Cohort', form=form)
    #return render_template('cohort.html', title = 'Create a Cohort', cohorts=cohorts.items, prev_url=prev_url, next_url=next_url, form=form)

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
            med_id=sourceid if source == 'media' else None,
            prob_id = sourceid if source == 'probation' else None
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
        probservice = form.med_probid.data
        media = Media(
            med_clubid = club.id,
            med_prisonid=prison.id if prison else None,
            med_probid = probservice.id if probservice else None,
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
    return render_template('form.html', title='Media', media=media.items, form=form)


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
    #page = request.args.get('page', 1, type=int)
    #funds = Funding.query.order_by(Funding.fnd_date.desc()).paginate(
    #    page, current_app.config['POSTS_PER_PAGE'], False)
    #next_url = url_for(
    #    'main.funding', page=funds.next_num) if funds.has_next else None
    #prev_url = url_for(
    #   'main.funding', page=funds.prev_num) if funds.has_prev else None
    return render_template('form.html', title='Funding', form=form)

@bp.route('/newkit/<cohortid>', methods = ['GET', 'POST'])
@login_required
def newkit(cohortid):
    form = NewKitForm()
    if form.validate_on_submit():
        kit = Kit(
            kit_cohortid = cohortid,
            kit_numSmall = form.kit_small.data,
            kit_numMedium = form.kit_medium.data,
            kit_numLarge = form.kit_large.data,
            kit_date =form.kit_date.data
        )
        db.session.add(kit)
        db.session.commit()
        flash('New kit assigned')
        return redirect(url_for('main.cohort', id = cohortid))
    return render_template('form.html',title = "Kit", form = form)

@bp.route('/map')
def map():
    return render_template('map.html', title='Map')
