print("Hello world")

from flask import Flask,render_template,request,session,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user,login_manager,LoginManager
from flask_login import login_required,current_user
from sqlalchemy import create_engine,update
from datetime import datetime
# my db connection
local_server = True
app = Flask(__name__)
app.secret_key = 'sudeepa'
#for getting user access
login_manager=LoginManager(app)
login_manager.login_view='login'

@login_manager.user_loader
def load_user(user_id):
    return Info.query.get(int(user_id))
# app.config['SQLALCHEMY_DATABASE_URI']='mysql://username:password@localhost/database_name'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:@localhost:3307/travel'

db = SQLAlchemy(app)

from sqlalchemy import create_engine,text
from sqlalchemy.orm import sessionmaker

# db_uri = 'mysql+mysqldb://root:@localhost:3307/bus'
# dbd = create_engine(db_uri)


# creating db models (tables)
class Info(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(500))
    password = db.Column(db.String(1000))

class Passengers(db.Model):
    t_id= db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String(500))
    Name= db.Column(db.String(500))
    ticket_id=db.Column(db.Integer)
    action=db.Column(db.String(400))
    timestamp=db.Column(db.String(600))


class Ticket(db.Model):
    ticket_id= db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(500))
    Name= db.Column(db.String(500))
    bus_no= db.Column(db.Integer)
    seat_no=db.Column(db.Integer)
    time=db.Column(db.String(600))
    Travel_date=db.Column(db.String(500))
    From=db.Column(db.String(400))
    To=db.Column(db.String(600))
    #ticket_id=db.column(db.String(500))

class Buses(db.Model):
    bus_no = db.Column(db.Integer, primary_key=True)
    bus_type= db.Column(db.String(500))
    departure_time= db.Column(db.String(500))
    arrival_time=db.Column(db.String(400))
    From=db.Column(db.String(400))
    To=db.Column(db.String(600))
    status=db.Column(db.String(500))
@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/ticket',methods=['POST', 'GET'])
@login_required
def tickets():
    try:
        if request.method == "POST":
            username = request.form.get('username')
            name= request.form.get('name')
            bus_no= request.form.get('bus_no')
            seat_no= request.form.get('seat_no')
            time= request.form.get('time')
            date= request.form.get('date')
            source= request.form.get('from')
            dest= request.form.get('to')
            print(username,name,bus_no,seat_no,time,date,source,dest)
            new_book=Ticket(username=username,Name=name,bus_no=bus_no,seat_no=seat_no,time=time,Travel_date=date,From=source,To=dest)
            db.session.add(new_book)
            db.session.commit()
            flash("Boooking succesful","success")
        return render_template('ticket.html')
    except:
        flash("BUS NOT AVAILABLE","PRIMARY")
        return redirect(url_for('buses'))
    
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    try:
        if request.method == "POST":
            username = request.form.get('username')
            password = request.form.get('password')
            print(username,password)
            encpwd = generate_password_hash(password)
            new_user = Info(username=username, password=encpwd)
            db.session.add(new_user)
            db.session.commit()
            flash("Sign up succefull","primary")
            return render_template('login.html')
        return render_template('signup.html')
    except:
        flash("Username already exixts","primary")
        return redirect(url_for('signup'))
@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        print(username,password)
        user=Info.query.filter_by(username=username).first()
        if user and check_password_hash(user.password,password):
            login_user(user)
            #flash("Login Succesful","primary")
            return redirect(url_for('buses'))
        else:
            flash("Login unsuccesful","danger")  
            return render_template('login.html')
    return render_template('login.html')
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout succeful","info")
    return redirect(url_for('login'))

@app.route('/buses')
def buses():
    all_buses= db.session.query(Buses).all()

    return render_template('buses.html',posts=all_buses)
@app.route('/passengers')
@login_required
def passengers():
    user=current_user.username
    if user=="Admin":
        all_passengers= db.session.query(Passengers).all()
        return render_template('passengers.html',posts=all_passengers)
    else:
        flash("You are not the admin,login as the admin","danger")
        return redirect(url_for('login'))

@app.route('/booking')
@login_required
def booking():
        current=current_user.username
        filtered_tickets = db.session.query(Ticket).filter(
        Ticket.username == current).all()
        return render_template('booking.html',posts=filtered_tickets)


@app.route('/test')
def test():
     try:
        # Try querying the Route table to check if the database connection is working
        routes = Info.query.all()
        return 'My database is connected'
     except Exception as e:
        return 'My database is not connected. Error: ' + str(e)
@app.route("/delete/<string:ticket_id>",methods=['POST','GET'])
@login_required
def delete(ticket_id):
    filtered_tickets = db.session.query(Ticket).filter(Ticket.ticket_id==ticket_id).all()
    for ticket in filtered_tickets:
        db.session.delete(ticket)
    db.session.commit()
    return redirect(url_for('booking'))

# @app.route("/edit/<string:ticket_id>",methods=['POST','GET'])
# @login_required
# # Assuming you have the necessary imports:
# # from sqlalchemy import update
# # from flask import render_template, request

# # Assuming you have the necessary imports and Ticket model defined

# def edit(ticket_id):
#     if request.method == "POST":
#         username = request.form.get('username')
#         name = request.form.get('name')
#         bus_no = request.form.get('bus_no')
#         seat_no = request.form.get('seat_no')
#         time = request.form.get('time')
#         date = datetime.strptime(request.form.get('date'), '%Y-%m-%d')
#         source = request.form.get('from')
#         dest = request.form.get('to')
#         # Fetch the existing ticket with the given ticket_id
#         existing_ticket = db.session.query(Ticket).filter_by(ticket_id=ticket_id).first()

#         # If the ticket exists, update its attributes
#         if existing_ticket:
#             existing_ticket.username = username
#             existing_ticket.Name = name
#             existing_ticket.bus_no = bus_no
#             existing_ticket.seat_no = seat_no
#             existing_ticket.time = time
#             existing_ticket.Travel_date = date
#             existing_ticket.From = source
#             existing_ticket.To = dest
#         else:
#             # If the ticket does not exist, create a new Ticket object
#             existing_ticket = Ticket(
#                 ticket_id=ticket_id,
#                 username=username,
#                 Name=name,
#                 bus_no=bus_no,
#                 seat_no=seat_no,
#                 time=time,
#                 Travel_date=date,
#                 From=source,
#                 To=dest
#             )

#         # Merge the ticket with the database session
#         db.session.merge(existing_ticket)
#         db.session.commit()

#         print("Update successful.")

#     return render_template('edit.html')



if __name__ == "__main__":
    app.run(debug=True)
