# ---------------------imports-----------------#
from flask import Flask, render_template, request, redirect, url_for,jsonify 
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import column_property
from sqlalchemy import Column, Integer, LargeBinary
from fastapi import FastAPI
from fastapi.encoders  import jsonable_encoder

# --------------------------------------#
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:ali12345@localhost/webp'
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)
login_manager = LoginManager(app)

# ---------------------DBTable-----------------#
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User( UserMixin, db.Model):
    __tablename__='User'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    Email = db.Column(db.String(100) , unique = True)
    gender = db.Column(db.String(10))
    role = db.Column(db.String(20))
    password = db.Column(db.Text)
    
    def __init__(self,name,Email,gender,role,password):
        self.name=name
        self.Email=Email    
        self.gender=gender
        self.role=role
        self.password=password


class feed_back(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    motivation = db.Column(db.String(100))
    mostFeature = db.Column(db.String(100))
    opinion = db.Column(db.Text) 
    rate = db.Column(db.Integer)

    def __init__(self , motivation, mostFeature, opinion, rate):
        self.motivation = motivation    
        self.mostFeature = mostFeature
        self.opinion = opinion
        self.rate = rate
    

class addPlaceTo (UserMixin , db.Model ) :
    __tablename__='addPlaceTo'
    placeId = db.Column(db.Integer , primary_key = True)
    placeName = db.Column(db.String(255))
    placeDescription = db.Column(db.String(255))
    location = db.Column(db.String(100))
    maxNumPeop = db.Column(db.Integer)
    maxNumRoom = db.Column(db.Integer)
    placePrice = db.Column(db.Double)
    imgofplace = column_property(db.Column(db.String(255)))
    garage = db.Column(db.Boolean, default=False)
    camera = db.Column(db.Boolean, default=False)
    pool = db.Column(db.Boolean, default=False)
    paw = db.Column(db.Boolean, default=False)
    grill = db.Column(db.Boolean, default=False)
    washer = db.Column(db.Boolean, default=False)
    router = db.Column(db.Boolean, default=False)
    screen = db.Column(db.Boolean, default=False)
    drinks = db.Column(db.Boolean, default=False)

    def __init__ (self, placeName, location, placeDescription, maxNumPeop,maxNumRoom, imgofplace, placePrice, garage, camera, pool, paw, grill, washer, router, screen, drinks):
        self.placeName = placeName
        self.location = location
        self.placeDescription = placeDescription
        self.maxNumPeop = maxNumPeop
        self.maxNumRoom=maxNumRoom
        self.imgofplace = imgofplace
        self.placePrice = placePrice
        self.garage = garage
        self.camera = camera
        self.pool = pool
        self.paw = paw
        self.grill = grill
        self.washer = washer
        self.router = router
        self.screen = screen
        self.drinks = drinks
    def to_dict(self):
        return {
            'placeId': self.placeId,
            'placeName': self.placeName,
            'placeDescription': self.placeDescription,
            'location': self.location,
            'maxNumPeop': self.maxNumPeop,
            'placePrice': self.placePrice,
            'imgofplace': self.imgofplace,
            'garage': self.garage,
            'camera': self.camera,
            'pool': self.pool,
            'paw': self.paw,
            'grill': self.grill,
            'washer': self.washer,
            'router': self.router,
            'screen': self.screen,
            'drinks': self.drinks
        }


class giftCard(db.Model):
    __tablename__='gifcard'
    giftcard_id=db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    dis_code=db.Column(db.String(255),unique=True)
    card = db.Column(db.String(255))
    usable=db.Column(db.Boolean(),default=True)
    user = db.relationship('User', backref=db.backref('giftCard', lazy=True))


class details(db.Model):
    __tablename__ = 'details'
    detail_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    hotel_id = db.Column(db.Integer, db.ForeignKey('addPlaceTo.placeId'))
    
    user = db.relationship('User', backref=db.backref('details', lazy=True))
    hotel = db.relationship('addPlaceTo', backref=db.backref('details', lazy=True))

    def __init__(self, user_id, hotel_id):
        self.user_id = user_id
        self.hotel_id = hotel_id

class Reservation(db.Model):
    __tablename__ = 'reservation'
    resrv_id = db.Column(db.Integer, primary_key=True)
    hotel_id = db.Column(db.Integer, db.ForeignKey('addPlaceTo.placeId'))
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    price = db.Column(db.Float)
    date=db.Column(db.String(255),nullable=True)

    user = db.relationship('User', backref=db.backref('Reservation', lazy=True))
    hotel = db.relationship('addPlaceTo', backref=db.backref('Reservation', lazy=True))

    def __init__(self, hotel_id, user_id, price,date):
        self.hotel_id = hotel_id
        self.user_id = user_id
        self.price = price
        self.date=date

# --------------------------------------#


# ---------------------routs-----------------#

@app.route('/')
def index():
    if current_user.is_authenticated : 
        return render_template("index.html" , user = current_user)
    return render_template("index.html")

# ______________________________

@app.route("/filter")
def filter () :
    if current_user.is_authenticated : 
        return render_template("filter.html" , user = current_user)
    return render_template('filter.html')

# ______________________________

# @app.route("/service",methods=["GET","POST"])
# def service () :
#     if request.method=="POST":
#         name = request.form['name']
#         email = request.form['email']
#         motivation = request.form['motivation']
#         feature = request.form['feature']
#         opinion = request.form.get('opinion', '')
        
#         feedback = Feedback(name=name, email=email,motivation=motivation,feature=feature, opinion=opinion)
#         db.session.add(feedback)
#         db.session.commit()
#         return redirect(url_for('/'))
#     return render_template("service.html")

# ______________________________

@app.route("/newlogin" , methods=['GET', 'POST']) 
def login () :
    if current_user.is_authenticated : 
        return redirect(url_for("index"))
    
    if request.method == "POST" :
        email = request.form['Email']
        password = request.form['password']
        user = User.query.filter_by(Email=email).first()

        if user and check_password_hash(user.password, password) : 
            print(check_password_hash(user.password , password))
            login_user(user)
            return render_template("index.html",user=user)

    return render_template("newLogin.html")

# ______________________________

@app.route('/logout')
@login_required
def logout():
    if User.is_authenticated : 
        logout_user()    
        
    return redirect(url_for('login'))

# ______________________________

@app.route("/detail/<int:hotelId>")
def detail (hotelId) :
    if current_user.is_authenticated : 
        hotel=addPlaceTo.query.get_or_404(hotelId)
        return render_template("Details.html",hotel=hotel)
    return redirect(url_for('login'))

# ______________________________

@app.route("/GiftCard")
def GiftCard () :
    if current_user.is_authenticated :
        return render_template("GiftCard.html")
    return redirect(url_for('login'))

# ______________________________
@app.route('/reddemgiftcard',methods=['GET'])
def reddem():
    if current_user.is_authenticated :
        return render_template("RedeemCard.html")
    return redirect(url_for('index'))
    
# ______________________________
@app.route('/api/reddemgiftcard',methods=['PUT','GET'])
def addGif():
    userId=current_user.id
    g_card=giftCard.query.filter_by(user_id=userId).first()
    if request.method=='PUT':
        g_card.usable=request.json["usable"]
        db.session.commit()
        return  jsonify({"message":"Success"})
    return  (jsonable_encoder(g_card))
# ______________________________
@app.route('/api/giftcard',methods=['POST'])
def addGift():
    user_id = current_user.id
    num_gift_cards = giftCard.query.filter_by(user_id=user_id).count()

    
    if num_gift_cards >= 1:
        return jsonify({"error": "You have reached the maximum limit of gift cards"}), 403

    dis_code = request.json['code'] 
    card = request.json['discount'] 
    newGift=giftCard(user_id=user_id,dis_code=dis_code,card=card)
    db.session.add(newGift)
    db.session.commit()
    return jsonify({"success":"yeahhhhh"})
# ______________________________

@app.route('/api/all_hotels', methods=['GET'])
def all_hotels():
    hotels = addPlaceTo.query.all()
    return jsonable_encoder(hotels)
# ______________________________
@app.route("/api/gethotel/<int:hotelId>")
def getHotel(hotelId):
    hotel=addPlaceTo.query.get_or_404(hotelId) 
    print(hotelId)      
    return jsonable_encoder(hotel)
# ______________________________
@app.route('/api/reserve',methods=['POST'])
def reserve():
    userId=current_user.id
    reservation=Reservation(hotel_id=request.json['hotelId'],user_id=userId,price=request.json['price'],date=request.json['date'])
    db.session.add(reservation)
    db.session.commit()
    return jsonify({"message":"Success"})
# ______________________________
@app.route('/api/getreserve',methods=['GET'])
def getreserv():
    userId=current_user.id
    reservation=Reservation.query.filter_by(user_id=userId).all()
    return jsonable_encoder(reservation)
# ______________________________
@app.route('/api/searchText/<string:text>',methods=['GET'])
def search(text):
    hotels=addPlaceTo.query.filter(addPlaceTo.placeName.ilike(f"%{text}%")).all()
    return jsonable_encoder(hotels)
# ______________________________
@app.route("/addPlace", methods=['GET', 'POST'])
@login_required
def addPlace():
    if current_user.is_authenticated and request.method=='GET': 
        return render_template("addPlace.html" , user = current_user)
    if request.method == "POST":
        placeName1 = request.form['placeNameForm']
        location = request.form['location']
        placeDescription = request.form['placeDescription']
        maxNumPeop = request.form['maxNumPeop']
        maxNumRoom = request.form['maxNumRoom']
        placePrice = request.form['placePrice']
        garage = bool(int(request.form.get('garage', 0)))
        camera = bool(int(request.form.get('camera', 0)))
        pool = bool(int(request.form.get('pool', 0)))
        paw = bool(int(request.form.get('paw', 0)))
        grill = bool(int(request.form.get('grill', 0)))
        washer = bool(int(request.form.get('washer', 0)))
        router = bool(int(request.form.get('router', 0)))
        screen = bool(int(request.form.get('screen', 0)))
        drinks = bool(int(request.form.get('drinks', 0)))

        if 'imgofplace' in request.files:
            img_file = request.files['imgofplace']
            imgName = f"{placeName1}_{placePrice}"
            imgPath = f"./static/img/{imgName}.png"
            img_file.save(imgPath)
        
        check=addPlaceTo.query.filter_by(placeName=placeName1).all()

        if not check :
            newHotel = addPlaceTo(placeName=placeName1, location=location, placeDescription=placeDescription, maxNumPeop=maxNumPeop,maxNumRoom=maxNumRoom, imgofplace=imgPath, placePrice=placePrice, garage=garage, camera=camera, pool=pool, paw=paw, grill=grill, washer=washer, router=router, screen=screen, drinks=drinks)
            db.session.add(newHotel)
            db.session.commit()
            user_id = current_user.id
            detail = details(user_id=user_id, hotel_id=newHotel.placeId)

            db.session.add(detail)
            db.session.commit()
            return redirect(url_for('index'))
        return redirect(url_for('addPlace'))

    return render_template("newLogin.html")

# ______________________________

@app.route("/register", methods=['GET', 'POST'])
def register():
    
    if request.method == "POST" :
        fullName = request.form.get("name")
        Email = request.form.get("email")
        role = request.form.get("accountType")
        password = request.form.get("password")
        gender = request.form.get("gender")
        user = User(name = fullName , Email=Email, gender=gender, role=role, password= generate_password_hash(password))
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('index') )

    return render_template('register.html')


# ______________________________

@app.route("/feedBack" , methods = ['GET' ,'Post'])
def feedBack () :
    if current_user.is_authenticated :
        if request.method == 'POST' :

            Motivation = request.form.get("motivation")
            MostFeature = request.form.get("mostFeature")
            Opinion = request.form.get("opinion")
            feedBack = feed_back(motivation=Motivation, mostFeature=MostFeature, opinion=Opinion, rate=5)
            db.session.add(feedBack)
            db.session.commit()

            return render_template('index.html')
        return render_template("feedBack.html",user=current_user)
    return render_template("newLogin.html")
# ______________________________
@app.route('/terms')
def terms():
    return render_template('terms.html')
# ______________________________
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)