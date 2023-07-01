
from flask import render_template, redirect, request, url_for, flash,abort
from flask_login import login_user,login_required,logout_user,current_user

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired,Email,EqualTo
from wtforms import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
import numpy as np
import numpy_financial as npf
from flowgiston import *
from graphviz import *
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


from flask_login import UserMixin


# Create a login manager object
login_manager = LoginManager()

app = Flask(__name__)

# Often people will also separate these into a separate config.py file
app.config['SECRET_KEY'] = 'mysecretkey'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)

# We can now pass in our app to the login manager
login_manager.init_app(app)

# Tell users what view to go to when they need to login.
login_manager.login_view = "login"


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    Name = StringField('Name', validators=[DataRequired()])
    Mobile_Number=StringField("Mobile Number",validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('pass_confirm', message='Passwords Must Match!')])
    pass_confirm = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register!')

    def check_email(self, field):
        # Check if not None for that user email!
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been registered already!')

    def check_username(self, field):
        # Check if not None for that username!
        if User.query.filter_by(Name=field.data).first():
            raise ValidationError('Sorry, that username is taken!')

# with app.app_context().push()

# with app.app_context().push():
#     db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

with app.app_context():


    class User(db.Model, UserMixin):

        # Create a table in the db
        __tablename__ = 'users'

        id = db.Column(db.Integer, primary_key = True)
        email = db.Column(db.String(64), unique=True, index=True)
        Name = db.Column(db.String(64), unique=True, index=True)
        password_hash = db.Column(db.String(128))
        Mobile_Number=db.Column(db.String(10),unique=True)
        data = db.relationship('Data', backref='user', lazy=True)
        financialparameter = db.relationship('FinancialParameters', backref='user', lazy=True)
        labex = db.relationship('Labex', backref='user', lazy=True)
        labexmisc = db.relationship('LabexMisc', backref='user', lazy=True)
        opex = db.relationship('Opex', backref='user', lazy=True)
        opexmiscs = db.relationship('OpexMisc', backref='user', lazy=True)
        operational_assumption = db.relationship('OperationalAssumptions', backref='user', lazy=True)
        cda= db.relationship('CDA', backref='user', lazy=True)
        storagedata1 = db.relationship('StorageData1', backref='user', lazy=True)
        bur = db.relationship('BUR', backref='user', lazy=True)
        storagedata = db.relationship('StorageData', backref='user', lazy=True)
        capex = db.relationship('capex', backref='user', lazy=True)
        capexmisc = db.relationship('CapexMisc', backref='user', lazy=True)
        pic = db.relationship('PIC', backref='user', lazy=True)
        onetimecost = db.relationship('OneTimeCost', backref='user', lazy=True)
        pd = db.relationship('PD', backref='user', lazy=True)
        ga = db.relationship('GA', backref='user', lazy=True)
        commercial= db.relationship('Commercial', backref='user', lazy=True)

        def __init__(self, email, Name, password,Mobile_Number):
            self.email = email
            self.Name = Name
            self.Mobile_Number=Mobile_Number
            self.password_hash = generate_password_hash(password)

        def check_password(self,password):
            # https://stackoverflow.com/questions/23432478/flask-generate-password-hash-not-constant-output
            return check_password_hash(self.password_hash,password)

    #Creating model table for our CRUD database
    class Data(db.Model):
        __tablename__ = 'datas'
        year = db.Column(db.Integer)
        id = db.Column(db.Integer,primary_key = True)
        Category=db.Column(db.Text)
        ProcessDescription=db.Column(db.Text)
        Successor=db.Column(db.Text)
        Flowtype=db.Column(db.Text)
        UOM=db.Column(db.Text)
        Productivity=db.Column(db.Float)
        Responsibility=db.Column(db.Text)
        Facilitator=db.Column(db.Text)
        SuggestedProductivity=db.Column(db.Float)
        Volume=db.Column(db.Float)
        headcount = db.Column(db.Float)
        user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

        def __init__(self,year, Category, ProcessDescription, Successor, Flowtype, UOM, Productivity,
                    Responsibility, Facilitator, SuggestedProductivity, Volume, headcount):
                    self.year = year
                    self.Category=Category
                    self.ProcessDescription=ProcessDescription
                    self.Successor=Successor
                    self.Flowtype=Flowtype
                    self.UOM=UOM
                    self.Productivity=Productivity
                    self.Responsibility=Responsibility
                    self.Facilitator = Facilitator
                    self.SuggestedProductivity=SuggestedProductivity
                    self.Volume=Volume
                    self.headcount = headcount
                    self.user_id=current_user.id

    class Labex(db.Model):
        __tablename__ = 'labexs'
        id = db.Column(db.Integer, primary_key=True)
        responsibility = db.Column(db.Text)
        manpower_rate_per_month = db.Column(db.Float)
        year = db.Column(db.Integer)
        manpower = db.Column(db.Float)
        total_cost = db.Column(db.Float)
        user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

        def __init__(self,  responsibility, manpower_rate_per_month, year, manpower, total_cost):
            self.responsibility = responsibility
            self.manpower_rate_per_month = manpower_rate_per_month
            self.year = year
            self.manpower = manpower
            self.total_cost = total_cost
            self.user_id=current_user.id

    class LabexMisc(db.Model):
        __tablename__ = 'labexmiscs'
        id = db.Column(db.Integer, primary_key=True)
        responsibility = db.Column(db.Text)
        manpower_rate_per_month = db.Column(db.Float)
        year = db.Column(db.Integer)
        manpower = db.Column(db.Float)
        total_cost = db.Column(db.Float)
        user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

        def __init__(self,  responsibility, manpower_rate_per_month, year, manpower, total_cost):
            self.responsibility = responsibility
            self.manpower_rate_per_month = manpower_rate_per_month
            self.year = year
            self.manpower = manpower
            self.total_cost = total_cost
            self.user_id=current_user.id

    class Opex(db.Model):
        __tablename__ = 'opexs'
        id = db.Column(db.Integer, primary_key=True)
        category = db.Column(db.Text)
        running_costs_description = db.Column(db.Text)
        unit_cost = db.Column(db.Float)
        year = db.Column(db.Integer)
        units = db.Column(db.Float)
        running_cost = db.Column(db.Float)
        user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

        def __init__(self,  category, running_costs_description, unit_cost, year, units, running_cost):
            self.category = category
            self.running_costs_description = running_costs_description
            self.unit_cost = unit_cost
            self.year = year
            self.units = units
            self.running_cost = running_cost
            self.user_id=current_user.id

    class OpexMisc(db.Model):
        __tablename__ = 'opexmiscs'
        id = db.Column(db.Integer, primary_key=True)
        category = db.Column(db.Text)
        running_costs_description = db.Column(db.Text)
        unit_cost = db.Column(db.Float)
        year = db.Column(db.Integer)
        units = db.Column(db.Float)
        running_cost = db.Column(db.Float)
        user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

        def __init__(self,  category, running_costs_description, unit_cost, year, units, running_cost):
            self.category = category
            self.running_costs_description = running_costs_description
            self.unit_cost = unit_cost
            self.year = year
            self.units = units
            self.running_cost = running_cost
            self.user_id=current_user.id

    class OperationalAssumptions(db.Model):
        __tablename__ = 'operationalassumptionss'
        id = db.Column(db.Integer, primary_key=True)
        parameter_description = db.Column(db.Text)
        value = db.Column(db.Float)
        remarks = db.Column(db.Text)
        user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

        def __init__(self,  parameter_description, value, remarks):
            self.parameter_description = parameter_description
            self.value = value
            self.remarks = remarks
            self.user_id=current_user.id

    class CDA(db.Model):
        __tablename__ = 'cdas'
        id = db.Column(db.Integer, primary_key=True)
        Description = db.Column(db.Text)
        UOM = db.Column(db.Text)
        Monthly_Value=db.Column(db.Float)
        year=db.Column(db.Integer)
        user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


        def __init__(self, year, Description, UOM, Monthly_Value):
            self.year = year
            self.Description = Description
            self.UOM = UOM
            self.Monthly_Value = Monthly_Value
            self.user_id=current_user.id

    class StorageData1(db.Model):
        __tablename__ = 'storagedatass'
        id = db.Column(db.Integer, primary_key=True)
        misc_areatype = db.Column(db.Text)
        year = db.Column(db.Integer)
        area = db.Column(db.Float)
        user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

        def __init__(self, misc_areatype, year, area):
                    self.misc_areatype = misc_areatype
                    self.year = year
                    self.area =area
                    self.user_id=current_user.id

    class FinancialParameters(db.Model):
        
        __tablename__ = 'financial_parameters'
        id = db.Column(db.Integer, primary_key=True)
        entity = db.Column(db.Text)
        value = db.Column(db.Float)
        UOM = db.Column(db.Text)
        remarks = db.Column(db.Text)
        user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

        def __init__(self, entity, value, UOM, remarks):
                    self.entity = entity
                    self.value = value
                    self.UOM = UOM
                    self.remarks = remarks
                    self.user_id = current_user.id

    class BUR(db.Model):
        __tablename__ = 'burs'
        id = db.Column(db.Integer, primary_key=True)
        year = db.Column(db.Integer)
        value = db.Column(db.Float)
        user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

        def __init__(self,  year, value):
            self.year = year
            self.value = value
            self.user_id=current_user.id

    class StorageData(db.Model):
        __tablename__ = 'storagedatas'
        id = db.Column(db.Integer, primary_key=True)
        year = db.Column(db.Integer)
        Storage_type = db.Column(db.Text)
        MHE_type = db.Column(db.Text)
        Aisle_width = db.Column(db.Float)
        Clear_bay_width = db.Column(db.Float)
        Upright_width = db.Column(db.Float)
        Pallets_per_face = db.Column(db.Float)
        Upright_depth = db.Column(db.Float)
        Pallet_overhang = db.Column(db.Float)
        Multideep_pallet_spacing = db.Column(db.Float)
        Spacing_between_rack = db.Column(db.Float)
        Storage_depth = db.Column(db.Float)
        No_of_pallet_high = db.Column(db.Float)
        Storage_locations = db.Column(db.Float)
        Space_standard_sqm_per_location = db.Column(db.Float)
        Space_standard_sqft_per_location = db.Column(db.Float)
        cross_aisle = db.Column(db.Float)
        Storage_area_required = db.Column(db.Float)
        user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

        def __init__(self,year,Storage_type,MHE_type,Aisle_width,Clear_bay_width,Upright_width,Pallets_per_face,Upright_depth,
                    Pallet_overhang,Multideep_pallet_spacing,Spacing_between_rack,Storage_depth,No_of_pallet_high,
                    Storage_locations,Space_standard_sqm_per_location,Space_standard_sqft_per_location,cross_aisle,
                    Storage_area_required):
            self.year = year
            self.Storage_type = Storage_type
            self.MHE_type = MHE_type
            self.Aisle_width = Aisle_width
            self.Clear_bay_width = Clear_bay_width
            self.Upright_width = Upright_width
            self.Pallets_per_face = Pallets_per_face
            self.Upright_depth = Upright_depth
            self.Pallet_overhang = Pallet_overhang
            self.Multideep_pallet_spacing = Multideep_pallet_spacing
            self.Spacing_between_rack = Spacing_between_rack
            self.Storage_depth = Storage_depth
            self.No_of_pallet_high = No_of_pallet_high
            self.Storage_locations = Storage_locations
            self.Space_standard_sqm_per_location = Space_standard_sqm_per_location
            self.Space_standard_sqft_per_location = Space_standard_sqft_per_location
            self.cross_aisle = cross_aisle
            self.Storage_area_required = Storage_area_required
            self.user_id=current_user.id

    #Capex table initialization

    class capex(db.Model):
        __tablename__ = 'capexs'
        id = db.Column(db.Integer, primary_key=True)
        category = db.Column(db.Text)
        items = db.Column(db.Text)
        year = db.Column(db.Integer)
        quantity = db.Column(db.Integer)
        uom = db.Column(db.Text)
        unit_cost = db.Column(db.Float)
        depreciation_period = db.Column(db.Float)
        maintenance_rate_per_year = db.Column(db.Float)
        investment_inclusion = db.Column(db.Text)
        total_investment = db.Column(db.Float)
        monthly_emi = db.Column(db.Float)
        monthly_depreciation = db.Column(db.Float)
        monthly_interest = db.Column(db.Float)
        monthly_maintenance_cost = db.Column(db.Float)
        user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

        def __init__(self, category, items, year, quantity, uom, unit_cost, depreciation_period, maintenance_rate_per_year,
                    investment_inclusion, total_investment, monthly_emi, monthly_depreciation, monthly_interest,
                    monthly_maintenance_cost):
            self.category = category
            self.items = items
            self.year = year
            self.quantity = quantity
            self.uom = uom
            self.unit_cost = unit_cost
            self.depreciation_period = depreciation_period
            self.maintenance_rate_per_year = maintenance_rate_per_year
            self.investment_inclusion = investment_inclusion
            self.total_investment = total_investment
            self.monthly_emi = monthly_emi
            self.monthly_depreciation = monthly_depreciation
            self.monthly_interest = monthly_interest
            self.monthly_maintenance_cost = monthly_maintenance_cost
            self.user_id=current_user.id

    class CapexMisc(db.Model):
        __tablename__ = 'capexmiscs'
        id = db.Column(db.Integer, primary_key=True)
        category = db.Column(db.Text)
        items = db.Column(db.Text)
        year = db.Column(db.Integer)
        quantity = db.Column(db.Integer)
        uom = db.Column(db.Text)
        unit_cost = db.Column(db.Float)
        depreciation_period = db.Column(db.Float)
        maintenance_rate_per_year = db.Column(db.Float)
        investment_inclusion = db.Column(db.Text)
        total_investment = db.Column(db.Float)
        monthly_emi = db.Column(db.Float)
        monthly_depreciation = db.Column(db.Float)
        monthly_interest = db.Column(db.Float)
        monthly_maintenance_cost = db.Column(db.Float)
        user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

        def __init__(self,  category, items, year, quantity, uom, unit_cost, depreciation_period, maintenance_rate_per_year,
                    investment_inclusion, total_investment, monthly_emi, monthly_depreciation, monthly_interest, monthly_maintenance_cost):
            self.category = category
            self.items = items
            self.year = year
            self.quantity = quantity
            self.uom = uom
            self.unit_cost = unit_cost
            self.depreciation_period = depreciation_period
            self.maintenance_rate_per_year = maintenance_rate_per_year
            self.investment_inclusion = investment_inclusion
            self.total_investment = total_investment
            self.monthly_emi = monthly_emi
            self.monthly_depreciation = monthly_depreciation
            self.monthly_interest = monthly_interest
            self.monthly_maintenance_cost = monthly_maintenance_cost
            self.user_id=current_user.id

    class PIC(db.Model):
        __tablename__ = 'pics'
        id = db.Column(db.Integer, primary_key=True)
        startup_expense = db.Column(db.Text)
        uom = db.Column(db.Text)
        units = db.Column(db.Float)
        cost_per_unit = db.Column(db.Float)
        percentage_consideration = db.Column(db.Float)
        total_cost = db.Column(db.Float)
        user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

        def __init__(self,  start_up_expemse, uom, units, cost_per_unit, percentage_consideration, total_cost):
            self.startup_expense = start_up_expemse
            self.uom = uom
            self.units = units
            self.cost_per_unit = cost_per_unit
            self.percentage_consideration = percentage_consideration
            self.total_cost = total_cost
            self.user_id=current_user.id

    class OneTimeCost(db.Model):
        __tablename__ = 'onetimecosts'
        id = db.Column(db.Integer, primary_key=True)
        cost_head_description = db.Column(db.Text)
        uom = db.Column(db.Text)
        units = db.Column(db.Float)
        cost_per_unit = db.Column(db.Float)
        percentage_consideration = db.Column(db.Float)
        total_cost = db.Column(db.Float)
        user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

        def __init__(self,  cost_head_description, uom, units, cost_per_unit, percentage_consideration, total_cost):
            self.cost_head_description = cost_head_description
            self.uom = uom
            self.units = units
            self.cost_per_unit = cost_per_unit
            self.percentage_consideration = percentage_consideration
            self.total_cost = total_cost
            self.user_id=current_user.id

    class PD(db.Model):
        __tablename__ = 'pds'
        id = db.Column(db.Integer, primary_key=True)
        date = db.Column(db.Text)
        project_member = db.Column(db.Text)
        due_date = db.Column(db.Text)
        scope = db.Column(db.Text)
        location = db.Column(db.Text)
        tender = db.Column(db.Text)
        op_id = db.Column(db.Text)
        user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

        def __init__(self, date, project_member, due_date, scope, location, tender, op_id):
            self.date = date
            self.project_member = project_member
            self.due_date = due_date
            self.scope = scope
            self.location = location
            self.tender = tender
            self.op_id = op_id
            self.user_id=current_user.id


    class GA(db.Model):
        __tablename__ = 'gas'
        id = db.Column(db.Integer, primary_key=True)
        assumption = db.Column(db.Text)
        user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

        def __init__(self, assumption):
            self.assumption = assumption
            self.user_id=current_user.id

    class Commercial(db.Model):
        __tablename__ = 'commercials'
        id = db.Column(db.Integer, primary_key=True)
        monthly_cost_breakup = db.Column(db.Text)
        overhead = db.Column(db.Float)
        management_fee = db.Column(db.Float)
        year = db.Column(db.Integer)
        total_cost = db.Column(db.Float)
        user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

        def __init__(self, monthly_cost_breakup, overhead, management_fee, year, total_cost):
            self.monthly_cost_breakup = monthly_cost_breakup
            self.overhead = overhead
            self.management_fee = management_fee
            self.year = year
            self.total_cost = total_cost
            self.user_id=current_user.id
    db.create_all()

# with app.app_context():
#     db.create_all()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/welcome')
@login_required
def welcome_user():
    return redirect(url_for("Index"))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You logged out!')
    return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        # Grab the user from our User Models table
        user = User.query.filter_by(email=form.email.data).first()

        # Check that the user was supplied and the password is right
        # The verify_password method comes from the User object
        # https://stackoverflow.com/questions/2209755/python-operation-vs-is-not

        if user.check_password(form.password.data) and user is not None:
            #Log in the user

            login_user(user)
            flash('Logged in successfully.')

            # If a user was trying to visit a page that requires a login
            # flask saves that URL as 'next'.
            next = request.args.get('next')

            # So let's now check if that next exists, otherwise we'll go to
            # the welcome page.
            if next == None or not next[0]=='/':
                next = url_for('welcome_user')

            return redirect(next)
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)

    if form.validate_on_submit():
        user = User(Name=form.Name.data,
                    Mobile_Number=form.Mobile_Number.data,
                    email=form.email.data,password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering! Now you can login!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/SCS')
@login_required
def Index():

    return render_template("index.html")


@app.route('/DataEntry')
@login_required
# def DataEntry():
#     temp = CDA.query.all()
#     uom_list = []
#     for element in temp:
#         if element.UOM not in uom_list:
#             uom_list.append(element.UOM)

#     process=Data.query.all()
#     years = int(FinancialParameters.query.get(5).value)
#     nps = int(len(process) / years)
#     return render_template('data.html',process=process, years = years, nps=nps, uom_list=uom_list)
def DataEntry():
    temp = CDA.query.filter_by(user_id=current_user.id).all()
    uom_list = []
    for element in temp:
        if element.UOM not in uom_list:
            uom_list.append(element.UOM)

    process = Data.query.filter_by(user_id=current_user.id).all()
    years = FinancialParameters.query.get(5)
    if years is None:
        return render_template('error.html', message='Please fill in the value for years first.')
    years = int(years.value)
    nps = int(len(process) / years)
    return render_template('data.html', process=process, years=years, nps=nps, uom_list=uom_list)



#this route is for inserting data to mysql database via html forms
# @app.route('/insert', methods = ['POST'])
# def insert():
#     years = int(FinancialParameters.query.get(5).value)
#     temp1 = db.session.query(CDA.UOM, CDA.year, db.func.sum(CDA.Monthly_Value)).group_by(CDA.UOM, CDA.year).all()
#     if request.method == 'POST':
#         for i in range(years):
#             fluctuation = OperationalAssumptions.query.get(4).value
#             working_hours = OperationalAssumptions.query.get(7).value
#             efficiency = OperationalAssumptions.query.get(3).value
#             days=OperationalAssumptions.query.get(1).value
#             year = i+1
#             Category=request.form['Category']
#             ProcessDescription=request.form['ProcessDescription']
#             Successor=request.form['Sucessor']
#             Flowtype=request.form['Flowtype']
#             UOM=request.form['UOM']
#             Productivity=request.form['Productivity']
#             Responsibility=request.form['Responsibility']
#             Facilitator=request.form['Facilitator']
#             SuggestedProductivity=request.form['SuggestedProductivity']
#             temp = []
#             for element in temp1:
#                 if element[0] == UOM:
#                     temp.append(element)
#             for element in temp:
#                 if element[1] == i+1:
#                     Volume= round((element[2]/days),0)
#             headcount = round((Volume*(1+fluctuation/100)/working_hours/(float(Productivity)*efficiency/100)),2)
#
#             my_data=Data(year,Category, ProcessDescription, Successor, Flowtype, UOM, Productivity,Responsibility, Facilitator, SuggestedProductivity, Volume,headcount)
#             db.session.add(my_data)
#         db.session.commit()
#
#         responsibility_table = db.session.query(Data.Responsibility).group_by(Data.Responsibility).all()
#
#         responsibility_list = []
#         for i in range(len(responsibility_table)):
#             responsibility_list.append(responsibility_table[i][0])
#
#         Labex.query.delete()
#         for j in range(len(responsibility_list)):
#             for i in range(years):
#                 responsibility = responsibility_list[j]
#                 manpower_rate_per_month = None
#                 year = i
#                 manpower = None
#                 total_cost = 0.0
#
#                 my_data = Labex(responsibility, manpower_rate_per_month, year, manpower, total_cost)
#
#                 db.session.add(my_data)
#         db.session.commit()
#
#         flash("Process Inserted Successfully")
#
#         return redirect(url_for('DataEntry'))
#
# #this is our update route where we are going to update our employee
# @app.route('/update', methods = ['GET', 'POST'])
# def update():
#     years = int(FinancialParameters.query.get(5).value)
#     temp1 = db.session.query(CDA.UOM, CDA.year, db.func.sum(CDA.Monthly_Value)).group_by(CDA.UOM, CDA.year).all()
#     print(temp1)
#     if request.method == 'POST':
#         for i in range(years):
#             fluctuation = OperationalAssumptions.query.get(4).value
#             working_hours = OperationalAssumptions.query.get(7).value
#             efficiency = OperationalAssumptions.query.get(3).value
#             days=OperationalAssumptions.query.get(1).value
#             temp = years * int(request.form['id']) + i+1
#             my_data = Data.query.get(temp)
#             my_data.year = i+1
#             my_data.Category=request.form['Category']
#             my_data.ProcessDescription=request.form['ProcessDescription']
#             my_data.Successor=request.form['Sucessor']
#             my_data.Flowtype=request.form['Flowtype']
#             my_data.UOM=request.form['UOM']
#             UOM = request.form['UOM']
#             print(UOM)
#             my_data.Productivity=request.form['Productivity']
#             Productivity = request.form['Productivity']
#             my_data.Responsibility=request.form['Responsibility']
#             my_data.Facilitator=request.form['Facilitator']
#             my_data.SuggestedProductivity=request.form['SuggestedProductivity']
#             temp = []
#             for element in temp1:
#                 if element[0] == UOM:
#                     temp.append(element)
#             for element in temp:
#                 if element[1] == i+1:
#                     Volume = round(element[2]/days,0)
#                     my_data.Volume = round(element[2]/days,0)
#             my_data.headcount = round((Volume*(1+fluctuation/100)/working_hours/(float(Productivity)*efficiency/100)),2)
#
#         db.session.commit()
#         flash("Process Updated Successfully")
#
#         responsibility_table = db.session.query(Data.Responsibility).group_by(Data.Responsibility).all()
#
#         responsibility_list = []
#         for i in range(len(responsibility_table)):
#             responsibility_list.append(responsibility_table[i][0])
#
#         Labex.query.delete()
#         for j in range(len(responsibility_list)):
#             for i in range(years):
#                 responsibility = responsibility_list[j]
#                 manpower_rate_per_month = None
#                 year = i
#                 manpower = None
#                 total_cost = 0.0
#
#                 my_data = Labex(responsibility, manpower_rate_per_month, year, manpower, total_cost)
#
#                 db.session.add(my_data)
#         db.session.commit()
#
#         return redirect(url_for('DataEntry'))

@app.route('/insert', methods = ['POST'])
@login_required
def insert():
    years = FinancialParameters.query.get(5)
    if years is None:
        return render_template('error.html', message='Please fill in the value for years first.')
    years = int(years.value)

    temp1 = db.session.query(CDA.UOM, CDA.year, db.func.sum(CDA.Monthly_Value)).group_by(CDA.UOM, CDA.year).all()

    # years = int(FinancialParameters.query.get(5).value)
    # temp1 = db.session.query(CDA.UOM, CDA.year, db.func.sum(CDA.Monthly_Value)).group_by(CDA.UOM, CDA.year).all()
    if request.method == 'POST':
        for i in range(years):

            # fluctuation = OperationalAssumptions.query.get(4).value
            # working_hours = OperationalAssumptions.query.get(7).value
            # efficiency = OperationalAssumptions.query.get(3).value
            # days=OperationalAssumptions.query.get(1).value
            fluctuation = OperationalAssumptions.query.get(4)
            working_hours = OperationalAssumptions.query.get(7)
            efficiency = OperationalAssumptions.query.get(3)
            days = OperationalAssumptions.query.get(1)

            if fluctuation is None or working_hours is None or efficiency is None or days is None:
                return render_template('error.html', message='Please fill in all the required operational assumptions first.')

            fluctuation = fluctuation.value
            working_hours = working_hours.value
            efficiency = efficiency.value
            days = days.value

            year = i+1
            Category=request.form['Category']
            ProcessDescription=request.form['ProcessDescription']
            Successor=request.form['Sucessor']
            Flowtype=request.form['Flowtype']
            UOM=request.form['UOM']
            Productivity=request.form['Productivity']
            Responsibility=request.form['Responsibility']
            Facilitator=request.form['Facilitator']
            SuggestedProductivity=request.form['SuggestedProductivity']
            temp = []
            for element in temp1:
                if element[0] == UOM:
                    temp.append(element)
            for element in temp:
                if element[1] == i+1:
                    Volume= round((element[2]/days),0)
            headcount = round(
                (Volume * (1 + fluctuation / 100) / working_hours / (float(Productivity) * efficiency / 100)), 2)

            my_data = Data(year, Category, ProcessDescription, Successor, Flowtype, UOM, Productivity, Responsibility,
                           Facilitator, SuggestedProductivity, Volume, headcount)
            db.session.add(my_data)
        db.session.commit()

        responsibility_table = db.session.query(Data.Responsibility).group_by(Data.Responsibility).all()

        temp = db.session.query(Data.Responsibility, Data.year, db.func.sum(Data.headcount)).group_by(Data.year, Data.Responsibility).all()

        responsibility_list = []
        for i in range(len(responsibility_table)):
            responsibility_list.append(responsibility_table[i][0])
        responsibility_list_len = len(responsibility_list)

        Labex.query.delete()
        for j in range(responsibility_list_len):
            for i in range(years):
                responsibility = responsibility_list[j]
                manpower_rate_per_month = None
                year = i
                manpower = temp[responsibility_list_len*i+j][2]
                total_cost = 0.0

                my_data = Labex(responsibility, manpower_rate_per_month, year, manpower, total_cost)

                db.session.add(my_data)
        db.session.commit()

        flash("Process Inserted Successfully")

        return redirect(url_for('DataEntry'))

#this is our update route where we are going to update our employee
@app.route('/update', methods = ['GET', 'POST'])
@login_required
def update():
    # years = int(FinancialParameters.query.get(5).value)
    years = FinancialParameters.query.get(5).value
    if years is None:
        return render_template('error.html', message='Please fill in the value for years first.')
    years = int(years.value)
    temp1 = db.session.query(CDA.UOM, CDA.year, db.func.sum(CDA.Monthly_Value)).group_by(CDA.UOM, CDA.year).all()
    print(temp1)
    if request.method == 'POST':
        for i in range(years):
            # fluctuation = OperationalAssumptions.query.get(4).value
            # working_hours = OperationalAssumptions.query.get(7).value
            # efficiency = OperationalAssumptions.query.get(3).value
            # days=OperationalAssumptions.query.get(1).value
            fluctuation = OperationalAssumptions.query.get(4)
            working_hours = OperationalAssumptions.query.get(7)
            efficiency = OperationalAssumptions.query.get(3)
            days = OperationalAssumptions.query.get(1)

            if fluctuation is None or working_hours is None or efficiency is None or days is None:
                return render_template('error.html', message='Please fill in all the required operational assumptions first.')

            fluctuation = fluctuation.value
            working_hours = working_hours.value
            efficiency = efficiency.value
            days = days.value
            temp = years * int(request.form['id']) + i+1
            my_data = Data.query.get(temp)
            my_data.year = i+1
            my_data.Category=request.form['Category']
            my_data.ProcessDescription=request.form['ProcessDescription']
            my_data.Successor=request.form['Sucessor']
            my_data.Flowtype=request.form['Flowtype']
            my_data.UOM=request.form['UOM']
            UOM = request.form['UOM']
            print(UOM)
            my_data.Productivity=request.form['Productivity']
            Productivity = request.form['Productivity']
            my_data.Responsibility=request.form['Responsibility']
            my_data.Facilitator=request.form['Facilitator']
            my_data.SuggestedProductivity=request.form['SuggestedProductivity']
            temp = []
            for element in temp1:
                if element[0] == UOM:
                    temp.append(element)
            for element in temp:
                if element[1] == i+1:
                    Volume = round(element[2]/days,0)
                    my_data.Volume = round(element[2]/days,0)
            my_data.headcount = round((Volume*(1+fluctuation/100)/working_hours/(float(Productivity)*efficiency/100)),2)

        db.session.commit()
        flash("Process Updated Successfully")

        responsibility_table = db.session.query(Data.Responsibility).group_by(Data.Responsibility).all()
        temp = db.session.query(Data.Responsibility, Data.year, db.func.sum(Data.headcount)).group_by(Data.year, Data.Responsibility).all()

        responsibility_list = []
        for i in range(len(responsibility_table)):
            responsibility_list.append(responsibility_table[i][0])
        responsibility_list_len = len(responsibility_list)

        Labex.query.delete()
        for j in range(responsibility_list_len):
            for i in range(years):
                responsibility = responsibility_list[j]
                manpower_rate_per_month = None
                year = i
                manpower = temp[responsibility_list_len*i+j][2]
                total_cost = 0.0

                my_data = Labex(responsibility, manpower_rate_per_month, year, manpower, total_cost)

                db.session.add(my_data)
        db.session.commit()

        return redirect(url_for('DataEntry'))



#This route is for deleting our employee
@app.route('/delete/<id>/', methods = ['GET', 'POST'])
@login_required
def delete(id):
    # years = int(FinancialParameters.query.get(5).value)
    years = FinancialParameters.query.get(5).value
    if years is None:
        return render_template('error.html', message='Please fill in the value for years first.')
    years = int(years.value)

    for i in range(years):
        my_data = Data.query.get(years*int(id)+i+1)
        db.session.delete(my_data)
    db.session.commit()
    flash("Process Deleted Successfully")

    return redirect(url_for('DataEntry'))


@app.route('/CustomerData')
@login_required
# def CustomerData():
#     years = int(FinancialParameters.query.get(5).value)
#     data = CDA.query.all()
#     ncds = int(len(data)/years)
#     return render_template('Customer_Data_&_Assumptions1.html', years=years, data=data, ncds=ncds)

def CustomerData():
    # financial_param = FinancialParameters.query.get(5)
    years = FinancialParameters.query.get(5)
    if years is None:
        return render_template('error.html', message='Please fill in the value for years first.')
    financial_param = FinancialParameters.query.get(5)
    if financial_param is None:
        return render_template('error.html', message="Please fill the value first.")
    else:
        years = int(financial_param.value)
        data = CDA.query.filter_by(user_id=current_user.id).all()
        ncds = int(len(data) / years)
        return render_template('Customer_Data_&_Assumptions1.html', years=years, data=data, ncds=ncds)


#
# @app.route('/CustomerData')
# def CustomerData():
#
#     years = int(FinancialParameters.query.get(5).value)
#     CustomerData=CustomerDataAndAssumptions.query.all()
#     ncds=int(len(CustomerData)/years)
#     return render_template('Customer_Data_&_Assumptions.html',years=years,CustomerData=CustomerData,ncds=ncds)

@app.route('/CustomerUpdate', methods=['GET', 'POST'])
@login_required
def CustomerUpdate():
    # years = int(FinancialParameters.query.get(5).value)
    years = FinancialParameters.query.get(5)
    if years is None:
        return render_template('error.html', message='Please fill in the value for years first.')
    years = int(years.value)
    if request.method=='POST':
        for i in range(years):
            temp = years * int(request.form['ncd']) + i+1
            my_data = CDA.query.get(temp)
            my_data.year = i+1
            my_data.Description = request.form['Description']
            my_data.UOM = request.form['UOM']
            my_data.Monthly_Value = request.form['Monthly_Value'+str(i)]
        db.session.commit()
        return redirect(url_for('CustomerData'))

@app.route('/CustomerAdd',methods=['GET','POST'])
@login_required
def CustomerAdd():
    # years = int(FinancialParameters.query.get(5).value)
    years = FinancialParameters.query.get(5)
    if years is None:
        return render_template('error.html', message='Please fill in the value for years first.')
    years = int(years.value)
    if request.method == 'POST':
        for i in range(years):
            year = i+1
            Description = request.form['Description']
            UOM = request.form['UOM']
            Monthly_Value = request.form['Monthly_Value'+str(i)]
            my_data = CDA(year, Description, UOM, Monthly_Value)
            db.session.add(my_data)
        db.session.commit()
        return redirect(url_for('CustomerData'))




@app.route('/options')
@login_required
def options():

    return render_template("options.html")


@app.route('/Flowchart')
@login_required
def Flowchart():
    return render_template('error.html', message='this page is not available')
    all_data = Data.query.all()
    process=[]
    Succ=[]
    Flow=[]
    Category=[]
    for i in all_data:
        # q=all_data[i].ProcessDescription
        process.append(i.ProcessDescription)
        Succ.append(i.Successor)
        Flow.append(i.Flowtype)
        Category.append(i.Category)
    print(process)
    print(Succ)
    print(Flow)
    print(Category)
    Process_Description=process
    Sucessor=Succ
    Flowtype=Flow


    b={ 'Category':Category,'Process_Description':process,'Sucessor':Succ,'Flowtype':Flow}
    c=pd.DataFrame(b)
    print(c)
    def Return_Successor(num):
        return str(int(Sucessor[num])-1)

    s=list(range(100000))
    step=[]
    for i in range(100000):
        step.append(str(s[i]))
    Base = flowgiston_base(fillcolor='lightblue')
    class No(Base):
        fillcolor = 'Red'
        label = 'No'
        fontcolor = 'white'
        shape = 'octagon'
    class Note(Base):
        fillcolor = 'lightyellow'
        style = 'filled,bold'
        shape = 'box'
        fontname = 'courier'
    class Page(Base):
        fillcolor = 'lightblue'
        style = 'filled'
        shape = 'ellipse'
        fontname = 'courier'
    chart1 = FlowgistonChart(Base)
    step[0] = chart1.start(Process_Description[0])
    i=1
    while i<=(len(Process_Description)-1)  and  Category[i]=='A':
        if Flowtype[i]=="Decision Point":
                step[i] = step[int(Return_Successor(i))].edge(chart1.if_(Process_Description[i]))
             # step[i] = step[int(Return_Successor(i))].edge(chart.if_(Process_Description[i]))
                i+=1
            # step[i]=step[int(Return_Successor(i))].edge(chart.Note.node(Process_Description[i]))
            # i+=1
            # step[i]=step[int(Return_Successor(i))].edge(chart.No.node(Process_Description[i]))
            # i=i+1


        else:
            step[i] = step[int(Return_Successor(i))].edge(chart1.Note.node(Process_Description[i]))

            i=i+1
    step[i-1].edge(chart1.Page.node("A Complete"))
    chart1

    # chart.save(filename=img1,directory='../static')
    # chart.render(format='jpg', directory=basedir)
    # basedir = os.path.abspath(os.path.dirname(__file__)) +'/static'
    basedir = os.path.abspath(os.path.dirname(__file__))+'/static'
    chart1.render(format='jpg', directory=basedir,filename='flowimage101')
    # session.clear()





    chart2 = FlowgistonChart(Base)
    step[i-1] = chart2.start('A Complete')

    while i<=(len(Process_Description)-1) and Category[i]=='B':

                if Flowtype[i]=="Decision point":
                            step[i] = step[int(Return_Successor(i))].edge(chart2.if_(Process_Description[i]))
                            i+=1


                else:
                    step[i] = step[int(Return_Successor(i))].edge(chart2.Note.node(Process_Description[i]))
                          # print(i)
                    i=i+1

    chart2
    chart2.render(format='jpg', directory=basedir,filename='flowimage202')
    return render_template('flowchart.html')


@app.route('/storage', methods=['GET','POST'])
@login_required
def storage():

    # years = int(FinancialParameters.query.get(5).value)
    years = FinancialParameters.query.get(5)
    if years is None:
        return render_template('error.html', message='Please fill in the value for years first.')
    years = int(years.value)

    inp_list = [('Storage_type', 'Storage Type'), ('MHE_type', 'MHE Type'), ('Aisle_width', 'Aisle width (m) clear'),
                ('Clear_bay_width', 'Clear bay width (m)'), ('Upright_width', 'Upright width (m)'),
                ('Pallets_per_face', 'Pallets/ face (plt)'), ('Upright_depth', 'Upright depth (m)'),
                ('Pallet_overhang', 'Pallet overhang (m)'),
                ('Multideep_pallet_spacing', 'Multi-deep pallet spacing (m)'),
                ('Spacing_between_rack', 'Spacing between rack (m)'), ('Storage_depth', 'Storage depth (plts)'),
                ('No_of_pallet_high', 'No. of pallet high (plts)'), ('Storage_locations', 'Storage Locations'),
                ('cross_aisle', 'Cross Aisle (%)')]

    if request.method == 'POST':

        for i in range(1, years + 1):
            year = i
            Storage_type = request.form[inp_list[0][0] + str(i)]
            MHE_type = request.form[inp_list[1][0] + str(i)]
            Aisle_width = float(request.form[inp_list[2][0] + str(i)])
            Clear_bay_width = float(request.form[inp_list[3][0] + str(i)])
            Upright_width = float(request.form[inp_list[4][0] + str(i)])
            Pallets_per_face = float(request.form[inp_list[5][0] + str(i)])
            Upright_depth = float(request.form[inp_list[6][0] + str(i)])
            Pallet_overhang = float(request.form[inp_list[7][0] + str(i)])
            Multideep_pallet_spacing = float(request.form[inp_list[8][0] + str(i)])
            Spacing_between_rack = float(request.form[inp_list[9][0] + str(i)])
            Storage_depth = float(request.form[inp_list[10][0] + str(i)])
            No_of_pallet_high = float(request.form[inp_list[11][0] + str(i)])
            Storage_locations = float(request.form[inp_list[12][0] + str(i)])
            Space_standard_sqm_per_location = float(((Clear_bay_width + Upright_width) * (0.5 * (Aisle_width + Spacing_between_rack) + (2 * Pallet_overhang + Upright_depth + Multideep_pallet_spacing) * Storage_depth)) / (Storage_depth * No_of_pallet_high * Pallets_per_face))
            Space_standard_sqft_per_location = float(Space_standard_sqm_per_location * 10.76391)
            cross_aisle = float(request.form[inp_list[13][0] + str(i)])
            Storage_area_required = round(Storage_locations * Space_standard_sqft_per_location * (1 + cross_aisle / 100))
            my_data = StorageData(year, Storage_type, MHE_type, Aisle_width, Clear_bay_width, Upright_width,
                                  Pallets_per_face, Upright_depth, Pallet_overhang, Multideep_pallet_spacing, Spacing_between_rack, Storage_depth,
                                  No_of_pallet_high, Storage_locations, Space_standard_sqm_per_location, Space_standard_sqft_per_location,
                                  cross_aisle, Storage_area_required)

            db.session.add(my_data)
            db.session.commit()

            category = "Storage"
            items = Storage_type
            quantity = Storage_locations
            uom = "PP"
            unit_cost = 1
            depreciation_period = 3
            maintenance_rate_per_year = 7
            investment_inclusion = "Yes"
            total_investment = quantity * unit_cost
            monthly_emi = 10
            monthly_depreciation = round(total_investment / (depreciation_period * 12), 1)
            monthly_interest = 12
            monthly_maintenance_cost = 0
            my_data1 = capex(category, items, year, quantity, uom, unit_cost, depreciation_period,
                                 maintenance_rate_per_year, investment_inclusion, total_investment,
                                 monthly_emi, monthly_depreciation, monthly_interest, monthly_maintenance_cost)

            db.session.add(my_data1)
            db.session.commit()

    storage_data = StorageData.query.filter_by(user_id=current_user.id).all()
    storage_data1 = StorageData1.query.filter_by(user_id=current_user.id).all()

    # temp1 = db.session.query(StorageData.year,db.func.sum(StorageData.Storage_area_required)).group_by(StorageData.year).all()
    # temp2 = db.session.query(StorageData1.year, db.func.sum(StorageData1.area)).group_by(StorageData1.year).all()
    temp1 = db.session.query(StorageData.year, db.func.sum(StorageData.Storage_area_required)).filter(StorageData.user_id == current_user.id).group_by(StorageData.year).all()

    temp2 = db.session.query(StorageData1.year, db.func.sum(StorageData1.area)).filter(StorageData1.user_id == current_user.id).group_by(StorageData1.year).all()

    carpet_area = []

    temp1_len = len(temp1)
    temp2_len = len(temp2)
    if (temp1 and temp2):
        for i in range(years):
            if (temp1_len > 0 and temp2_len > 0):
                carpet_area.append(round(temp1[i][1]) + round(temp2[i][1]))
            elif temp1_len > 0:
                carpet_area.append(round(temp1[i][1]))
            elif temp2_len > 0:
                carpet_area.append(round(temp2[i][1]))
            else:
                print()

    bur = BUR.query.filter_by(user_id=current_user.id).all()

    nma = int(len(storage_data1) / years)
    nsts = int(len(storage_data) / years)
    # Rent_per_sqft = FinancialParameters.query.get(16).value
    # Security_Deposit = FinancialParameters.query.get(17).value
    # Annual_rate_onsecuritydeposit = FinancialParameters.query.get(18).value
    Rent_per_sqft = FinancialParameters.query.get(16)
    Security_Deposit = FinancialParameters.query.get(17)
    Annual_rate_onsecuritydeposit = FinancialParameters.query.get(18)

    if Rent_per_sqft is None or Rent_per_sqft.value is None or Security_Deposit is None or Security_Deposit.value is None or Annual_rate_onsecuritydeposit is None or Annual_rate_onsecuritydeposit.value is None:
        return render_template('error.html', message='Please fill in all the required values in FinancialParameters first.')

    Rent_per_sqft = Rent_per_sqft.value
    Security_Deposit = Security_Deposit.value
    Annual_rate_onsecuritydeposit = Annual_rate_onsecuritydeposit.value

    Monthly_Interest_onsecuritydeposit = []
    monthly_rental = []
    if bur:
        for i in range(years):
            monthly_rental.append((carpet_area[i] * (1 + bur[i].value / 100) + 100 - carpet_area[i] * (1 + bur[i].value / 100) % 100)*Rent_per_sqft)

        for i in monthly_rental:
            Monthly_Interest_onsecuritydeposit.append(round(i*Security_Deposit*Annual_rate_onsecuritydeposit/12/100))
    

    des_list = [('Storage_type', 'Storage Type'), ('MHE_type', 'MHE Type'), ('Aisle_width', 'Aisle width (m) clear'),
                ('Clear_bay_width', 'Clear bay width (m)'), ('Upright_width', 'Upright width (m)'),
                ('Pallets_per_face', 'Pallets/ face (plt)'), ('Upright_depth', 'Upright depth (m)'),
                ('Pallet_overhang', 'Pallet overhang (m)'),
                ('Multideep_pallet_spacing', 'Multi-deep pallet spacing (m)'),
                ('Spacing_between_rack', 'Spacing between rack (m)'), ('Storage_depth', 'Storage depth (plts)'),
                ('No_of_pallet_high', 'No. of pallet high (plts)'), ('Storage_locations', 'Storage Locations'),
                ('Space_standard_sqm_per_location','Space Standard (sqm)/location'),
                ('Space_standard_sqft_per_location','Space Standard (sq. ft)/location'),('cross_aisle', 'Cross Aisle (%)'),
                ('Storage_area_required','Storage area required (sqft.)')]

    return render_template('storage.html',monthly_rental=monthly_rental, Monthly_Interest_onsecuritydeposit=Monthly_Interest_onsecuritydeposit, bur=bur,Rent_per_sqft = Rent_per_sqft, Security_Deposit = Security_Deposit, Annual_rate_onsecuritydeposit= Annual_rate_onsecuritydeposit,carpet_area =carpet_area, nsts=nsts,nma=nma, storage_data= storage_data,storage_data1= storage_data1,year=years,des_list=des_list,inp_list=inp_list)


@app.route('/update_storage', methods=['GET', 'POST'])
@login_required
def update_storage():
    years = int(FinancialParameters.query.get(5).value)

    inp_list = [('Storage_type', 'Storage Type'), ('MHE_type', 'MHE Type'), ('Aisle_width', 'Aisle width (m) clear'),
                ('Clear_bay_width', 'Clear bay width (m)'), ('Upright_width', 'Upright width (m)'),
                ('Pallets_per_face', 'Pallets/ face (plt)'), ('Upright_depth', 'Upright depth (m)'),
                ('Pallet_overhang', 'Pallet overhang (m)'),
                ('Multideep_pallet_spacing', 'Multi-deep pallet spacing (m)'),
                ('Spacing_between_rack', 'Spacing between rack (m)'), ('Storage_depth', 'Storage depth (plts)'),
                ('No_of_pallet_high', 'No. of pallet high (plts)'), ('Storage_locations', 'Storage Locations'),
                ('cross_aisle', 'Cross Aisle (%)')]

    if request.method == 'POST':

        for i in range(1, years + 1):
            temp = years * int(request.form['nst']) + i
            my_data = StorageData.query.get(temp)
            year = str(i)
            my_data.Storage_type = request.form[inp_list[0][0] + str(i)]
            my_data.MHE_type = request.form[inp_list[1][0] + str(i)]
            my_data.Aisle_width = float(request.form[inp_list[2][0] + str(i)])
            my_data.Clear_bay_width = float(request.form[inp_list[3][0] + str(i)])
            my_data.Upright_width = float(request.form[inp_list[4][0] + str(i)])
            my_data.Pallets_per_face = float(request.form[inp_list[5][0] + str(i)])
            my_data.Upright_depth = float(request.form[inp_list[6][0] + str(i)])
            my_data.Pallet_overhang = float(request.form[inp_list[7][0] + str(i)])
            my_data.Multideep_pallet_spacing = float(request.form[inp_list[8][0] + str(i)])
            my_data.Spacing_between_rack = float(request.form[inp_list[9][0] + str(i)])
            my_data.Storage_depth = float(request.form[inp_list[10][0] + str(i)])
            my_data.No_of_pallet_high = float(request.form[inp_list[11][0] + str(i)])
            my_data.Storage_locations = float(request.form[inp_list[12][0] + str(i)])
            my_data.Space_standard_sqm_per_location = float(((my_data.Clear_bay_width + my_data.Upright_width) * (
                        0.5 * (my_data.Aisle_width + my_data.Spacing_between_rack) + (
                            2 * my_data.Pallet_overhang + my_data.Upright_depth + my_data.Multideep_pallet_spacing) * my_data.Storage_depth)) / (
                                                                        my_data.Storage_depth * my_data.No_of_pallet_high * my_data.Pallets_per_face))
            my_data.Space_standard_sqft_per_location = float(my_data.Space_standard_sqm_per_location * 10.76391)
            my_data.cross_aisle = float(request.form[inp_list[13][0] + str(i)])
            my_data.Storage_area_required = round(
                my_data.Storage_locations * my_data.Space_standard_sqft_per_location * (1 + my_data.cross_aisle / 100))

            db.session.commit()

            my_data1 = capex.query.get(temp)
            my_data1.category = "Storage"
            my_data1.items = my_data.Storage_type
            my_data1.year = i
            my_data1.quantity = my_data.Storage_locations
            my_data1.uom = "PP"
            my_data1.unit_cost = 1
            my_data1.depreciation_period = 3
            my_data1.maintenance_rate_per_year = 7
            my_data1.investment_inclusion = "Yes"
            my_data1.total_investment = my_data1.quantity * my_data1.unit_cost
            my_data1.monthly_emi = 10
            my_data1.monthly_depreciation = round(my_data1.total_investment / (my_data1.depreciation_period * 12), 1)
            my_data1.monthly_interest = 12

            db.session.commit()
        flash("Process Updated Successfully")

        return redirect(url_for('storage'))


@app.route('/addbur', methods = ['GET', 'POST'])
@login_required
def addbur():
        # years = int(FinancialParameters.query.get(5).value)
        years = FinancialParameters.query.get(5)
        if years is None:
            return render_template('error.html', message='Please fill in the value for years first.')
        years = int(years.value)
        if request.method == 'POST':
            for i in range(1, years + 1):
                year = i
                value = request.form['bur' + str(i-1)]
                my_data = BUR(year, value)
                db.session.add(my_data)
                db.session.commit()
            return redirect(url_for('storage'))

@app.route('/updatebur', methods = ['GET', 'POST'])
@login_required
def updatebur():
    # years = int(FinancialParameters.query.get(5).value)
    years = FinancialParameters.query.get(5)
    if years is None:
        return render_template('error.html', message='Please fill in the value for years first.')
    years = int(years.value)

    if request.method == 'POST':
        temp = BUR.query.filter_by(user_id=current_user.id).all()
        for i in range(years):
            temp[i].value = request.form['bur'+str(i)]
        db.session.commit()
        return redirect(url_for('storage'))

@app.route('/miscareas', methods=['GET','POST'])
@login_required
def miscareas():
    # years=int(FinancialParameters.query.get(5).value)
    years = FinancialParameters.query.get(5)
    if years is None:
        return render_template('error.html', message='Please fill in the value for years first.')
    years = int(years.value)

    if request.method == 'POST':
        for i in range(1,years+1):
            year= i
            misc_areatype= request.form['areatype']
            value = round(float(request.form['value'+str(i)]))
            my_data = StorageData1(misc_areatype,year,value)
            db.session.add(my_data)
            db.session.commit()
        return redirect(url_for('storage'))

# @app.route('/capex', methods=['GET','POST'])
# def capexinput():
#     capex_data = capex.query.all()
#
#     rows = len(capex_data)
#
#     input_list = [('category', 'Category'), ('items', 'Items'), ('quantity', 'Quantity'), ('uom', 'UOM'),
#                   ('unit_cost', 'Unit Cost'), ('depreciation_period', 'Depreciation Period'),
#                   ('maintenance_rate_per_year', 'Maintenance Rate per year (in%)'),
#                   ('investment_inclusion', 'Investment Inclusion')
#                   ]
#
#     output_list = [('category', 'Category'), ('items', 'Items'), ('quantity', 'Quantity'), ('uom', 'UOM'),
#                   ('unit_cost', 'Unit Cost'), ('depreciation_period', 'Depreciation Period'),
#                   ('maintenance_rate_per_year', 'Maintenance Rate per year (in%)'),
#                   ('investment_inclusion', 'Investment Inclusion'), ('total_investment', 'Total Investment'),
#                    ('monthly_emi', 'Monthly Emi'), ('monthly_depreciation', 'Monthly Depreciation'), ('monthly_interest', 'Monthly Interest')
#                    ]
#
#     if request.method == 'POST':
#             category = request.form[input_list[0][0]]
#             items = request.form[input_list[1][0]]
#             quantity = float(request.form[input_list[2][0]])
#             uom = request.form[input_list[3][0]]
#             unit_cost = float(request.form[input_list[4][0]])
#             depreciation_period = float(request.form[input_list[5][0]])
#             maintenance_rate_per_year = float(request.form[input_list[6][0]])
#             investment_inclusion = request.form[input_list[7][0]]
#             total_investment = 9
#             monthly_emi = 10
#             monthly_depreciation = 11
#             monthly_interest = 12
#
#             my_data = capex(category, items, quantity, uom, unit_cost, depreciation_period,
#                                   maintenance_rate_per_year, investment_inclusion, total_investment,
#                                   monthly_emi, monthly_depreciation, monthly_interest)
#
#             db.session.add(my_data)
#             db.session.commit()
#
#     return render_template('capex.html', capex_data=capex_data, input_list = input_list, output_list = output_list, rows=rows)
#

@app.route('/financialparameters')
@login_required
def financialparameters():
    # parameters = FinancialParameters.query.all()
    user_id = current_user.id  # Get the ID of the current logged-in user
    parameters = FinancialParameters.query.filter_by(user_id=current_user.id).all()
    inp_list = [('Minimum EBIT', 'Minimum_EBIT'), ('Allocation Rate', 'Allocation_Rate'),
                ('Discount Rate  (Warehouse Rental + Long Term Liabilities)', 'Discount_Rate'),
                ('Minimum MIRR requirement', 'Minimum_MIRR_requirement'),
                 ('Contract Period', 'Contract_Period'),
                ('Average Days Sales Outstanding (DSO)', 'Average_Days_Sales'),
                ('Average Days Payables Outstanding (DPO)', 'Average_Days_Payables'),
                ('Depreciation Method for Investment', 'Depreciation_Method_for_Investment'),
                ('Investments Annual Interest Rate', 'Annual_Interest_Rate'),
                ('Currency Used in This Model*', 'Currency_Used'),
                ('Exchange rate', 'Exchange_rate'), ('YoY Rental Inflation','YoY_Rental_Inflation'),
                ('YoY Manpower Rate Inflation', 'YoY_Manpower_Rate_Inflation'),
                ('YoY Capex Rate Inflation', 'YoY_Capex_Rate_Inflation'),
                ('YoY OPEX Rate Inflation', 'YoY_OPEX_Rate_Inflation'),
                ('Rent per sqft (builtup)', 'Rent_per_sqft_(builtup)'),
                ('Security Deposit (Months)', 'Security_Deposit_(Months)'),
                ('Annual Interest rate on security deposit (%)', 'Annual_Interest_rate_on_security_deposit_(%)'),
                ('Interest on Working Capital','Interest_on_Working_Capital')]

    return render_template('financialparameter.html', inp_list = inp_list, parameters = parameters)

@app.route('/financialparameters/update',methods=['POST','GET'])
@login_required
def updatefinancialparameters():
    parameters = FinancialParameters.query.filter_by(user_id=current_user.id).all()
    inp_list = [('Minimum EBIT', 'Minimum_EBIT'), ('Allocation Rate', 'Allocation_Rate'),
                ('Discount Rate  (Warehouse Rental + Long Term Liabilities)', 'Discount_Rate'),
                ('Minimum MIRR requirement', 'Minimum_MIRR_requirement'),
                 ('Contract Period', 'Contract_Period'),
                ('Average Days Sales Outstanding (DSO)', 'Average_Days_Sales'),
                ('Average Days Payables Outstanding (DPO)', 'Average_Days_Payables'),
                ('Depreciation Method for Investment', 'Depreciation_Method_for_Investment'),
                ('Investments Annual Interest Rate', 'Annual_Interest_Rate'),
                ('Currency Used in This Model*', 'Currency_Used'),
                ('Exchange rate', 'Exchange_rate'), ('YoY Rental Inflation','YoY_Rental_Inflation'),
                ('YoY Manpower Rate Inflation', 'YoY_Manpower_Rate_Inflation'),
                ('YoY Capex Rate Inflation', 'YoY_Capex_Rate_Inflation'),
                ('YoY OPEX Rate Inflation', 'YoY_OPEX_Rate_Inflation'),
                ('Rent per sqft (builtup)', 'Rent_per_sqft_(builtup)'),
                ('Security Deposit (Months)', 'Security_Deposit_(Months)'),
                ('Annual Interest rate on security deposit (%)', 'Annual_Interest_rate_on_security_deposit_(%)'),
                ('Interest on Working Capital','Interest_on_Working_Capital')]

    if request.method == 'POST':
        if(request.form['Contract_Periodvalue'] != FinancialParameters.query.get(5).value or request.form['Depreciation_Method_for_Investmentvalue'] !=FinancialParameters.query.get(8).value):
            StorageData.query.delete()
            StorageData1.query.delete()
            BUR.query.delete()
            capex.query.delete()
            CapexMisc.query.delete()
            db.session.commit()
        i=0
        for element in parameters:
            element.value = request.form[inp_list[i][1]+'value']
            element.UOM = request.form[inp_list[i][1] + 'UOM']
            element.remarks = request.form[inp_list[i][1] + 'remarks']
            i=i+1
        db.session.commit()
        return redirect(url_for('financialparameters'))


@app.route('/financialparameters/insert', methods=['POST','GET'])
@login_required
def insertfinancialparameters():
    inp_list = [('Minimum EBIT', 'Minimum_EBIT'), ('Allocation Rate', 'Allocation_Rate'),
                ('Discount Rate  (Warehouse Rental + Long Term Liabilities)', 'Discount_Rate'),
                ('Minimum MIRR requirement', 'Minimum_MIRR_requirement'),
                ('Contract Period', 'Contract_Period'),
                ('Average Days Sales Outstanding (DSO)', 'Average_Days_Sales'),
                ('Average Days Payables Outstanding (DPO)', 'Average_Days_Payables'),
                ('Depreciation Method for Investment', 'Depreciation_Method_for_Investment'),
                ('Investments Annual Interest Rate', 'Annual_Interest_Rate'),
                ('Currency Used in This Model*', 'Currency_Used'),
                ('Exchange rate', 'Exchange_rate'), ('YoY Rental Inflation','YoY_Rental_Inflation'),
                ('YoY Manpower Rate Inflation', 'YoY_Manpower_Rate_Inflation'),
                ('YoY Capex Rate Inflation', 'YoY_Capex_Rate_Inflation'),
                ('YoY OPEX Rate Inflation', 'YoY_OPEX_Rate_Inflation'),
                ('Rent per sqft (builtup)', 'Rent_per_sqft_(builtup)'),
                ('Security Deposit (Months)', 'Security_Deposit_(Months)'),
                ('Annual Interest rate on security deposit (%)', 'Annual_Interest_rate_on_security_deposit_(%)'),
                ('Interest on Working Capital','Interest_on_Working_Capital')]

    if request.method == 'POST':
        for element in inp_list:
            entity = element[0]
            value = request.form[element[1] + 'value']
            UOM = request.form[element[1] + 'UOM']
            remarks = request.form[element[1] + 'remarks']

            my_data = FinancialParameters(entity, value, UOM, remarks)
            db.session.add(my_data)
        db.session.commit()
        return redirect(url_for('financialparameters'))



@app.route('/capextrial', methods=['GET', 'POST'])
@login_required
def capexinputtrial():
    # years = int(FinancialParameters.query.get(5).value)
    years = FinancialParameters.query.get(5)
    if years is None:
        return render_template('error.html', message='Please fill in the value for years first.')
    years = int(years.value)

    input_list = [('category', 'Category'), ('items', 'Items'), ('quantity', 'Quantity'), ('uom', 'UOM'),
                  ('unit_cost', 'Unit Cost'), ('depreciation_period', 'Depreciation Period (in years)'),
                  ('maintenance_rate_per_year', 'Maintenance Rate per year (in%)'),
                  ('investment_inclusion', 'Investment Inclusion')
                  ]

    output_list = [('category', 'Category'), ('items', 'Items'), ('quantity', 'Quantity'), ('uom', 'UOM'),
                  ('unit_cost', 'Unit Cost'), ('depreciation_period', 'Depreciation Period (in years)'),
                  ('maintenance_rate_per_year', 'Maintenance Rate per year (in%)'),
                  ('investment_inclusion', 'Investment Inclusion'), ('total_investment', 'Total Investment'),
                  ('monthly_emi', 'Monthly Emi'), ('monthly_depreciation', 'Monthly Depreciation'), ('monthly_interest', 'Monthly Interest'),
                  ('monthly_maintenance_cost', 'Monthly Maintenance Cost')
                   ]

    misc_list_facility = ['Dock Tables + 1 Chairs', 'Conveyor', 'Fire Extinguishers ABC types', 'Metal Detector - Hand Frisking', 'Pedestal Fan - 24"',
                          'Office Setup - Basic - (Area in sq.ft.)', 'Water Dispenser Machine', 'Filing Cabinets', 'Emergency Lighting', 'Canteen Facility - (Area in sq.ft.)',
                          'D.G. Set', 'Attendence System', 'Garbage Bins', 'Display Boards', 'Signagaes', 'CCTV -HD Camera ', 'Dock Leveller - 5 ton (2m X 2.2m)',
                          'Lockers (15 compartments per locker)', 'W/h Electrification', 'Public announcement system', 'Fire prevention', 'Floor Cleaning Machine',
                          ]

    misc_list_it = ['Lease line', 'Laptop', 'Desktops', 'UPS - 1 KVA with 30 mins backup', '4 in 1 (Fax-Printer-Scanner-Copier)', 'Laser printer', 'Inkjet printer',
                    'Label Printer', 'Barcode Printer', 'Gift message printer'
                    ]

    if request.method == 'POST':
        annual_interest_rate = FinancialParameters.query.get(9).value
        if annual_interest_rate is None or annual_interest_rate.value is None:
            return render_template('error.html', message='Please fill in the value for annual_interest_rate in FinancialParameters first.')
        monthly_interest_rate = annual_interest_rate / 1200*1.0


        for i in range(years):
            category = request.form[input_list[0][0]]
            items = request.form[input_list[1][0]]
            year = i
            quantity = float(request.form[input_list[2][0] + str(i)])
            uom = request.form[input_list[3][0]]
            unit_cost = float(request.form[input_list[4][0]])
            depreciation_period = float(request.form[input_list[5][0]])
            maintenance_rate_per_year = float(request.form[input_list[6][0]])
            investment_inclusion = request.form[input_list[7][0]]
            total_investment = round(quantity * unit_cost)
            monthly_emi = round(npf.pmt(monthly_interest_rate, depreciation_period*12, total_investment))*(-1)
            monthly_depreciation = round(total_investment / (depreciation_period * 12))
            monthly_interest = round(total_investment * monthly_interest_rate)
            monthly_maintenance_cost= round(total_investment * maintenance_rate_per_year/1200)

            my_data = CapexMisc(category,items,year,quantity,uom,unit_cost,depreciation_period,
                                    maintenance_rate_per_year,investment_inclusion,total_investment,
                                    monthly_emi,monthly_depreciation,monthly_interest,monthly_maintenance_cost)

            db.session.add(my_data)
            db.session.commit()

    capex_data_storage = capex.query.filter_by(user_id=current_user.id).all()
    capex_data_misc = CapexMisc.query.filter_by(user_id=current_user.id).all()

    num_capex_storage_rows = int(len(capex_data_storage) / years)
    num_capex_misc_rows = int(len(capex_data_misc)/years)

    if num_capex_misc_rows == 0:
        for j in range(len(misc_list_facility)):
            for i in range(years):
                category = "Facility"
                items = misc_list_facility[j]
                year = i
                quantity = None
                uom = None
                unit_cost = None
                depreciation_period = None
                maintenance_rate_per_year = None
                investment_inclusion = None
                total_investment = 0.0
                monthly_emi = 0.0
                monthly_depreciation = 0.0
                monthly_interest = 0.0
                monthly_maintenance_cost = 0.0

                my_data = CapexMisc(category, items, year, quantity, uom, unit_cost, depreciation_period,
                                    maintenance_rate_per_year, investment_inclusion, total_investment,
                                    monthly_emi, monthly_depreciation, monthly_interest, monthly_maintenance_cost)

                db.session.add(my_data)
                db.session.commit()

        for j in range(len(misc_list_it)):
            for i in range(years):
                category = "IT"
                items = misc_list_it[j]
                year = i
                quantity = None
                uom = None
                unit_cost = None
                depreciation_period = None
                maintenance_rate_per_year = None
                investment_inclusion = None
                total_investment = 0.0
                monthly_emi = 0.0
                monthly_depreciation = 0.0
                monthly_interest = 0.0
                monthly_maintenance_cost = 0.0

                my_data = CapexMisc(category, items, year, quantity, uom, unit_cost, depreciation_period,
                                    maintenance_rate_per_year, investment_inclusion, total_investment,
                                    monthly_emi, monthly_depreciation, monthly_interest, monthly_maintenance_cost)

                db.session.add(my_data)
                db.session.commit()

        capex_data_misc = CapexMisc.query.filter_by(user_id=current_user.id).all()
        num_capex_misc_rows = int(len(capex_data_misc)/years)

        #depreciation_method = FinancialParameters.query.get(10).value

    # grand_total_table1 = db.session.query(db.func.sum(capex.total_investment), db.func.sum(capex.monthly_emi), db.func.sum(capex.monthly_depreciation), db.func.sum(capex.monthly_interest), db.func.sum(capex.monthly_maintenance_cost)).group_by(capex.year)
    # grand_total_table2 = db.session.query(db.func.sum(CapexMisc.total_investment), db.func.sum(CapexMisc.monthly_emi), db.func.sum(CapexMisc.monthly_depreciation), db.func.sum(CapexMisc.monthly_interest), db.func.sum(CapexMisc.monthly_maintenance_cost)).group_by(CapexMisc.year)
    grand_total_table1 = db.session.query(db.func.sum(capex.total_investment),db.func.sum(capex.monthly_emi),db.func.sum(capex.monthly_depreciation),db.func.sum(capex.monthly_interest),db.func.sum(capex.monthly_maintenance_cost)).filter(capex.user_id == current_user.id).group_by(capex.year).all()

    grand_total_table2 = db.session.query(db.func.sum(CapexMisc.total_investment),db.func.sum(CapexMisc.monthly_emi),db.func.sum(CapexMisc.monthly_depreciation),db.func.sum(CapexMisc.monthly_interest),db.func.sum(CapexMisc.monthly_maintenance_cost)).filter(CapexMisc.user_id == current_user.id).group_by(CapexMisc.year).all()

    data_list = []

    for i in range(years):
        if num_capex_storage_rows==0:
            data_list.append(grand_total_table2[i][0])
            data_list.append(grand_total_table2[i][1])
            data_list.append(grand_total_table2[i][2])
            data_list.append(grand_total_table2[i][3])
            data_list.append(grand_total_table2[i][4])
        else:
            data_list.append(grand_total_table1[i][0] + grand_total_table2[i][0])
            data_list.append(grand_total_table1[i][1] + grand_total_table2[i][1])
            data_list.append(grand_total_table1[i][2] + grand_total_table2[i][2])
            data_list.append(grand_total_table1[i][3] + grand_total_table2[i][3])
            data_list.append(grand_total_table1[i][4] + grand_total_table2[i][4])
    grand_total_list = ['Total Investment','Monthly EMI', 'Monthly Depreciation', 'Monthly Interest','Monthly Maintenance Cost']
    grand_list_rows = int(len(grand_total_list))
    return render_template('capextrial2.html', capex_data_storage=capex_data_storage, input_list=input_list, output_list=output_list,
                           rows=num_capex_storage_rows, years=years, ncts=num_capex_storage_rows, misc_rows=num_capex_misc_rows,
                           capex_data_misc=capex_data_misc, misc_list_facility=misc_list_facility, misc_list_it=misc_list_it,
                           grand_total_list=grand_total_list, data_list=data_list, grand_list_rows=grand_list_rows)

@app.route('/update_capex', methods = ['GET', 'POST'])
@login_required
def update_capex():
    # years = int(FinancialParameters.query.get(5).value)
    years = FinancialParameters.query.get(5)

    if years is None or years.value is None:
        return render_template('error.html', message='Please fill in the value for years in FinancialParameters first.')

    years = int(years.value)

    input_list = [('id', 'ID'), ('category', 'Category'), ('items', 'Items'), ('quantity', 'Quantity'),
                  ('uom', 'UOM'), ('unit_cost', 'Unit Cost'),
                  ('depreciation_period', 'Depreciation Period (in years)'),
                  ('maintenance_rate_per_year', 'Maintenance Rate per year (in%)'),
                  ('investment_inclusion', 'Investment Inclusion')
                  ]

    if request.method == 'POST':
        annual_interest_rate = FinancialParameters.query.get(9).value
        if annual_interest_rate is None or annual_interest_rate.value is None:
            return render_template('error.html', message='Please fill in the value for annual_interest_rate in FinancialParameters first.')
        monthly_interest_rate = annual_interest_rate/1200

        for i in range(years):
            # my_data1 = capex.query.get(request.form.get('id'))

            temp = years * int(request.form['id']) + (i+1)
            my_data1 = capex.query.get(temp)

            my_data1.uom = str(request.form[input_list[4][0]])
            my_data1.unit_cost = float(request.form[input_list[5][0]])
            my_data1.depreciation_period = float(request.form[input_list[6][0]])
            my_data1.maintenance_rate_per_year = float(request.form[input_list[7][0]])
            my_data1.investment_inclusion = str(request.form[input_list[8][0]])
            my_data1.total_investment = round(my_data1.quantity * my_data1.unit_cost, 1)
            my_data1.monthly_emi = round(npf.pmt(monthly_interest_rate, my_data1.depreciation_period*12, my_data1.total_investment))*(-1)
            my_data1.monthly_depreciation = round(my_data1.total_investment / (my_data1.depreciation_period * 12))
            my_data1.monthly_interest = round(my_data1.total_investment * monthly_interest_rate)
            my_data1.monthly_maintenance_cost = round(my_data1.total_investment * my_data1.maintenance_rate_per_year/1200)
            db.session.commit()
        flash("Process Updated Successfully")
        return redirect(url_for('capexinputtrial'))

@app.route('/update_capex_misc', methods = ['GET', 'POST'])
@login_required
def update_capex_misc():
    # years = int(FinancialParameters.query.get(5).value)
    years = FinancialParameters.query.get(5).value
    if years is None or years.value is None:
        return render_template('error.html', message='Please fill in the value for years in FinancialParameters first.')

    input_list = [('id', 'ID'), ('category', 'Category'), ('items', 'Items'), ('quantity', 'Quantity'),
                  ('uom', 'UOM'),
                  ('unit_cost', 'Unit Cost'), ('depreciation_period', 'Depreciation Period (in years)'),
                  ('maintenance_rate_per_year', 'Maintenance Rate per year (in%)'),
                  ('investment_inclusion', 'Investment Inclusion')
                  ]

    if request.method == 'POST':
        annual_interest_rate = FinancialParameters.query.get(9).value
        if annual_interest_rate is None or annual_interest_rate.value is None:
            return render_template('error.html', message='Please fill in the value for annual_interest_rate in FinancialParameters first.')
        monthly_interest_rate = annual_interest_rate/1200

        for i in range(years):
            # my_data1 = capex.query.get(request.form.get('id'))

            temp = years * int(request.form['id']) + (i+1)
            my_data1 = CapexMisc.query.get(temp)

            my_data1.quantity = float(request.form[input_list[3][0]+ str(i)])
            my_data1.uom = str(request.form[input_list[4][0]])
            my_data1.unit_cost = float(request.form[input_list[5][0]])
            my_data1.depreciation_period = float(request.form[input_list[6][0]])
            my_data1.maintenance_rate_per_year = float(request.form[input_list[7][0]])
            my_data1.investment_inclusion = str(request.form[input_list[8][0]])
            my_data1.total_investment = round(my_data1.quantity * my_data1.unit_cost, 1)
            my_data1.monthly_emi = round(npf.pmt(monthly_interest_rate, my_data1.depreciation_period*12, my_data1.total_investment))*(-1)
            my_data1.monthly_depreciation = round(my_data1.total_investment / (my_data1.depreciation_period * 12))
            my_data1.monthly_interest = round(my_data1.total_investment * monthly_interest_rate)
            my_data1.monthly_maintenance_cost = round(my_data1.total_investment * my_data1.maintenance_rate_per_year/1200)
            db.session.commit()
        flash("Process Updated Successfully")
        return redirect(url_for('capexinputtrial'))

@app.route('/operational_assumptions', methods=['GET', 'POST'])
@login_required
def operational_assumptions():

    input_list = [('parameter_description', 'Parameter Description'), ('value', 'Value'), ('remarks', 'Remarks')]

    if request.method == 'POST':
        parameter_description = str(request.form[input_list[0][0]])
        value = float(request.form[input_list[1][0]])
        remarks = str(request.form[input_list[2][0]])

        my_data = OperationalAssumptions(parameter_description, value, remarks)

        db.session.add(my_data)
        db.session.commit()

    ops_data = OperationalAssumptions.query.filter_by(user_id=current_user.id).all()
    num_rows_ops_data = int(len(ops_data))

    prefill_parameters = ['Working days per month', 'Working days per week', 'Working Efficiency (in %)',
                'Volume fluctuation within a day (in %)', 'Manpower Leaves (in %)', 'Number of working shifts',
                'Working hours per shift']

    prefill_value = [30.0, 7.0, 85.0, 15.0, 12.0, 1.0, 8.0]

    if num_rows_ops_data == 0:
        for i in range(len(prefill_parameters)):
            parameter_description = prefill_parameters[i]
            value = prefill_value[i]
            remarks = "None"

            my_data = OperationalAssumptions(parameter_description, value, remarks)
            db.session.add(my_data)
            db.session.commit()

        ops_data = OperationalAssumptions.query.filter_by(user_id=current_user.id).all()
        num_rows_ops_data = int(len(ops_data))

    return render_template('ops.html', input_list = input_list, ops_data_rows = num_rows_ops_data,
                           ops_data=ops_data)

@app.route('/operationalassumptions/update',methods=['POST','GET'])
@login_required
def update_operational_assumptions():

    input_list = [('id', 'ID'), ('parameter_description', 'Parameter Description'), ('value', 'Value'),
                  ('remarks', 'Remarks')]

    if request.method == 'POST':
        temp = int(request.form['id'])+1
        my_data = OperationalAssumptions.query.get(temp)

        my_data.parameter_description = str(request.form[input_list[1][0]])
        my_data.value = float(request.form[input_list[2][0]])
        my_data.remarks = str(request.form[input_list[3][0]])

        db.session.commit()
        flash("Updated Successfully")

    return redirect(url_for('operational_assumptions'))
#
# @app.route('/labex', methods=['GET', 'POST'])
# def labex():
#
#     years = int(FinancialParameters.query.get(5).value)
#
#     input_list = [('responsibility', 'Responsibility'), ('manpower_rate_per_month', 'Manpower Rate per Month'),
#                   ('manpower', 'Manpower')]
#
#     output_list = [('responsibility', 'Responsibility'), ('manpower_rate_per_month', 'Manpower Rate per Month'),
#                   ('manpower', 'Manpower'), ('total_cost', 'Total Cost')
#                   ]
#     # Check if the formula is working. Comment print statement after the check step
#     responsibility_table = db.session.query(Data.Responsibility).group_by(Data.Responsibility).all()
#
#     responsibility_list = []
#     for i in range(len(responsibility_table)):
#         responsibility_list.append(responsibility_table[i][0])
#     responsibility_list_len = len(responsibility_list)
#
#
#     # Change PFMC to actual name of table: Check head_count, responsibility with actual name of column in PFMC table
#     temp = db.session.query(Data.Responsibility, Data.year, db.func.sum(Data.headcount)).group_by(Data.year,Data.Responsibility).all()
#     if request.method == 'POST':
#         for i in range(years):
#             responsibility = str(request.form[input_list[0][0]])
#             manpower_rate_per_month = float(request.form[input_list[1][0]])
#             year = i
#             manpower = float(request.form[input_list[2][0] + str(i)])
#             total_cost = round(manpower*manpower_rate_per_month)
#
#             my_data = LabexMisc(responsibility, manpower_rate_per_month, year, manpower, total_cost)
#
#             db.session.add(my_data)
#             db.session.commit()
#
#     labex_data = Labex.query.all()
#     num_labex_rows = int(len(labex_data)/years)
#
#     labex_data_misc = LabexMisc.query.all()
#     num_labex_data_misc_rows = int(len(labex_data_misc)/years)
#
#     grand_total_table1 = db.session.query(db.func.sum(Labex.total_cost)).group_by(Labex.year)
#     grand_total_table2 = db.session.query(db.func.sum(LabexMisc.total_cost)).group_by(LabexMisc.year)
#
#     grand_total_list = []
#     for i in range(years):
#         if num_labex_data_misc_rows==0 and num_labex_rows==0:
#             grand_total_list=[]
#         elif (num_labex_data_misc_rows==0):
#             grand_total_list.append(grand_total_table1[i][0])
#         elif (num_labex_rows==0):
#             grand_total_list.append(grand_total_table2[i][0])
#         else:
#             grand_total_list.append(grand_total_table1[i][0] + grand_total_table2[i][0])
#
#     return render_template('labex.html', labex_data=labex_data, input_list=input_list, output_list=output_list,
#                            rows=num_labex_rows, years=years, ncts=num_labex_rows, responsibility_list=responsibility_list,
#                            labex_data_misc=labex_data_misc, misc_rows=num_labex_data_misc_rows,
#                            responsibility_list_len=responsibility_list_len, temp=temp, grand_total_list=grand_total_list)
#
# @app.route('/update_labex', methods = ['GET', 'POST'])
# def update_labex():
#     years = int(FinancialParameters.query.get(5).value)
#
#     input_list = [('id', 'ID'), ('responsibility', 'Responsibility'), ('manpower_rate_per_month', 'Manpower Rate per Month'),
#                   ('manpower', 'Manpower'), ('total_cost', 'Total Cost')
#                   ]
#
#     if request.method == 'POST':
#         for i in range(years):
#             temp = years* int(request.form['id']) + (i + 1)
#             my_data = Labex.query.get(temp)
#
#             my_data.manpower_rate_per_month = float(request.form[input_list[2][0]])
#             my_data.manpower = float(request.form[input_list[3][0] + str(i)])
#             my_data.total_cost = round(my_data.manpower_rate_per_month * my_data.manpower)
#
#             db.session.commit()
#         flash("Process Updated Successfully")
#         return redirect(url_for('labex'))
#
# @app.route('/update_labex_misc', methods = ['GET', 'POST'])
# def update_labex_misc():
#     years = int(FinancialParameters.query.get(5).value)
#
#     input_list = [('id', 'ID'), ('responsibility', 'Responsibility'), ('manpower_rate_per_month', 'Manpower Rate per Month'),
#                   ('manpower', 'Manpower'), ('total_cost', 'Total Cost')
#                   ]
#
#     if request.method == 'POST':
#         for i in range(years):
#             temp = years* int(request.form['id']) + (i + 1)
#             my_data = LabexMisc.query.get(temp)
#
#             my_data.responsibility = str(request.form[input_list[1][0]])
#             my_data.manpower_rate_per_month = float(request.form[input_list[2][0]])
#             my_data.manpower = float(request.form[input_list[3][0] + str(i)])
#             my_data.total_cost = round(my_data.manpower*my_data.manpower_rate_per_month)
#
#             db.session.commit()
#         flash("Process Updated Successfully")
#         return redirect(url_for('labex'))
#

@app.route('/labex', methods=['GET', 'POST'])
@login_required
def labex():

    # years = int(FinancialParameters.query.get(5).value)
    # inflation_rate = float(FinancialParameters.query.get(13).value/100)
    years = FinancialParameters.query.get(5)

    if years is None:
        return render_template('error.html', message='Please fill in the value for years in FinancialParameters first.')
    years=int(years.value)
    inflation_rate =FinancialParameters.query.get(13)

    if inflation_rate is None:
        return render_template('error.html', message='Please fill in the value for inflation_rate in FinancialParameters first.')
    inflation_rate =float(inflation_rate .value / 100)

    input_list = [('responsibility', 'Responsibility'), ('manpower_rate_per_month', 'Manpower Rate per Month'),
                  ('manpower', 'Manpower')]

    output_list = [('responsibility', 'Responsibility'), ('manpower_rate_per_month', 'Manpower Rate per Month'),
                  ('manpower', 'Manpower'), ('total_cost', 'Total Cost')
                  ]
    # Check if the formula is working. Comment print statement after the check step
    # responsibility_table = db.session.query(Data.Responsibility).group_by(Data.Responsibility).all()
    responsibility_table = db.session.query(Data.Responsibility).filter(Data.user_id == current_user.id).group_by(Data.Responsibility).all()

    responsibility_list = []
    for i in range(len(responsibility_table)):
        responsibility_list.append(responsibility_table[i][0])
    responsibility_list_len = len(responsibility_list)


    # Change PFMC to actual name of table: Check head_count, responsibility with actual name of column in PFMC table
    # temp = db.session.query(Data.Responsibility, Data.year, db.func.sum(Data.headcount)).group_by(Data.year,Data.Responsibility).all()
    temp = db.session.query(Data.Responsibility, Data.year, db.func.sum(Data.headcount)).filter(Data.user_id == current_user.id).group_by(Data.year, Data.Responsibility).all()

    if request.method == 'POST':
        for i in range(years):
            responsibility = str(request.form[input_list[0][0]])
            manpower_rate_per_month = float(request.form[input_list[1][0]])
            year = i
            manpower = float(request.form[input_list[2][0] + str(i)])
            total_cost = round(manpower*manpower_rate_per_month*(1+inflation_rate)**i)

            my_data = LabexMisc(responsibility, manpower_rate_per_month, year, manpower, total_cost)

            db.session.add(my_data)
            db.session.commit()

    labex_data = Labex.query.filter_by(user_id=current_user.id).all()
    num_labex_rows = int(len(labex_data)/years)

    labex_data_misc = LabexMisc.query.filter_by(user_id=current_user.id).all()
    num_labex_data_misc_rows = int(len(labex_data_misc)/years)

    # grand_total_table1 = db.session.query(db.func.sum(Labex.total_cost)).group_by(Labex.year)
    # grand_total_table2 = db.session.query(db.func.sum(LabexMisc.total_cost)).group_by(LabexMisc.year)
    grand_total_table1 = db.session.query(db.func.sum(Labex.total_cost)).filter(Labex.user_id == current_user.id).group_by(Labex.year).all()
    grand_total_table2 = db.session.query(db.func.sum(LabexMisc.total_cost)).filter(LabexMisc.user_id == current_user.id).group_by(LabexMisc.year).all()


    grand_total_list = []
    for i in range(years):
        if num_labex_data_misc_rows==0 and num_labex_rows==0:
            grand_total_list=[]
        elif (num_labex_data_misc_rows==0):
            grand_total_list.append(grand_total_table1[i][0])
        elif (num_labex_rows==0):
            grand_total_list.append(grand_total_table2[i][0])
        else:
            grand_total_list.append(grand_total_table1[i][0] + grand_total_table2[i][0])

    return render_template('labex.html', labex_data=labex_data, input_list=input_list, output_list=output_list,
                           rows=num_labex_rows, years=years, ncts=num_labex_rows, responsibility_list=responsibility_list,
                           labex_data_misc=labex_data_misc, misc_rows=num_labex_data_misc_rows,
                           responsibility_list_len=responsibility_list_len, temp=temp, grand_total_list=grand_total_list)

@app.route('/update_labex', methods = ['GET', 'POST'])
@login_required
def update_labex():
    # years = int(FinancialParameters.query.get(5).value)
    # inflation_rate = float(FinancialParameters.query.get(13).value / 100)
    years = int(FinancialParameters.query.get(5).value)

    if years is None:
        return render_template('error.html', message='Please fill in the value for years in FinancialParameters first.')

    inflation_rate = float(FinancialParameters.query.get(13).value / 100)

    if inflation_rate is None:
        return render_template('error.html', message='Please fill in the value for inflation_rate in FinancialParameters first.')


    input_list = [('id', 'ID'), ('responsibility', 'Responsibility'), ('manpower_rate_per_month', 'Manpower Rate per Month'),
                  ('manpower', 'Manpower'), ('total_cost', 'Total Cost')
                  ]

    if request.method == 'POST':
        for i in range(years):
            temp = years* int(request.form['id']) + (i + 1)
            my_data = Labex.query.get(temp)

            my_data.manpower_rate_per_month = float(request.form[input_list[2][0]])
            my_data.manpower = float(request.form[input_list[3][0] + str(i)])
            my_data.total_cost = round(my_data.manpower_rate_per_month * my_data.manpower*(1+inflation_rate)**i)

            db.session.commit()
        flash("Process Updated Successfully")
        return redirect(url_for('labex'))

@app.route('/update_labex_misc', methods = ['GET', 'POST'])
@login_required
def update_labex_misc():
    # years = int(FinancialParameters.query.get(5).value)
    # inflation_rate = float(FinancialParameters.query.get(13).value / 100)
    years = int(FinancialParameters.query.get(5).value)

    if years is None:
        return render_template('error.html', message='Please fill in the value for years in FinancialParameters first.')

    inflation_rate = FinancialParameters.query.get(13)

    if inflation_rate is None:
        return render_template('error.html', message='Please fill in the value for inflation_rate in FinancialParameters first.')
    inflation_rate=float(inflation_rate.value / 100)

    input_list = [('id', 'ID'), ('responsibility', 'Responsibility'), ('manpower_rate_per_month', 'Manpower Rate per Month'),
                  ('manpower', 'Manpower'), ('total_cost', 'Total Cost')
                  ]

    if request.method == 'POST':
        for i in range(years):
            temp = years* int(request.form['id']) + (i + 1)
            my_data = LabexMisc.query.get(temp)

            my_data.responsibility = str(request.form[input_list[1][0]])
            my_data.manpower_rate_per_month = float(request.form[input_list[2][0]])
            my_data.manpower = float(request.form[input_list[3][0] + str(i)])
            my_data.total_cost = round(my_data.manpower*my_data.manpower_rate_per_month*(1+inflation_rate)**i)

            db.session.commit()
        flash("Process Updated Successfully")
        return redirect(url_for('labex'))


@app.route('/opex', methods=['GET', 'POST'])
@login_required
def opex():

    # years = int(FinancialParameters.query.get(5).value)
    # inflation_rate = float(FinancialParameters.query.get(15).value)/100
    years = FinancialParameters.query.get(5)

    if years is None:
        return render_template('error.html', message='Please fill in the value for years in FinancialParameters first.')
    years=int(years.value)
    inflation_rate = float(FinancialParameters.query.get(13).value / 100)

    if inflation_rate is None:
        return render_template('error.html', message='Please fill in the value for inflation_rate in FinancialParameters first.')


    input_list = [('category', 'Category'), ('running_costs_description', 'Running Costs Description'),
                  ('unit_cost', 'Unit Cost'), ('units', 'Units')]
    output_list = [('category', 'Category'), ('running_costs_description', 'Running Costs Description'),
                  ('unit_cost', 'Unit Cost'), ('units', 'Units'), ('running_cost', 'Running Cost')
                  ]

    if request.method == 'POST':
        for i in range(years):
            category = str(request.form[input_list[0][0]])
            running_costs_description = str(request.form[input_list[1][0]])
            unit_cost = float(request.form[input_list[2][0]])
            year = i
            units = float(request.form[input_list[3][0] + str(i)])
            running_cost = round(unit_cost * units * (1+inflation_rate)**year)

            my_data = OpexMisc(category, running_costs_description, unit_cost, year, units, running_cost)
            db.session.add(my_data)
            db.session.commit()

    opex_list = ['Staff welfare (i.e. tea, coffee, etc.) FTE', 'Staff welfare (i.e. tea, coffee, etc.) Contract', 'Pallets',
                 'Mobile', 'Data Card', 'Repair & Maintenance - Capex', 'Transportation Cost', 'Pest Control', 'Cleaning & Maintenance',
                 'Diesel for Generator', 'Electricity Rates', 'Aisle Painting', 'PPE', 'Office Expenses- Paper & other stationary', 'Reach Truck',
                 'Order Picker', 'Lease line running cost']

    opex_data = Opex.query.filter_by(user_id=current_user.id).all()
    num_opex_rows = int(len(opex_data)/years)

    if num_opex_rows == 0:
        for j in range(len(opex_list)):
            for i in range(years):
                category = ""
                running_costs_description = opex_list[j]
                unit_cost = 0.0
                year = i
                units = 0.0
                running_cost = 0.0

                my_data = Opex(category, running_costs_description, unit_cost, year, units, running_cost)
                db.session.add(my_data)
        db.session.commit()

        opex_data = Opex.query.filter_by(user_id=current_user.id).all()
        num_opex_rows = int(len(opex_data) / years)

    opex_data_misc = OpexMisc.query.filter_by(user_id=current_user.id).all()
    num_opex_rows_misc = int(len(opex_data_misc)/years)

    grand_total_table1 = db.session.query(db.func.sum(Opex.running_cost)).group_by(Opex.year)
    grand_total_table2 = db.session.query(db.func.sum(OpexMisc.running_cost)).group_by(OpexMisc.year)

    grand_total_list = []
    for i in range(years):
        if num_opex_rows_misc==0:
            grand_total_list.append(grand_total_table1[i][0])
        else:
            grand_total_list.append(grand_total_table1[i][0] + grand_total_table2[i][0])
    return render_template('opex.html', opex_data=opex_data, input_list=input_list, rows=num_opex_rows,
                           years=years, ncts=num_opex_rows, opex_list=opex_list,
                           opex_data_misc=opex_data_misc, misc_rows=num_opex_rows_misc, output_list=output_list,
                           grand_total_list=grand_total_list)

@app.route('/update_opex', methods = ['GET', 'POST'])
@login_required
def update_opex():
    # years = int(FinancialParameters.query.get(5).value)
    # inflation_rate = float(FinancialParameters.query.get(15).value/100)
    years = int(FinancialParameters.query.get(5).value)

    if years is None:
        return render_template('error.html', message='Please fill in the value for years in FinancialParameters first.')

    inflation_rate = float(FinancialParameters.query.get(13).value / 100)

    if inflation_rate is None:
        return render_template('error.html', message='Please fill in the value for inflation_rate in FinancialParameters first.')


    input_list = [('id', 'ID'), ('category', 'Category'), ('running_costs_description', 'Running Costs Description'),
                  ('unit_cost', 'Unit Cost'), ('units', 'Units')]

    if request.method == 'POST':
        for i in range(years):
            temp = years * int(request.form['id']) + (i + 1)
            my_data = Opex.query.get(temp)

            my_data.category = str(request.form[input_list[1][0]])
            my_data.unit_cost = float(request.form[input_list[3][0]])
            my_data.units = float(request.form[input_list[4][0] + str(i)])
            my_data.running_cost = round(my_data.unit_cost*my_data.units*(1+inflation_rate)**i)

            db.session.commit()
        flash("Process Updated Successfully")
        return redirect(url_for('opex'))

@app.route('/update_opex_misc', methods = ['GET', 'POST'])
@login_required
def update_opex_misc():
    # years = int(FinancialParameters.query.get(5).value)
    # inflation_rate = float(FinancialParameters.query.get(15).value)/100
    years = int(FinancialParameters.query.get(5).value)

    if years is None:
        return render_template('error.html', message='Please fill in the value for years in FinancialParameters first.')

    inflation_rate = float(FinancialParameters.query.get(13).value / 100)

    if inflation_rate is None:
        return render_template('error.html', message='Please fill in the value for inflation_rate in FinancialParameters first.')


    input_list = [('id', 'ID'), ('category', 'Category'), ('running_costs_description', 'Running Costs Description'),
                  ('unit_cost', 'Unit Cost'), ('units', 'Units')]

    if request.method == 'POST':
        for i in range(years):
            temp = years * int(request.form['id']) + (i + 1)
            my_data = OpexMisc.query.get(temp)

            my_data.category = str(request.form[input_list[1][0]])
            my_data.running_costs_description = str(request.form[input_list[2][0]])
            my_data.unit_cost = float(request.form[input_list[3][0]])
            my_data.units = float(request.form[input_list[4][0] + str(i)])
            my_data.running_cost = round(my_data.unit_cost*my_data.units*(1+inflation_rate)**i)

            db.session.commit()
        flash("Process Updated Successfully")
        return redirect(url_for('opex'))

@app.route('/project_implementation_cost', methods=['GET', 'POST'])
@login_required
def project_implementation_cost():

    input_list = [('startup_expense', 'Startup Expense'), ('uom', 'UOM'), ('units', 'Units'), ('cost_per_unit', 'Cost per unit'),
                  ('percentage_consideration', 'Percentage Consideration')]

    output_list = [('startup_expense', 'Startup Expense'), ('uom', 'UOM'), ('units', 'Units'), ('cost_per_unit', 'Cost per unit'),
                  ('percentage_consideration', 'Percentage Consideration'), ('total_cost', 'Total Cost')
                  ]

    if request.method == 'POST':
        startup_expense = str(request.form[input_list[0][0]])
        uom = str(request.form[input_list[1][0]])
        units = float(request.form[input_list[2][0]])
        cost_per_unit = float(request.form[input_list[3][0]])
        percentage_consideration = float(request.form[input_list[4][0]])
        total_cost = round(units * cost_per_unit * percentage_consideration / 100)

        my_data = PIC(startup_expense, uom, units, cost_per_unit, percentage_consideration, total_cost)
        db.session.add(my_data)
        db.session.commit()

    pic_data = PIC.query.filter_by(user_id=current_user.id).all()
    num_pic_rows = int(len(pic_data))

    grand_total_table = db.session.query(db.func.sum(PIC.total_cost))
    grand_total = grand_total_table[0][0]

    return render_template('pic.html', pic_data=pic_data, input_list=input_list, rows=num_pic_rows,
                           output_list=output_list, grand_total=grand_total)

@app.route('/update_project_implementation_cost', methods = ['GET', 'POST'])
@login_required
def update_project_implementation_cost():
    input_list = [('id','ID'), ('startup_expense', 'Startup Expense'), ('uom', 'UOM'), ('units', 'Units'), ('cost_per_unit', 'Cost per unit'),
                  ('percentage_consideration', 'Percentage Consideration')
                  ]

    if request.method == 'POST':
        temp = int(request.form['id']) + 1
        my_data = PIC.query.get(temp)
        my_data.startup_expense = str(request.form[input_list[1][0]])
        my_data.uom = str(request.form[input_list[2][0]])
        my_data.units = float(request.form[input_list[3][0]])
        my_data.cost_per_unit = float(request.form[input_list[4][0]])
        my_data.percentage_consideration = float(request.form[input_list[5][0]])
        my_data.total_cost = round(my_data.units * my_data.cost_per_unit * my_data.percentage_consideration / 100)

        db.session.commit()

        flash("Process Updated Successfully")
        return redirect(url_for('project_implementation_cost'))

@app.route('/one_time_cost', methods=['GET', 'POST'])
@login_required
def one_time_cost():

    input_list = [('cost_head_description', 'Cost Head Description'), ('uom', 'UOM'), ('units', 'Units'), ('cost_per_unit', 'Cost per unit'),
                  ('percentage_consideration', 'Percentage Consideration')
                  ]
    output_list = [('cost_head_description', 'Cost Head Description'), ('uom', 'UOM'), ('units', 'Units'), ('cost_per_unit', 'Cost per unit'),
                  ('percentage_consideration', 'Percentage Consideration'), ('total_cost', 'Total Cost')
                  ]

    if request.method == 'POST':
        cost_head_description = str(request.form[input_list[0][0]])
        uom = str(request.form[input_list[1][0]])
        units = float(request.form[input_list[2][0]])
        cost_per_unit = float(request.form[input_list[3][0]])
        percentage_consideration = float(request.form[input_list[4][0]])
        total_cost = round(units * cost_per_unit * percentage_consideration /100)

        my_data = OneTimeCost(cost_head_description, uom, units, cost_per_unit, percentage_consideration, total_cost)
        db.session.add(my_data)
        db.session.commit()

    otc_data = OneTimeCost.query.filter_by(user_id=current_user.id).all()
    num_otc_rows = int(len(otc_data))

    grand_total_table = db.session.query(db.func.sum(OneTimeCost.total_cost))
    grand_total = grand_total_table[0][0]
    return render_template('otc.html', otc_data=otc_data, input_list=input_list, output_list=output_list,
                           rows=num_otc_rows, grand_total=grand_total)

@app.route('/update_one_time_cost', methods = ['GET', 'POST'])
@login_required
def update_one_time_cost():

    input_list = [('id','ID'), ('cost_head_description', 'Cost Head Description'), ('uom', 'UOM'), ('units', 'Units'), ('cost_per_unit', 'Cost per unit'),
                  ('percentage_consideration', 'Percentage Consideration')
                  ]

    if request.method == 'POST':
        temp = int(request.form['id']) + 1
        my_data = OneTimeCost.query.get(temp)
        my_data.cost_head_description = str(request.form[input_list[1][0]])
        my_data.uom = str(request.form[input_list[2][0]])
        my_data.units = float(request.form[input_list[3][0]])
        my_data.cost_per_unit = float(request.form[input_list[4][0]])
        my_data.percentage_consideration = float(request.form[input_list[5][0]])
        my_data.total_cost =round(my_data.units * my_data.cost_per_unit * my_data.percentage_consideration /100)

        db.session.commit()

        flash("Process Updated Successfully")
        return redirect(url_for('one_time_cost'))

@app.route('/commercial', methods=['GET', 'POST'])
@login_required
def commercial():

    # years = int(FinancialParameters.query.get(5).value)
    # user_current=current_user.id
    # years = FinancialParameters.query.filter_by(user_id=current_user.id, id=((user_current-1)*19)+5).first()
    years = FinancialParameters.query.get(5)

    if years is None:
        return render_template('error.html', message='Please fill in the value for years in FinancialParameters first.')

    years=int(years.value)
    input_list = [('monthly_cost_breakup', 'Monthly Cost Break-up'), ('overhead', 'Overhead'),
                  ('management_fee', 'Management Fee')]

    output_list = [('monthly_cost_breakup', 'Monthly Cost Break-up'), ('overhead', 'Overhead'),
                  ('management_fee', 'Management Fee'), ('total_cost', 'Total Cost')]

    commercial_list = ['Rentals', 'Manpower', 'Equipments', 'Operating Cost', 'Implementation Cost']
    commercial_list_sub = ['Working Capital', 'Overhead', 'Management Fee']

    commercial_data = Commercial.query.filter_by(user_id=current_user.id).all()
    num_commercial_rows = int(len(commercial_data)/years)

    if num_commercial_rows == 0:
        for j in range(len(commercial_list)):
            for i in range(years):
                monthly_cost_breakup = commercial_list[j]
                overhead = 0.0
                management_fee = 0.0
                year = i
                total_cost = 0.0

                my_data = Commercial(monthly_cost_breakup, overhead, management_fee, year, total_cost)
                db.session.add(my_data)
        db.session.commit()

        commercial_data = Commercial.query.filter_by(user_id=current_user.id).all()
        num_commercial_rows = int(len(commercial_data) / years)

    # temp1 = db.session.query(StorageData.year, db.func.sum(StorageData.Storage_area_required)).group_by(StorageData.year).all()
    # temp2 = db.session.query(StorageData1.year, db.func.sum(StorageData1.area)).group_by(StorageData1.year).all()
    temp1 = db.session.query(StorageData.year, db.func.sum(StorageData.Storage_area_required)).filter(StorageData.user_id == current_user.id).group_by(StorageData.year).all()

    temp2 = db.session.query(StorageData1.year, db.func.sum(StorageData1.area)).filter(StorageData1.user_id == current_user.id).group_by(StorageData1.year).all()

    carpet_area = []

    temp1_len = len(temp1)
    temp2_len = len(temp2)
    if (temp1 and temp2):
        for i in range(years):
            if (temp1_len > 0 and temp2_len > 0):
                carpet_area.append(round(temp1[i][1]) + round(temp2[i][1]))
            elif temp1_len > 0:
                carpet_area.append(round(temp1[i][1]))
            elif temp2_len > 0:
                carpet_area.append(round(temp2[i][1]))
            else:
                print()

    bur = BUR.query.filter_by(user_id=current_user.id).all()

    # Rent_per_sqft = FinancialParameters.query.get(16).value
    # Security_Deposit = FinancialParameters.query.get(17).value
    # Annual_rate_onsecuritydeposit = FinancialParameters.query.get(18).value
    Rent_per_sqft = FinancialParameters.query.get(16)
    Security_Deposit = FinancialParameters.query.get(17)
    Annual_rate_onsecuritydeposit = FinancialParameters.query.get(18)

    if Rent_per_sqft is None or Rent_per_sqft.value is None:
        return render_template('error.html', message='Please fill in the value for Rent_per_sqft in FinancialParameters first.')

    if Security_Deposit is None or Security_Deposit.value is None:
        return render_template('error.html', message='Please fill in the value for Security_Deposit in FinancialParameters first.')

    if Annual_rate_onsecuritydeposit is None or Annual_rate_onsecuritydeposit.value is None:
        return render_template('error.html', message='Please fill in the value for Annual_rate_onsecuritydeposit in FinancialParameters first.')

    Rent_per_sqft = FinancialParameters.query.get(16).value
    Security_Deposit = FinancialParameters.query.get(17).value
    Annual_rate_onsecuritydeposit = FinancialParameters.query.get(18).value

    Monthly_Interest_onsecuritydeposit = []
    monthly_rental = []

    if bur:
        for i in range(years):
            monthly_rental.append(round((carpet_area[i] * (1 + bur[i].value / 100) + 100 - carpet_area[i] * (1 + bur[i].value / 100) % 100) * Rent_per_sqft))

        for i in monthly_rental:
            Monthly_Interest_onsecuritydeposit.append(round(i * Security_Deposit * Annual_rate_onsecuritydeposit / 12/100))

        for i in range(years):
            Commercial.query.get(i+1).total_cost = monthly_rental[i]+Monthly_Interest_onsecuritydeposit[i]


    # temp1 = db.session.query(Labex.year, db.func.sum(Labex.total_cost)).group_by(Labex.year).all()
    # temp2 = db.session.query(LabexMisc.year, db.func.sum(LabexMisc.total_cost)).group_by(LabexMisc.year).all()
    temp1 = db.session.query(Labex.year, db.func.sum(Labex.total_cost)).filter(Labex.user_id == current_user.id).group_by(Labex.year).all()

    temp2 = db.session.query(LabexMisc.year, db.func.sum(LabexMisc.total_cost)).filter(LabexMisc.user_id == current_user.id).group_by(LabexMisc.year).all()

    if (temp1 and temp2):
        for i in range(years):
            Commercial.query.get(i+1 + years).total_cost = round(temp1[i][1] + temp2[i][1])

    # temp1 = db.session.query(Opex.year, db.func.sum(Opex.running_cost)).group_by(Opex.year).all()
    # temp2 = db.session.query(OpexMisc.year, db.func.sum(OpexMisc.running_cost)).group_by(OpexMisc.year).all()
    temp1 = db.session.query(Opex.year, db.func.sum(Opex.running_cost)).filter(Opex.user_id == current_user.id).group_by(Opex.year).all()

    temp2 = db.session.query(OpexMisc.year, db.func.sum(OpexMisc.running_cost)).filter(OpexMisc.user_id == current_user.id).group_by(OpexMisc.year).all()

    if (temp1 and temp2):
        for i in range(years):
            Commercial.query.get(i + 1 + 3*years).total_cost = round(temp1[i][1] + temp2[i][1])


    if FinancialParameters.query.get(8).value == 0:
        # temp1 = db.session.query(capex.year, db.func.sum(capex.monthly_depreciation)).group_by(capex.year).all()
        # temp2 = db.session.query(capex.year, db.func.sum(capex.monthly_interest)).group_by(capex.year).all()
        # temp3 = db.session.query(CapexMisc.year, db.func.sum(CapexMisc.monthly_depreciation)).group_by(CapexMisc.year).all()
        # temp4 = db.session.query(CapexMisc.year,db.func.sum(CapexMisc.monthly_interest)).group_by(CapexMisc.year).all()
        temp1 = db.session.query(capex.year, db.func.sum(capex.monthly_depreciation)).filter(capex.user_id == current_user.id).group_by(capex.year).all()

        temp2 = db.session.query(capex.year, db.func.sum(capex.monthly_interest)).filter(capex.user_id == current_user.id).group_by(capex.year).all()

        temp3 = db.session.query(CapexMisc.year, db.func.sum(CapexMisc.monthly_depreciation)).filter(CapexMisc.user_id == current_user.id).group_by(CapexMisc.year).all()

        temp4 = db.session.query(CapexMisc.year, db.func.sum(CapexMisc.monthly_interest)).filter(CapexMisc.user_id == current_user.id).group_by(CapexMisc.year).all()

        if (temp1 and temp3):
            for i in range(years):
                Commercial.query.get(i + 1 + 2 * years).total_cost = round(temp1[i][1] + temp2[i][1]+ temp3[i][1]+ temp4[i][1])

    else:
        # temp1 = db.session.query(capex.year, db.func.sum(capex.monthly_emi)).group_by(capex.year).all()
        # temp2 = db.session.query(CapexMisc.year, db.func.sum(CapexMisc.monthly_emi)).group_by(CapexMisc.year).all()
        temp1 = db.session.query(capex.year, db.func.sum(capex.monthly_emi)).filter(capex.user_id == current_user.id).group_by(capex.year).all()

        temp2 = db.session.query(CapexMisc.year, db.func.sum(CapexMisc.monthly_emi)).filter(CapexMisc.user_id == current_user.id).group_by(CapexMisc.year).all()
        if (temp1 and temp2):
            for i in range(years):
                Commercial.query.get(i + 1 + 2*years).total_cost = round(temp1[i][1] + temp2[i][1])

    if FinancialParameters.query.get(8).value == 1:
        temp1 = db.session.query(db.func.sum(PIC.total_cost)).all()
        # annual_interest_rate = FinancialParameters.query.get(9).value
        if annual_interest_rate is None :
            return render_template('error.html', message='Please fill in the value FinancialParameters first.')
        annual_interest_rate = annual_interest_rate.value
        
        monthly_interest_rate = annual_interest_rate / 1200 * 1.0
        monthly_emi = round(npf.pmt(monthly_interest_rate, years * 12, temp1[0][0])) * (-1)
        for i in range(years):
            Commercial.query.get(i + 1 + 4 * years).total_cost = monthly_emi
    else:
        monthly_interest_rate = FinancialParameters.query.get(9).value / 1200 * 1.0
        temp1 = db.session.query(db.func.sum(PIC.total_cost)).all()
        # for i in range(years):
        #     Commercial.query.get(i + 1 + 4 * years).total_cost = round(temp1[0][0]/years/12 + temp1[0][0]*monthly_interest_rate)
        if temp1 and temp1[0][0] is not None:
            for i in range(years):
                Commercial.query.get(i + 1 + 4 * years).total_cost = round(temp1[0][0]/years/12 + temp1[0][0]*monthly_interest_rate)
        else:
            # Handle the case when temp1 or temp1[0][0] is None
            # Assign a default value or perform alternative logic
            for i in range(years):
                Commercial.query.get(i + 1 + 4 * years).total_cost = 0 
    db.session.commit()

    subtotal = db.session.query(Commercial.year, db.func.sum(Commercial.total_cost)).group_by(Commercial.year).all()
    workingcapital = []
    for i in subtotal:
        workingcapital.append(round(i[1]*FinancialParameters.query.get(19).value/1200))

    overhead = db.session.query(Commercial.year, db.func.sum(Commercial.total_cost*Commercial.overhead/100)).group_by(Commercial.year).all()
    for i in range(years):
        overhead[i] = round(overhead[i][1])
    managementfee = db.session.query(Commercial.year, db.func.sum(Commercial.total_cost*Commercial.management_fee/100)).group_by(Commercial.year).all()
    for i in range(years):
        managementfee[i] = round(managementfee[i][1])

    onetime = db.session.query(db.func.sum(OneTimeCost.total_cost)).all()

    return render_template('commercial.html', commercial_data=commercial_data, input_list=input_list,
                           rows=num_commercial_rows, years=years, ncts=num_commercial_rows,
                           output_list=output_list, subtotal = subtotal,workingcapital=workingcapital,
                           overhead= overhead, managementfee = managementfee, onetime = onetime)

@app.route('/update_commercial', methods = ['GET', 'POST'])
@login_required
def update_commercial():
    # years = int(FinancialParameters.query.get(5).value)
    years = FinancialParameters.query.get(5)

    if years is None:
        return render_template('error.html', message='Please fill in the value for years in FinancialParameters first.')

    years=int(years.value)
    input_list = [('id', 'ID'), ('monthly_cost_breakup', 'Monthly Cost Break-up'), ('overhead', 'Overhead'),
                  ('management_fee', 'Management Fee')]

    if request.method == 'POST':
        for i in range(years):
            temp = years * int(request.form['id']) + (i + 1)
            my_data = Commercial.query.get(temp)

            my_data.overhead = float(request.form[input_list[2][0]])
            my_data.management_fee = float(request.form[input_list[3][0]])

            db.session.commit()
        flash("Process Updated Successfully")
        return redirect(url_for('commercial'))

@app.route('/general_assumptions')
@login_required
def general_assumptions():
    data = GA.query.filter_by(user_id=current_user.id).all()

    return render_template('general_assumptions.html',data = data )


@app.route('/ga_add',methods=['GET','POST'])
@login_required
def ga_add():
    if request.method == 'POST':
        assumption = request.form['assumption']
        my_data = GA(assumption)
        db.session.add(my_data)
        db.session.commit()
        return redirect(url_for('general_assumptions'))


@app.route('/ga_update', methods=['GET','POST'])
@login_required
def ga_update():
    if request.method == 'POST':
        id = request.form['id']
        print(id)
        my_data = GA.query.get(id)
        my_data.assumption = request.form['assumption']

        db.session.commit()
        return redirect(url_for('general_assumptions'))



@app.route('/project_details')
@login_required
def project_details():
    data = PD.query.filter_by(user_id=current_user.id).all()

    return render_template('project_details.html',data = data )


@app.route('/pd_add',methods=['GET','POST'])
@login_required
def pd_add():
    if request.method == 'POST':
        date = request.form['date']
        project_member = request.form['project_member']
        due_date = request.form['due_date']
        scope = request.form['scope']
        location = request.form['location']
        tender = request.form['tender']
        op_id = request.form['op_id']

        my_data = PD(date, project_member, due_date, scope, location, tender, op_id)

        db.session.add(my_data)
        db.session.commit()
        return redirect(url_for('project_details'))


@app.route('/pd_update', methods=['GET','POST'])
@login_required
def pd_update():
    if request.method == 'POST':

        my_data = PD.query.get(1)
        my_data.date = request.form['date']
        my_data.project_member = request.form['project_member']
        my_data.due_date = request.form['due_date']
        my_data.scope = request.form['scope']
        my_data.location = request.form['location']
        my_data.tender = request.form['tender']
        my_data.op_id = request.form['op_id']


        db.session.commit()
        return redirect(url_for('project_details'))


if __name__ == '__main__':
    # app.debug=True   
    # app.run(host='0.0.0.0',port=5000)
    app.run(debug=False,host='0.0.0.0')
