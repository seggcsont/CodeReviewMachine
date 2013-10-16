# coding: utf8
# try something like
#import random
import review_assigner.py

def index(): return dict(message="hello from changelist.py")

@auth.requires_login()
def add():
    form = FORM("Add changelist",
                DIV(INPUT(_name="tr_changelist", requires=IS_MATCH('^\d+$',error_message='Must be a number'))),
                DIV(INPUT(_type="submit", _label='Add')))
    if form.process(onvalidation=is_changelist_uniqeue).accepted:
        assigned_user = get_random_user()
        
        db.to_review.insert(tr_changelist=form.vars.tr_changelist, tr_reporter_id=auth.user_id, tr_reviewer_id=assigned_user)
        session.flash="Changelist %s assigned to %s!" % (str(form.vars.tr_changelist),
                                                                        " ".join([assigned_user.first_name,assigned_user.last_name]))
        if send_mail(assigned_user, form.vars.tr_changelist):
            session.flash = session.flash + " Email sent!"
        redirect(URL('default','index'))
    return dict(form=form)

def is_changelist_uniqeue(form):
    if not db(db.to_review.tr_changelist==form.vars.tr_changelist).isempty():
        form.errors.tr_changelist = 'Changelist has been already added!'

def get_random_user():
    #users = db(db.auth_user.id!=auth.user_id).select(db.auth_user.ALL)
    #return users[random.randint(0,len(users)-1)]
    return review_assigner.get_next_user(db, auth.user_id)
    
def send_mail(user,change_id):
    msg = response.render("email_template_new_change_assigned.html",
                          dict(name=user.first_name,
                              change_id=change_id,
                              link=A(B("ToDo page"),_href=URL('reviews','todo',host=True))
                              ))
    return mail.send(to=[user.email],
        subject='New change',
        message=msg)
