from flask_pymongo import PyMongo
from  src.schema import validate_psw
mongo=PyMongo()

def init_app(app):
    mongo.init_app(app)

def register_user(username, password):
    res=validate_psw(password)
    user=mongo.db.users.find_one({
        'username': username,       
    })
    if(res and user==None):
        mongo.db.users.insert_one({
            'username': username,
            'password':  password
        })
        return True
    else:
        return False
    
def find_user(username, password):
    user=mongo.db.users.find_one({
        'username': username,
        'password':  password
    })
    
    if(user):
        return True
    else:
        return False