from wtforms.form import Form
from wtforms.fields import *
from wtforms import validators

#create some actual validators later 
class UserForm(Form):
    username = StringField(u'username', validators=[validators.input_required()])
    password = StringField(u'password', validators=[validators.input_required()])
    name = StringField(u'name', validators=[validators.input_required()])
    address = StringField(u'address', validators=[validators.input_required()])
    phone = StringField(u'phone', validators=[validators.input_required()])
    email = StringField(u'email', validators=[validators.input_required()])

class CardForm(Form):
    upvotes = IntegerField(u'upvotes',validators=[validators.input_required()])
    downvotes =  IntegerField(u'upvotes',validators=[validators.input_required()])
    totalvotes = IntegerField(u'upvotes',validators=[validators.input_required()])
    title = StringField(u'title', validators=[validators.input_required()])
    description = StringField(u'description', validators=[validators.input_required()])





class AdminForm(Form):
    username = StringField(u'username', validators=[validators.input_required()])
    first_name = StringField(u'first_name', validators=[validators.input_required()])
    last_name = StringField(u'last_name', validators=[validators.input_required()])
    email = StringField(u'email', validators=[validators.input_required()])
    password = StringField(u'password', validators=[validators.input_required()])


class LoginForm(Form):
    username = StringField(u'username', validators=[validators.input_required()])
    password = StringField(u'password', validators=[validators.input_required()])
