from datetime import datetime, date, timedelta
from flask import render_template, flash, redirect, url_for, jsonify, current_app, request
from flask_login import current_user, login_required
from app import db, images
from app.main.forms import NewClubForm, NewDivisionForm, NewContactForm, NewCategoryForm, NewPrisonForm, NewCohortForm, EditCohortForm, NewCommentForm, TPIForm, NewMediaForm, NewFundingForm, NewKitForm, NewProbServiceForm, NewStockItemForm, EditContactForm, DeleteForm, EditClubForm, EditPrisonForm, EditProbationForm, NewLinkForm, CommentForm
from app.models import User, Club, Division, Contact, Category, Prison, Cohort, Comment, Media, Funding, Kit, Probation, Stock, Course, Task
from app.main import bp


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()


@bp.route('/', methods=['GET', 'POST'])
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
    cohorts = Cohort.query.filter(Cohort.coh_startDate <= today, Cohort.coh_endDate == None).order_by(
        Cohort.coh_startDate.asc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for(
        'main.index', page=cohorts.next_num) if cohorts.has_next else None
    prev_url = url_for(
        'main.index', page=cohorts.prev_num) if cohorts.has_prev else None
    return render_template('index.html', title='Home', today=today, cohorts=cohorts.items, numclubs=numclubs, numprisons=numprisons, numprobs=numprobs,
                           numcohorts=numcohorts, participants=participants, graduates=graduates, totalfunding=totalfunding, tot_kit=tot_kit, tot_small=tot_small,
                           tot_medium=tot_medium, tot_large=tot_large, tot_xlarge=tot_xlarge, next_url=next_url, prev_url=prev_url)


@bp.route('/clubs')
def clubs():
    #page = request.args.get('page', 1, type=int)
    clubs = Club.query.order_by(Club.clb_name.asc()).all()
    # paginate(
    #    page, current_app.config['POSTS_PER_PAGE'], False)
    # next_url = url_for(
    #    'main.clubs', page=clubs.next_num) if clubs.has_next else None
    # prev_url = url_for(
    #    'main.clubs', page=clubs.prev_num) if clubs.has_prev else None
    # for club in clubs:
    #    flash(club.id)
    #    flash(club.clb_name)
    #contact = Contact.query.filter_by(con_club=clubs.items[0].id).all()
    # flash(contact[0].con_firstname)
    #contacts = Contact.query.filter_by(Contact.con_club is not None).all()
    # flash(contacts[0])
    return render_template('club.html', title='Clubs', clubs=clubs)


@bp.route('/club/<id>')
@login_required
def club(id):
    club = Club.query.filter_by(id=id).first_or_404()
    prisons = club.clb_linked_prs.order_by(Prison.prs_name.asc())
    probs = club.clb_linked_prob.order_by(Probation.prob_name.asc())
    contacts = Contact.query.filter_by(con_club=id).all()
    cohorts = Cohort.query.filter_by(coh_clubid=id).all()

    page = request.args.get('page', 1, type=int)
    comments = club.clb_comment.order_by(Comment.timestamp.desc()).all()
    return render_template('clubdetails.html', title=club.clb_name, club=club, id=id, contacts=contacts, cohorts=cohorts,
                           prisons=prisons, probs=probs, comments=comments)


@bp.route('/editclub/<id>', methods=['GET', 'POST'])
@login_required
def editclub(id):
    club = Club.query.filter_by(id=id).first_or_404()
    form = EditClubForm(id=id)
    if form.validate_on_submit():
        try:
            url = images.url(
                images.save(request.files['club_badge']))
        except:
            url = ""
        if url != "":
            club.clb_badge = url
        club.clb_name = form.clubname.data
        club.clb_town = form.club_town.data
        club.clb_postcode = form.club_postcode.data
        club.division_id = form.club_division.data.id
        club.clb_contract = form.club_contract.data
        club.clb_collab = form.club_collab.data
        club.clb_fundingapp = form.club_fundingapp.data
        db.session.add(club)
        db.session.commit()
        flash('You have successfully updated ' + club.clb_name)
        return redirect(url_for('main.club', id=club.id))
    form.clubname.data = club.clb_name
    form.club_town.data = club.clb_town
    form.club_postcode.data = club.clb_postcode
    form.club_division.data = Division.query.filter_by(
        id=club.division_id).first_or_404()
    form.club_contract.data = club.clb_contract
    form.club_collab.data = club.clb_collab
    form.club_fundingapp.data = club.clb_fundingapp
    return render_template('clubform.html', title="Edit Club Details", form=form, club=club)


@bp.route('/contacts')
def contacts():
    contacts = Contact.query.order_by(Contact.con_surname.asc()).all()
    # flash(type(contacts))
    return render_template('contact.html', title='Contacts', contacts=contacts)


@bp.route('/contact/<id>')
@login_required
def contact(id):
    contact = Contact.query.filter_by(id=id).first_or_404()
    return render_template('contactdetails.html', title=contact.con_firstname + ' ' + contact.con_surname, contact=contact)


@bp.route('/clubcontacts/<id>')
@login_required
def clubcontacts(id):
    club = Club.query.filter_by(id=id).first_or_404()
    contacts = Contact.query.filter_by(con_club=id).all()
    return render_template('contact.html', title=club.clb_name + ' Contacts', contacts=contacts)


@bp.route('/prisoncontacts/<id>')
@login_required
def prisoncontacts(id):
    prison = Prison.query.filter_by(id=id).first_or_404()
    contacts = Contact.query.filter_by(con_prison=id).all()
    return render_template('contact.html', title=prison.prs_name + ' Contacts', contacts=contacts)


@bp.route('/probservcontacts/<id>')
@login_required
def probservcontacts(id):
    ps = Probation.query.filter_by(id=id).first_or_404()
    contacts = Contact.query.filter_by(con_probation=id).all()
    return render_template('contact.html', title=ps.prob_name + ' Contacts', contacts=contacts)


@bp.route('/editcontact/<id>', methods=['GET', 'POST'])
@login_required
def editcontact(id):
    contact = Contact.query.filter_by(id=id).first_or_404()
    form = EditContactForm(id=id)
    if form.validate_on_submit():
        contact.con_firstname = form.con_firstname.data
        contact.con_surname = form.con_surname.data
        contact.con_email = form.con_email.data
        contact.con_phone = form.con_phone.data
        db.session.add(contact)
        db.session.commit()
        flash('You have successfully edited ' + contact.con_firstname)
        return redirect(url_for('main.contacts'))
    form.con_firstname.data = contact.con_firstname
    form.con_surname.data = contact.con_surname
    form.con_email.data = contact.con_email
    form.email2.data = contact.con_email
    form.con_phone.data = contact.con_phone
    return render_template('form.html', form=form, contact=contact)


@bp.route('/deletecontact/<id>', methods=['GET', 'POST'])
@login_required
def deletecontact(id):
    contact = Contact.query.filter_by(id=id).first_or_404()
    form = DeleteForm(id=id)
    if form.validate_on_submit():
        db.session.delete(contact)
        db.session.commit()
        flash('Contact Deleted')
        return redirect(url_for('main.contacts'))
    return render_template('form.html', title='Delete Contact: {} {} ?'.format(contact.con_firstname, contact.con_surname), contact=contact, form=form)


@bp.route('/prisons')
def prisons():
    page = request.args.get('page', 1, type=int)
    prisons = Prison.query.join(Category).order_by(Prison.prs_name.asc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for(
        'main.prisons', page=prisons.next_num) if prisons.has_next else None
    prev_url = url_for(
        'main.prisons', page=prisons.prev_num) if prisons.has_prev else None
    return render_template('prison.html', title='Prisons', prisons=prisons.items, next_url=next_url, prev_url=prev_url)


@bp.route('/prison/<id>')
@login_required
def prison(id):
    prison = Prison.query.filter_by(id=id).first_or_404()
    clubs = prison.prs_linked_clb.order_by(Club.clb_name.asc())
    contacts = Contact.query.filter_by(con_prison=id).all()
    cohorts = Cohort.query.filter_by(coh_prisonid=id).all()

    comments = prison.prs_comment.order_by(Comment.timestamp.desc()).all()
    return render_template('prisondetails.html', title=prison.prs_name, prison=prison, contacts=contacts, cohorts=cohorts, clubs=clubs, comments=comments)


@bp.route('/editprison/<id>', methods=['GET', 'POST'])
@login_required
def editprison(id):
    prison = Prison.query.filter_by(id=id).first_or_404()
    form = EditPrisonForm(id=id)
    if form.validate_on_submit():
        prison.prs_name = form.prs_name.data
        prison.prs_town = form.prs_town.data
        prison.prs_postcode = form.prs_postcode.data
        prison.prs_category = form.prs_cat.data.id
        db.session.add(prison)
        db.session.commit()
        flash('You have successfully updated ' + prison.prs_name)
        return redirect(url_for('main.prison', id=prison.id))
    form.prs_name.data = prison.prs_name
    form.prs_town.data = prison.prs_town
    form.prs_postcode.data = prison.prs_postcode
    form.prs_cat.data = Category.query.filter_by(
        id=prison.prs_category).first_or_404()
    return render_template('form.html', title="Edit Prison Details", form=form, prison=prison)


@bp.route('/cohorts')
def cohorts():
    page = request.args.get('page', 1, type=int)
    cohorts = Cohort.query.order_by(Cohort.coh_startDate.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for(
        'main.cohorts', page=cohorts.next_num) if cohorts.has_next else None
    prev_url = url_for(
        'main.cohorts', page=cohorts.prev_num) if cohorts.has_prev else None
    return render_template('cohort.html', title='Cohorts', cohorts=cohorts.items, next_url=next_url, prev_url=prev_url)


@bp.route('/probservices')
def probservices():

    probservices = Probation.query.order_by(Probation.prob_name.asc())

    return render_template('probservice.html', title='Probation Services', probservices=probservices)


@bp.route('/probservice/<id>')
@login_required
def probservice(id):
    probservice = Probation.query.filter_by(id=id).first_or_404()
    clubs = probservice.prob_linked_clb.order_by(Club.clb_name.asc())
    contacts = Contact.query.filter_by(con_probation=id).all()
    cohorts = Cohort.query.filter_by(coh_probid=id).all()

    comments = probservice.prob_comment.order_by(
        Comment.timestamp.desc()).all()
    return render_template('probservicedetails.html', title=probservice.prob_name, probservice=probservice, contacts=contacts, cohorts=cohorts, clubs=clubs, comments=comments)


@bp.route('/link', methods=['GET', 'POST'])
@login_required
def createlink():

    form = NewLinkForm()
    if form.validate_on_submit():
        club = form.lnk_club.data
        prison = form.lnk_prs.data
        probservice = form.lnk_prob.data

        if prison != None:
            club.clb_linked_prs.append(prison)

        if probservice != None:
            club.clb_linked_prob.append(probservice)

        db.session.add(club)
        db.session.commit()

        db.session.add(club)
        flash('New link created')
        return redirect(url_for('main.club', id=club.id))
    x = request.referrer.rsplit('/')
    entity = x[-2]
    id = int(x[-1])
    if entity == 'club':
        form.lnk_club.data = Club.query.filter_by(
            id=id).first_or_404()
    return render_template('form.html', title="Link Page", form=form)


@bp.route('/editprobservice/<id>', methods=['GET', 'POST'])
@login_required
def editprobservice(id):
    probservice = Probation.query.filter_by(id=id).first_or_404()
    form = EditProbationForm(id=id)
    if form.validate_on_submit():
        probservice.prob_name = form.prob_name.data
        probservice.prob_town = form.prob_town.data
        probservice.prob_postcode = form.prob_postcode.data
        db.session.add(probservice)
        db.session.commit()
        flash('You have successfully updated ' + probservice.prob_name)
        return redirect(url_for('main.probationservice', id=probservice.id))
    form.prob_name.data = probservice.prob_name
    form.prob_town.data = probservice.prob_town
    form.prob_postcode.data = probservice.prob_postcode
    return render_template('form.html', title="Edit Probation Service Details", form=form, probservice=probservice)


@bp.route('/cohort/<id>')
@login_required
def cohort(id):
    cohort = Cohort.query.filter_by(id=id).first_or_404()
    funding = Funding.query.filter_by(
        fnd_cohort=id).order_by(Funding.fnd_date.desc()).all()
    totalfunding = 0
    for fund in funding:
        totalfunding += float(fund.fnd_amount)
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
    next_url = url_for('main.cohort', id=id,
                       page=comments.next_num) if comments.has_next else None
    prev_url = url_for('main.cohort', id=id,
                       page=comments.prev_num) if comments.has_prev else None
    return render_template('cohortdetails.html', cohort=cohort, comments=comments.items, id=id, totalfunding=totalfunding, funding=funding,
                           tot_kit=tot_kit, tot_small=tot_small, tot_medium=tot_medium, tot_large=tot_large, tot_xlarge=tot_xlarge, prev_url=prev_url, next_url=next_url)


@bp.route('/edit_cohort/<id>', methods=['GET', 'POST'])
@login_required
def edit_cohort(id):
    cohort = Cohort.query.filter_by(id=id).first_or_404()
    form = EditCohortForm(id=id)
    if form.validate_on_submit():
        cohort.coh_desc = form.coh_desc.data
        club = form.coh_club.data
        cohort.coh_clubid = club.id
        prison = form.coh_prison.data
        cohort.coh_prisonid = prison.id if prison else None
        probservice = form.coh_probserv.data
        cohort.coh_probid = probservice.id if probservice else None
        cohort.coh_startDate = form.coh_startDate.data
        cohort.coh_endDate = form.coh_endDate.data
        course = form.coh_course.data
        cohort.coh_course = course.id
        cohort.coh_participants = form.coh_participants.data
        cohort.coh_grads = form.coh_grads.data
        db.session.add(cohort)
        db.session.commit()
        flash('Your changes have been saved')
        return redirect(url_for('main.cohort', id=id))
    elif request.method == 'GET':
        form.coh_desc.data = cohort.coh_desc
        form.coh_club.data = Club.query.filter_by(
            id=cohort.coh_clubid).first_or_404()
        if cohort.coh_prisonid:
            form.coh_prison.data = Prison.query.filter_by(
                id=cohort.coh_prisonid).first_or_404()
        if cohort.coh_probid:
            form.coh_probserv.data = Probation.query.filter_by(
                id=cohort.coh_probid).first_or_404()
        form.coh_startDate.data = cohort.coh_startDate
        form.coh_endDate.data = cohort.coh_endDate
        form.coh_course.data = Course.query.filter_by(
            id=cohort.coh_course).first_or_404()
        form.coh_participants.data = cohort.coh_participants
        if cohort.coh_grads:
            form.coh_grads.data = cohort.coh_grads
    return render_template('form.html', title='Edit Cohort', cohort=cohort, form=form)


@bp.route('/toggletpi/<id>', methods=['GET', 'POST'])
@login_required
def toggletpi(id):
    cohort = Cohort.query.filter_by(id=id).first_or_404()
    current_tpi = cohort.coh_tpi
    if current_tpi:
        new_tpi = False
    else:
        new_tpi = True

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
    return render_template('admin.html', title='Admin')


@bp.route('/newclub', methods=['GET', 'POST'])
@login_required
def newclub():
    form = NewClubForm()
    if form.validate_on_submit():
        division = form.club_division.data
        try:
            filename = images.save(request.files['club_badge'])
        except:
            filename = "no_badge.png"
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
    return render_template('form.html', title='Add Club', form=form)


@bp.route('/newdivision', methods=['GET', 'POST'])
def newdivision():
    form = NewDivisionForm()
    if form.validate_on_submit():
        div = Division(div_desc=form.division.data)
        db.session.add(div)
        db.session.commit()
        flash('You have successfully added a new Division')
        return redirect(url_for('main.admin'))
    return render_template('admin.html', title='Add Division', form=form)


@bp.route('/newcontact', methods=['GET', 'POST'])
@login_required
def newcontact():
    form = NewContactForm()
    if form.validate_on_submit():
        club = form.con_club.data
        prison = form.con_prs.data
        probservice = form.con_prob.data
        contact = Contact(
            con_firstname=form.con_firstname.data,
            con_surname=form.con_surname.data,
            con_email=form.con_email.data,
            con_phone=form.con_phone.data,
            con_club=club.id if club else None,
            con_prison=prison.id if prison else None,
            con_probation=probservice.id if probservice else None
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
    return render_template('form.html', title='Add a Contact', form=form)


@bp.route('/newcategory', methods=['GET', 'POST'])
@login_required
def newcategory():
    form = NewCategoryForm()
    if form.validate_on_submit():
        cat = Category(
            cat_shortcode=form.cat_shortcode.data,
            cat_desc=form.cat_desc.data
        )
        db.session.add(cat)
        db.session.commit()
        flash('You have successfully add the Category ' + cat.cat_desc)
        return redirect(url_for('main.admin'))
    return render_template('admin.html', title='Add Category', form=form)


@bp.route('/newprison', methods=['GET', 'POST'])
@login_required
def newprison():
    form = NewPrisonForm()
    if form.validate_on_submit():
        cat = form.prs_cat.data
        prs = Prison(
            prs_name=form.prs_name.data,
            prs_town=form.prs_town.data,
            prs_category=cat.id
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
            prob_name=form.prob_name.data,
            prob_town=form.prob_town.data,
            prob_postcode=form.prob_postcode.data
        )
        db.session.add(prob)
        db.session.commit()
        flash('You have successfully added ' +
              prob.prob_name + ' Probation Service.')
        return redirect(url_for('main.probservices'))
    return render_template('form.html', title='Add a Probation Service', form=form)


@bp.route('/newcohort', methods=['GET', 'POST'])
@login_required
def newcohort():
    form = NewCohortForm()
    if form.validate_on_submit():
        club = form.coh_club.data
        prison = form.coh_prison.data
        probservice = form.coh_prob.data
        course = form.coh_course.data
        cohort = Cohort(
            coh_desc=form.coh_desc.data,
            coh_clubid=club.id,
            coh_prisonid=prison.id if prison else None,
            coh_probid=probservice.id if probservice else None,
            coh_startDate=form.coh_startDate.data,
            coh_endDate=form.coh_endDate.data,
            coh_course=course.id,
            coh_participants=form.coh_parts.data,
            coh_tpi=False
        )
        db.session.add(cohort)
        db.session.commit()
        flash('You have successfully created the cohort')
        return redirect(url_for('main.cohorts'))
    #page = request.args.get('page', 1, type=int)
    # cohorts = Cohort.query.order_by(Cohort.coh_startDate.asc()).paginate(
    #    page, current_app.config['POSTS_PER_PAGE'], False)
    # next_url = url_for(
    #    'main.cohorts', page=cohorts.next_num) if cohorts.has_next else None
    # prev_url = url_for(
    #    'main.cohorts', page=cohorts.prev_num) if cohorts.has_prev else None
    return render_template('form.html', title='Create a Cohort', form=form)
    # return render_template('cohort.html', title = 'Create a Cohort', cohorts=cohorts.items, prev_url=prev_url, next_url=next_url, form=form)


# @bp.route('/newcomment/<source>/<sourceid>', methods=['GET', 'POST'])
# @login_required
# def newcomment(source, sourceid):
#     form = NewCommentForm()
#     user = current_user
#     if form.validate_on_submit():
#         comment = Comment(
#             body=form.body.data,
#             timestamp=datetime.utcnow(),
#             user_id=user.id,
#             club_id=sourceid if source == 'club' else None,
#             cohort_id=sourceid if source == 'cohort' else None,
#             fnd_id=sourceid if source == 'funding' else None,
#             med_id=sourceid if source == 'media' else None,
#             prob_id=sourceid if source == 'probation' else None
#         )
#         db.session.add(comment)
#         db.session.commit()
#         flash('New comment added!')
#         return redirect(url_for('main.'+source, id=sourceid))
#     """ page = request.args.get('page', 1, type = int)
#     comments = Comment.query.filter_by(cohort_id = sourceid).order_by(Comment.timestamp.desc()).paginate(
#         page, current_app.config['COMMENTS_PER_PAGE'], False)
#     next_url = url_for('main.cohort', id = sourceid, page = comments.next_num) if comments.has_next else None
#     prev_url = url_for ('main.cohort', id = sourceid, page = comments.prev_num) if comments.has_prev else None """

#     return render_template('testform.html', title='Cohort Details', form=form)


@bp.route('/newcomment/<source>/<sourceid>', methods=['GET', 'POST'])
@login_required
def newcomment(source, sourceid):
    form = CommentForm(id=sourceid, source=source)
    user = current_user
    if form.validate_on_submit():
        cm_club = form.com_club.data
        cm_prs = form.com_prs.data
        cm_prob = form.com_prob.data

        comment = Comment(
            body=form.body.data,
            timestamp=datetime.utcnow(),
            user_id=user.id,
            club_id=cm_club.id if cm_club else None,
            cohort_id=sourceid if source == 'cohort' else None,
            fnd_id=sourceid if source == 'funding' else None,
            med_id=sourceid if source == 'media' else None,
            prob_id=cm_prob.id if cm_prob else None,
            prs_id=cm_prs.id if cm_prs else None
        )
        db.session.add(comment)
        db.session.commit()
        if form.com_date.data != None:
            task = Task(
                tk_comment=comment.id,
                tk_duedate=form.com_date.data,
                tk_notify=False
            )
            db.session.add(task)
            db.session.commit()
            msg = 'New task added'
        else:
            msg = 'New comment added'

        flash(msg)
        if source == 'blank':
            return redirect(url_for('main.tasks'))
        else:
            return redirect(url_for('main.'+source, id=sourceid))
    if source == 'club':
        club = Club.query.filter_by(id=sourceid).first_or_404()
        form.com_club.data = club
    if source == 'prison':
        prison = Prison.query.filter_by(id=sourceid).first_or_404()
        form.com_prs.data = prison
    if source == 'probservices':
        prob = Probation.query.filter_by(id=sourceid).first_or_404()
        form.com_prob.data = prob

    return render_template('testform.html', title='Cohort Details', form=form)


@bp.route('/newmedia', methods=['GET', 'POST'])
@login_required
def newmedia():
    form = NewMediaForm()
    if form.validate_on_submit():
        club = form.med_clubid.data
        prison = form.med_prisonid.data
        probservice = form.med_probid.data
        media = Media(
            med_clubid=club.id,
            med_prisonid=prison.id if prison else None,
            med_probid=probservice.id if probservice else None,
            med_date=form.med_date.data,
            med_medium=form.med_medium.data,
            med_publication=form.med_publication.data,
            med_link=form.med_link.data,
            med_author=form.med_author.data
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


@bp.route('/newfunding/<cohortid>', methods=['GET', 'POST'])
@login_required
def newfunding(cohortid):
    form = NewFundingForm()
    if form.validate_on_submit():
        funding = Funding(
            fnd_cohort=cohortid,
            fnd_date=form.fnd_date.data,
            fnd_amount=form.fnd_amount.data
        )
        db.session.add(funding)
        db.session.commit()
        flash('New funding assigned')
        return redirect(url_for('main.funding'))
    #page = request.args.get('page', 1, type=int)
    # funds = Funding.query.order_by(Funding.fnd_date.desc()).paginate(
    #    page, current_app.config['POSTS_PER_PAGE'], False)
    # next_url = url_for(
    #    'main.funding', page=funds.next_num) if funds.has_next else None
    # prev_url = url_for(
    #   'main.funding', page=funds.prev_num) if funds.has_prev else None
    return render_template('form.html', title='Funding', form=form)


@bp.route('/newkit/<cohortid>', methods=['GET', 'POST'])
@login_required
def newkit(cohortid):
    form = NewKitForm()
    if form.validate_on_submit():
        kit = Kit(
            kit_cohortid=cohortid,
            kit_numSmall=form.kit_small.data,
            kit_numMedium=form.kit_medium.data,
            kit_numLarge=form.kit_large.data,
            kit_date=form.kit_date.data
        )
        db.session.add(kit)
        db.session.commit()
        flash('New kit assigned')
        return redirect(url_for('main.cohort', id=cohortid))
    return render_template('form.html', title="Kit", form=form)


@bp.route('/map')
def map():
    return render_template('map.html', title='Map')


@bp.route('/addstockitem', methods=['GET', 'POST'])
@login_required
def addstockitem():
    form = NewStockItemForm()
    if form.validate_on_submit():
        stock = Stock(
            sku=form.item_sku.data,
            stock_desc=form.item_desc.data,
            qty=form.item_qty.data
        )
        flash(stock)
        db.session.add(stock)
        db.session.commit()
        flash(stock.stock_desc + ' added')
        return redirect(url_for('main.index'))
    return render_template('admin.html', title="Add stock item", form=form)


@bp.route('/stock')
@login_required
def stock():
    stocks = Stock.query.order_by(Stock.qty.asc())
    return render_template('admin.html', title='Stock Levels', stocks=stocks)


@bp.route('/tasks')
@login_required
def tasks():
    num_days = current_app.config['NOTIFICATION_DAYS']
    start = datetime.now() - timedelta(days=1)
    end = start + timedelta(days=num_days)
    now = datetime.today()

    tasks = Task.query.filter(Task.tk_duedate <= end).filter(
        Task.tk_duedate >= start)

    tasklist = []
    for task in tasks:
        taskdict = {}
        taskdict['comment'] = Comment.query.filter_by(
            id=task.tk_comment).first_or_404().body
        taskdict['task_id'] = task.id
        taskdict['date'] = task.tk_duedate.strftime("%Y/%m/%d")
        taskdict['notify'] = task.tk_notify
        tasklist.append(taskdict)

    return render_template('notifications.html', title="Notifications", tasks=tasks, tasklist=tasklist)


@bp.route('/task/<id>', methods=['GET', 'POST'])
@login_required
def task(id):
    task = Task.query.filter_by(id=id).first_or_404()
    if task.tk_notify:
        task.tk_notify = False
    else:
        task.tk_notify = True

    db.session.commit()
    return redirect(url_for('main.tasks'))
