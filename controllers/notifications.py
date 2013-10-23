# coding: utf8
# try something like
from gluon import current

def max_limit_reached():
    if not current.config.getboolean("Email","daily_notification"):
        return
    max_reviews = current.config.getint("Email","max_reviews")
    for user in db(db.auth_user).select(db.auth_user.ALL):
        query = db((db.to_review.tr_reviewer_id==user.id)&(db.to_review.tr_reviewed==None))
        if query.count() > max_reviews:
            send_mail(user, query.select())
    return
            
def send_mail(user,reviews_to_do):
    msg = response.render("email_template_max_limit_reached.html",
                          dict(name=user.first_name,
                              link=A(B("ToDo page"),_href=URL('reviews','todo',host=True)),
                              reviews_to_do=SQLTABLE(reviews_to_do,headers={'to_review.tr_changelist':"Changelist",'to_review.tr_added':"Added"}, columns=['to_review.tr_changelist','to_review.tr_added'])
                              ))
    return mail.send(to=[user.email],
        subject='Limit of reviews to do reached',
        message=msg)
