from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.orm import column_property
from sqlalchemy import Column

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    Email = db.Column(db.String(100), unique=True)
    gender = db.Column(db.String(10))
    role = db.Column(db.String(20))
    password = db.Column(db.Text)

    def _init_(self, name, Email, gender, role, password):
        self.name = name
        self.Email = Email
        self.gender = gender
        self.role = role
        self.password = password


class FeedBack(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    motivation = db.Column(db.String(100))
    mostFeature = db.Column(db.String(100))
    opinion = db.Column(db.Text)
    rate = db.Column(db.Integer)

    def _init_(self, motivation, mostFeature, opinion, rate):
        self.motivation = motivation
        self.mostFeature = mostFeature
        self.opinion = opinion
        self.rate = rate


class AddPlaceTo(UserMixin, db.Model):
    __tablename__ = 'addPlaceTo'
    placeId = db.Column(db.Integer, primary_key=True)
    placeName = db.Column(db.String(255))
    placeDescription = db.Column(db.String(255))
    location = db.Column(db.String(100))
    maxNumPeop = db.Column(db.Integer)
    maxNumRoom = db.Column(db.Integer)
    placePrice = db.Column(db.Float)
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

    def _init_(self, placeName, location, placeDescription, maxNumPeop, maxNumRoom, imgofplace, placePrice, garage, camera, pool, paw, grill, washer, router, screen, drinks):
        self.placeName = placeName
        self.location = location
        self.placeDescription = placeDescription
        self.maxNumPeop = maxNumPeop
        self.maxNumRoom = maxNumRoom
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


class GiftCard(db.Model):
    __tablename__ = 'gifcard'
    giftcard_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    dis_code = db.Column(db.String(255), unique=True)
    card = db.Column(db.String(255))
    usable = db.Column(db.Boolean(), default=True)
    user = db.relationship('User', backref=db.backref('giftCard', lazy=True))


class Details(db.Model):
    __tablename__ = 'details'
    detail_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    hotel_id = db.Column(db.Integer, db.ForeignKey('addPlaceTo.placeId'))

    user = db.relationship('User', backref=db.backref('details', lazy=True))
    hotel = db.relationship('addPlaceTo', backref=db.backref('details', lazy=True))

    def _init_(self, user_id, hotel_id):
        self.user_id = user_id
        self.hotel_id = hotel_id


class Reservation(db.Model):
    __tablename__ = 'reservation'
    resrv_id = db.Column(db.Integer, primary_key=True)
    hotel_id = db.Column(db.Integer, db.ForeignKey('addPlaceTo.placeId'))
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    price = db.Column(db.Float)
    date = db.Column(db.String(255), nullable=True)

    user = db.relationship('User', backref=db.backref('Reservation', lazy=True))
    hotel = db.relationship('addPlaceTo', backref=db.backref('Reservation', lazy=True))

    def _init_(self, hotel_id, user_id, price, date):
        self.hotel_id = hotel_id
        self.user_id = user_id
        self.price = price
        self.date = date