# coding: utf8
# try something like
from utils import *

@auth.requires_login()
def todo():
    response.title='Reviews to do'
    forms = []
    
    to_do_reviews = db((db.to_review.tr_reviewer_id==auth.user_id)&(db.to_review.tr_reviewed==None)).select(orderby=~db.to_review.tr_changelist)
    table_content = [DIV(
        DIV('Changelist',_class='table-cell'),
        DIV('Reporter',_class='table-cell'),
        DIV('Added',_class='table-cell'),
        DIV('Comment',_class='table-cell'),
        _class='table-header table-row')]
    for review in to_do_reviews:
        form = SQLFORM.factory(Field('comment','string', requires=IS_NOT_EMPTY()),
                table_name=str(review.tr_changelist),
                formstyle='divs',
                labels={'comment':''})
        table_content.append(DIV(
            DIV(review.tr_changelist,_class='table-cell'),
            DIV(get_user_display_name(review.tr_reporter_id),_class='table-cell'),
            DIV(review.tr_added,_class='table-cell'),
            DIV(form,_class='table-cell'),
            _class='table-row'))
        forms.append((review.tr_changelist,form))
    
    for (id,form) in forms:
        if form.process().accepted:
            db(db.to_review.tr_changelist==id).update(tr_comment=form.vars.comment,tr_reviewed=request.now)
            session.flash="Comment saved"
            redirect(URL())

    return dict(table=DIV(*table_content,_class='table'))

@auth.requires_login()
def done(): 
    response.title='Reviews done'
    done_reviews = db((db.to_review.tr_reviewer_id==auth.user_id)&~(db.to_review.tr_reviewed==None)).select(orderby=~db.to_review.tr_changelist)
    table_content = [DIV(
        DIV('Changelist',_class='table-cell'),
        DIV('Reporter',_class='table-cell'),
        DIV('Added',_class='table-cell'),
        DIV('Reviewed',_class='table-cell'),
        DIV('Comment',_class='table-cell'),
        _class='table-header table-row')]
    
    for review in done_reviews:
        table_content.append(DIV(
            DIV(review.tr_changelist,_class='table-cell'),
            DIV(get_user_display_name(review.tr_reporter_id),_class='table-cell'),
            DIV(review.tr_added,_class='table-cell'),
            DIV(review.tr_reviewed,_class='table-cell'),
            DIV(review.tr_comment,_class='table-cell'),
            _class='table-row'))
    return dict(table=DIV(*table_content,_class='table'))

@auth.requires_login()
def reported(): 
    response.title='Reviews reported'
    done_reviews = db(db.to_review.tr_reporter_id==auth.user_id).select(orderby=~db.to_review.tr_changelist)
    table_content = [DIV(
        DIV('Changelist',_class='table-cell'),
        DIV('Reviewer',_class='table-cell'),
        DIV('Added',_class='table-cell'),
        DIV('Reviewed',_class='table-cell'),
        DIV('Comment',_class='table-cell'),
        _class='table-header table-row')]
    
    for review in done_reviews:
        table_content.append(DIV(
            DIV(review.tr_changelist,_class='table-cell'),
            DIV(get_user_display_name(review.tr_reviewer_id),_class='table-cell'),
            DIV(review.tr_added,_class='table-cell'),
            DIV(review.tr_reviewed,_class='table-cell'),
            DIV(review.tr_comment,_class='table-cell'),
            _class='table-row'))
    return dict(table=DIV(*table_content,_class='table'))
    
def get_user_display_name(user_id):
    user = db(db.auth_user.id==user_id).select().first()
    return "%s %s" % (user.first_name, user.last_name) if user else 'Unknown'
