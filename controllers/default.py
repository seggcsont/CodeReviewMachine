# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simple replace the two lines below with:
    return auth.wiki()
    """
    response.title=" "
    response.subtitle="Changelists"
    reviews_from_db = db(db.to_review).select(orderby=~db.to_review.tr_changelist)
    if request.vars.rows:
        reviews_from_db = reviews_from_db[:int(request.vars.rows)]
    
    rows = [TR(
                TH('Changelist'),
                TH('Reporter'),
                TH('Added'),
                TH('Reviewer'),
                TH('Reviewed'))
            ]
    for review in reviews_from_db:
        rows.append(TR(
                        TD(review.tr_changelist),
                        TD(get_user_display_name(review.tr_reporter_id)),
                        TD(review.tr_added),
                        TD(get_user_display_name(review.tr_reviewer_id)),
                        TD(review.tr_reviewed)
                        ))
    reviews = TABLE(*rows,_class='table table-condensed table-striped')
    return dict(reviews=reviews)

def get_user_display_name(user_id):
    user = db(db.auth_user.id==user_id).select().first()
    return "%s %s" % (user.first_name, user.last_name) if user else 'Unknown'
    
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
