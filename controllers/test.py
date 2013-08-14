# coding: utf8
# try something like
def index(): 
    a = mail.send(to=['laszlo_tarcsanyi@epam.com'],
        subject='Subject',
        message='Hello world!') 
    #query = db((db.auth_user.id==db.auth_membership.user_id)&(db.auth_membership.group_id==15)).select(db.auth_user.ALL)
    return dict(message="OK" if a else "Error")
