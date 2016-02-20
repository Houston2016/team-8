import tornado.web
import requests
import json
import time
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
        (r'^/api/v1/users/([0-9]?)$', UserHandler),
        (r'^/api/v1/admin/([0-9]?)$', AdminHandler),
        ]
        settings = dict(
            cookie_secret="super secret!"
        )
        tornado.web.Application.__init__(self, handlers, **settings)
        # Have one global connection.
        self.db = scoped_session(sessionmaker(bind=engine))


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user_id = self.get_secure_cookie("user")
        if not user_id: return None
        return self.db.query(User).get(user_id)

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


        else:
            print("Error")
            print(self.request.arguments) 
                   


    def delete(self, _id):
        print("Deleted " , _id)
        self.db.query(User).filter_by(id=int(_id)).delete()


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
        print("Post to /user")
        if form.validate():
            data = {}
            for keys in self.request.arguments:
                data[keys] = self.request.arguments[keys][0].decode("utf-8") 
            print(data)    
            user = User(**data)
            self.db.add(user)
            self.db.commit()
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
            user = self.db.query(Admin).filter_by(id=int(_id))
            admin = Admin(**data)
            self.db.add(Admin)
            self.db.commit()
        else:
            print("Error")
            print(self.request.arguments)



    def delete(self, _id):
        print("Deleted " , _id)
        self.db.query(Admin).filter_by(id=int(_id)).delete()
        

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('templates/index.html')





if __name__ == "__main__":
    app = Application()
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()