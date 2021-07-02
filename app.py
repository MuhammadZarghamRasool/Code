from flask import Flask,render_template,redirect,url_for,session,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import re
from werkzeug import datastructures

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

class community(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post = db.Column(db.String(500), nullable=False)
    post_reply = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default= datetime.utcnow)
    author =db.Column(db.String(20), nullable=False)
    def __repr__(self):
        return '<Post %r>' % self.search_id


@app.route('/', methods=['GET','POST'])
def home():
     if request.method=='POST':
        data={}

        get_location=request.form['local'] 
        get_city=request.form['city']
        get_type=request.form['type']
        get_category=request.form['category']
       
        
        if get_category== "Category" and get_city== "City" and get_type== "Type":
            print("YEsssssss ")
            data=tests_rental.query.filter_by(location=get_location).all()
        
        elif get_category!= "Category" and get_city=="City" and get_type=="Type":
            data=tests_rental.query.filter_by(location=get_location, category=get_category).all()
        
        elif get_category=="Category" and get_city!="City" and get_type=="Type":
            data=tests_rental.query.filter_by(location=get_location, city=get_city).all()
        
        elif get_category=="Category" and get_city=="City" and get_type!="Type":
            data=tests_rental.query.filter_by(location=get_location, type=get_type).all()
        
        elif get_category!="Category" and get_city!="City" and get_type=="Type":
            data=tests_rental.query.filter_by(location=get_location, category=get_category, city=get_city).all()
        
        elif get_category!="Category" and get_city=="City" and get_type!="Type":
            data=tests_rental.query.filter_by(location=get_location, category=get_category, type=get_type).all()
        
        elif get_category=="Category" and get_city!="City" and get_type!="Type":
            data=tests_rental.query.filter_by(location=get_location, city=get_city, type=get_type).all()
        
        elif get_category!="Category" and get_city!="City" and get_type!="Type":
            data=tests_rental.query.filter_by(location=get_location, category=get_category, city=get_city, type=get_type).all()

        print(data)
        return render_template('properties.html', data=data)
     
     else:
         return render_template('index.html', name=session["user"])

@app.route('/properties', methods=['GET','POST'])
def properties():
            return redirect('/properties.html')


@app.route('/properties-detail/<int:id>', methods=['GET','POST'])
def Properties_Details(id):
    if request.method=='POST':
        get_id=tests_rental.query.filter_by(id=id)

    return render_template('/properties-detail.html', data=get_id)


@app.route('/pricesuggestion', methods=['POST','GET'])
def price():
    data={}
    counter=0;
    total_price=0.0
    crore=0.0
    lakh=0.0
    avg_price=0.0
    if request.method=='POST':
        get_location=request.form['local']
        get_city=request.form['city']
        get_area=request.form['area']
        get_category=request.form['category']
        get_type=request.form['type']
        get_area_unit=request.form['area_unit']

        if get_city!= "City" and get_type!= "Type" and get_category!="Category" and get_area_unit!="Area_Unit":                   
            print("YESSSS")
            data=tests_rental.query.filter_by(location=get_location, area=get_area+" "+get_area_unit,category=get_category,type=get_type,city=get_city ).all()
            print(data)
            
            for rows in data:
                # total_price=total_price+((int) rows.price)
                print(rows.price)
                if "Crore" in rows.price:
                    crore=crore+float(re.search(r'\d+', rows.price).group())
                if "Lakh" in rows.price:
                    lakh=lakh+float(re.search(r'\d+', rows.price).group())
                # int(re.search(r'\d+', rows.price).group())
                counter+=1
            total_crore=crore*10000000
            total_lakh=lakh*100000
            total_price=total_crore+total_lakh
            avg_price=0.0
            if counter==0:
                render_template('Price.html', price=avg_price)
            else:
                avg_price=total_price/counter
            print(data)
        
        else:"Please select all the input fields"
    
    
    return render_template('Price.html', price=avg_price)

@app.route('/communityforum', methods=['POST','GET'])
def community_forum():
    
    if "id" in session:
        posts=community.query.order_by("id").all()
        if request.method=='POST':
            get_post=request.form['posts']
            get_post_reply=""
            ad_post=community(post=get_post, author=session["user"], post_reply=get_post_reply)
        try:
            db.session.add(ad_post)
            db.session.commit()
            return redirect('/communityforum')
        except:
            "There is an issue in posting your query" 
            
    return render_template('community.html',posts=posts )


@app.route('/delete/<int:id>')
def delete(id):
    post_to_delete = community.query.get_or_404(id)
    try:
        db.session.delete(post_to_delete)
        db.session.commit()
        return redirect('/communityforum')
    except: 
        return "There is a problem in deleting a query"


@app.route('/reply/<int:id>')
def reply(id):
    if request.method=='POST':
        get_reply=request.form['posts']
        ad_reply=community.query.filter_by(id).first()
        ad_reply.post_reply=get_reply
        db.session.commit()
    return redirect('/communityforum')




@app.route('/login', methods=['POST','GET'] )
def login():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        account=user_account.query.filter_by(user_email=email,user_password=password).first()
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

@app.route('/logout')
def logout():
    if "user" in session and "id" in session:
        session.pop("user",None)
        session.pop("id",None)
        return redirect(url_for("index"))
   

if __name__=="__main__":
    app.run(debug=True)
