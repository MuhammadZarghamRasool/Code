from flask import Flask,render_template,redirect,url_for,session,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///zameen_rental.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
app.secret_key="pakistan"
db=SQLAlchemy(app)

class tests_rental(db.Model):
    image=db.Column('image', db.String(150), nullable=False)
    tittle=db.Column('tittle', db.String(150), nullable=False)
    price=db.Column('price', db.String(150), nullable=False)
    bed=db.Column('bed', db.String(150), nullable=False)
    area=db.Column('area', db.String(150), nullable=False)
    location=db.Column('location', db.String(150), nullable=False)
    city=db.Column('city', db.String(150), nullable=False)
    type=db.Column('type', db.String(150), nullable=False)
    category=db.Column('category', db.String(150), nullable=False)
    id=db.Column('id', db.Integer, primary_key= True, nullable=False)

class user_account(db.Model):
    user_id=db.Column(db.Integer, primary_key=True)
    user_name=db.Column(db.String(150), nullable=False)
    user_email=db.Column(db.String(150), nullable=False, unique=True)
    user_password=db.Column(db.String(150), nullable=False)
    def __repr__(self):
        return '<user_row %r>' % self.search_id

# class comm(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     post = db.Column(db.String(500), nullable=False)
#     post_reply = db.Column(db.String(500), nullable=False)
#     date_created = db.Column(db.DateTime, default= datetime.utcnow)
#     def __repr__(self):
#         return '<Task %r>' % self.search_id


@app.route('/', methods=['GET','POST'])
def home():
     if request.method=='POST':
        data={}
        location=request.form['local'] 
        city=request.form['city']
        type=request.form['type']
        category=request.form['category']
        print(location)
        print(city)
        print(type)
        print(category)
        data=tests_rental.query.filter_by(location="B-17, Islamabad").all()
        if category== 0 and city==0 and type== 0:
            print("YEsssssss ")
            data=tests_rental.query.filter_by(location=location).all()
        
        elif category!= "Category" and city=="City" and type=="Type":
            data=tests_rental.query.filter_by(location=location, category=category).all()
        
        elif category=="Category" and city!="City" and type=="Type":
            data=tests_rental.query.filter_by(location=location, city=city).all()
        
        elif category=="Category" and city=="City" and type!="Type":
            data=tests_rental.query.filter_by(location=location, type=type).all
        
        elif category!="Category" and city!="City" and type=="Type":
            data=tests_rental.query.filter_by(location=location, category=category, city=city).all()
        
        elif category!="Category" and city=="City" and type!="Type":
            data=tests_rental.query.filter_by(location=location, category=category, type=type).all()
        
        elif category=="Category" and city!="City" and type!="Type":
            data=tests_rental.query.filter_by(location=location, city=city, type=type).all()
        
        elif category!="Category" and city!="City" and type!="Type":
            data=tests_rental.query.filter_by(location=location, category=category, city=city, type=type).all()

        print(data)
        return render_template('properties.html', data=data)
     
     else:
         return render_template('index.html')

@app.route('/properties', methods=['GET','POST'])
def properties():
            return redirect('/properties.html')


# @app.route('/properties-detail')
# def Properties_Details():
#         print("JJJJJJJJJJJJJJ")
#         if request.method=='POST':
#             id=request.form['id'] 
#             #City=request.form['City']
        
#             print(id)
        
#             data=tests_rental.query.filter_by(id=id).all()
#             print(data)
#             return render_template('properties-detail.html', data=data)
#         else:
#             return render_template('properties-detail.html')


@app.route('/login', methods=['POST','GET'] )
def login():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        account=user_account.query.filter_by(user_email=email,
        user_password=password).first()
        if account:
            session["user"]=account.user_name
            session["id"]=account.user_id
            return redirect('/')
    else:
        return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def singup():
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        password=request.form['password']
        add_user=user_account(user_name=name,user_email=email,user_password=password)
        try:
            db.session.add(add_user)
            db.session.commit()
            return redirect('/login')
        except:
            return 'Account already exists.'
    else:
        return render_template('signup.html')
   


if __name__=="__main__":
    app.run(debug=True)
