import tornado.web
import requests
import json
import time
import uuid
import tornado.escape
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *  # import the engine to bind
from forms import *
from constants import SimpleMultiDict


class Application(tornado.web.Application):
    def __init__(self):
        create_all()
        handlers = [
        (r"^/", MainHandler),
        (r"^/login", LoginHandler),
        (r'^/api/v1/users/([0-9]?)$', UserHandler),
        (r'^/api/v1/admins/([0-9]?)$', AdminHandler),
        (r'^/api/v1/cards/([0-9]?)$', CardHandler),
        ]
        settings = {
            "cookie_secret": str(uuid.uuid1()),
            "login_url":"/login"
        }
        tornado.web.Application.__init__(self, handlers, **settings)
        # Have one global connection.
        self.db = scoped_session(sessionmaker(bind=engine))


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user_id = self.get_secure_cookie("user")
        if not user_id: return None
        return self.db.query(User).get(int(user_id))

class UserHandler(BaseHandler):
    @property
    def db(self):
        return self.application.db

    def get_current_user(self):
        user_id = self.get_secure_cookie("user")
        if not user_id: return None
        return self.db.query(User).get(user_id)

    def get(self, _id):
        if not _id:
            users = self.db.query(User).all()
            self.write(json.dumps({"users":users}, cls=AlchemyEncoder))

        else:
            user = self.db.query(User).get(int(_id))
            self.write(json.dumps({"user":user}, cls=AlchemyEncoder))

    #make sure you know when to put vs post
    def post(self, _id):
        user = User()
        form = UserForm(SimpleMultiDict(self.request.arguments), user)
        if form.validate():
            print(self.request.arguments)
            data = {}
            for keys in self.request.arguments:
                data[keys] = self.request.arguments[keys][0].decode("utf-8") 
            print(data)  
            user = User(**data)
            self.db.add(user)
            self.db.commit()
            self.write(json.dumps({"status":200}))
        else:
            print("Error")
            print(self.request.arguments) 

    def put(self, _id):
        user = User()
        form = UserForm(SimpleMultiDict(self.request.arguments), user)
        if form.validate():
            print(self.request.arguments)
            data = {}
            for keys in self.request.arguments:
                data[keys] = self.request.arguments[keys][0].decode("utf-8") 
            print(data)    
            self.db.query(User).filter_by(id=int(_id)).delete()
            user = self.db.query(User).filter_by(id=int(_id))
            user = User(**data)
            self.db.add(user)
            self.db.commit()
            self.write(json.dumps({"status":200}))

        else:
            print("Error")
            print(self.request.arguments) 
                   


    def delete(self, _id):
        print("Deleted " , _id)
        self.db.query(User).filter_by(id=int(_id)).delete()
        self.write(json.dumps({"status":200}))

class AdminHandler(BaseHandler):
    @property
    def db(self):
        return self.application.db

    def get(self, _id):
        if not _id:
            admin = self.db.query(Admin).all()
            self.write(json.dumps({"admins":admin}, cls=AlchemyEncoder))

        else:
            admin = self.db.query(Admin).get(int(_id))
            self.write(json.dumps({"admin":admin}, cls=AlchemyEncoder))


    def post(self, _id):
        admin = Admin()
        form = AdminForm(SimpleMultiDict(self.request.arguments), admin)
        if form.validate():
            data = {}
            for keys in self.request.arguments:
                data[keys] = self.request.arguments[keys][0].decode("utf-8")    
            admin = Admin(**data)
            self.db.add(user)
            self.db.commit()
            self.write(json.dumps({"status":200}))
        else:
            print("Error")
            print(self.request.arguments)
    
    def put(self, _id):
        admin = Admin()
        form = AdminForm(SimpleMultiDict(self.request.arguments), admin)
        if form.validate():
            data = {}
            for keys in self.request.arguments:
                data[keys] = self.request.arguments[keys][0].decode("utf-8") 
            print(data)    
            self.db.query(Admin).filter_by(id=int(_id)).delete()
            admin = self.db.query(Admin).filter_by(id=int(_id))
            admin = Admin(**data)
            self.db.add(Admin)
            self.db.commit()
            self.write(json.dumps({"status":200}))
        else:
            print("Error")
            print(self.request.arguments)



    def delete(self, _id):
        print("Deleted " , _id)
        self.db.query(Admin).filter_by(id=int(_id)).delete()
        


class CardHandler(BaseHandler):
    @property
    def db(self):
        return self.application.db

    def get(self, _id):
        if not _id:
            cards = self.db.query(Card).all()
            self.write(json.dumps({"cards":cards}, cls=AlchemyEncoder))
        else:
            card = self.db.query(Card).get(int(_id))
            self.write(json.dumps({"card":card}, cls=AlchemyEncoder))


    def post(self, _id):
        card = Card()
        #form = CardForm(SimpleMultiDict(self.request.arguments), card)
        if True:
            data = {}
            for keys in self.request.arguments:
                data[keys] = self.request.arguments[keys][0].decode("utf-8")    
            card = Card(**data)
            self.db.add(card)
            self.db.commit()
            self.write(json.dumps({"status":200}))

        else:
            print("Error")
            print(self.request.arguments)
    
    def put(self, _id):
        card = Card()
        form = CardForm(SimpleMultiDict(self.request.arguments), card)
        if form.validate():
            data = {}
            for keys in self.request.arguments:
                data[keys] = self.request.arguments[keys][0].decode("utf-8") 
            print(data)    
            self.db.query(Card).filter_by(id=int(_id)).delete()
            card = self.db.query(Card).filter_by(id=int(_id))
            card = Card(**data)
            self.db.add(Card)
            self.db.commit()
        else:
            print("Error")
            print(self.request.arguments)



    def delete(self, _id):
        print("Deleted " , _id)
        self.db.query(Admin).filter_by(id=int(_id)).delete()



class LoginHandler(BaseHandler):
    @property
    def db(self):
        return self.application.db
    def post(self):
        #expects username and password 

        data = {}
        for keys in self.request.arguments:
            data[keys] = self.request.arguments[keys][0].decode("utf-8")   

        if  data.get("username") is None or data.get("password") is None: 
            print("Empty fields")
            self.write(json.dumps({"Error":400, "message":"fields can't be empty"}))


        users = self.db.query(User).all()

        for user in users:
            if user.username.strip() == data.get('username').strip():
                if user.password != data.get("password"):
                    print("password not correct")
                    self.write(json.dumps({"Error":400, 'message':"user password is not correct"}))
                    break
                else:

                    self.set_secure_cookie("user", str(user.id))
                    print("YES")
                    self.write(json.dumps({"status":200}))
                #self.redirect("/")
        if user is None:
            print("No user")
            self.redirect('/signup')




class MainHandler(BaseHandler):
    @property
    def db(self):
        return self.application.db

    @tornado.web.authenticated
    def get(self):
        self.render('templates/index.html')





if __name__ == "__main__":
    app = Application()
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()