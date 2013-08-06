# coding: utf8
# try something like
def index(): 
    query = db((db.auth_user.id==db.auth_membership.user_id)&(db.auth_membership.group_id==15)).select(db.auth_user.ALL)
    return dict(message=query)
