'''
Created on Jul 31, 2013

@author: Laszlo_Tarcsanyi
'''
import random
from gluon import current

class ReviewAssigner(object):
    def __init__(self, db, user_id):
        reset(db)
        
    def get_next_user(self, db, user_id):
        if len(self.users) < 2: return
        while 1:
            if self.index >= len(self.users):
                reset(db)
            if self.users[self.index]!=user_id:
                self.index += 1
                return self.users[self.index]
            self.index += 1
        #if self.users[self.index-1]==user_id:
        #   return get_next_user(self, db, user_id)
        #return self.users[self.index-1]
        
    def reset(db):
        self.index=0
        self.users=db((db.auth_user.id==db.auth_membership.user_id)&(db.auth_membership.group_id==15)).select(db.auth_user.ALL)
        #self.users=db(db.auth_user).select(db.auth_user.ALL)
ra=None
def get_next_user(db,user_id):
    global ra
    if not ra:
        ra = ReviewAssigner(db, user_id)
    return ra.get_next_user(db, user_id)