# coding: utf8
# try something like
def index():
    users = db(db.auth_user).select()
    result = [TR(TH("User name"),TH("Reported"),TH("Done"),TH("ToDo"))]
    for user in users:
        todo = db((db.to_review.tr_reviewer_id==user.id)&(db.to_review.tr_reviewed==None)).count()
        done = db((db.to_review.tr_reviewer_id==user.id)&(db.to_review.tr_reviewed!=None)).count()
        reported = db(db.to_review.tr_reporter_id==user.id).count()
        result.append(TR(TD(user.first_name," ",user.last_name),TD(reported),TD(done),TD(todo),_class="alert alert-error" if todo > 3 else ""))
    return dict(result=TABLE(result,_class="table"))
