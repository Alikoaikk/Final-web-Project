from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from fastapi.encoders import jsonable_encoder
from .models import db, User, FeedBack, AddPlaceTo, GiftCard, Details, Reservation

bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    if current_user.is_authenticated:
        return render_template("index.html", user=current_user)
    return render_template("index.html")


@bp.route("/filter")
def filter():
    if current_user.is_authenticated:
        return render_template("filter.html", user=current_user)
    return render_template('filter.html')


@bp.route("/newlogin", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("routes.index"))

    if request.method == "POST":
        email = request.form['Email']
        password = request.form['password']
        user = User.query.filter_by(Email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return render_template("index.html", user=user)

    return render_template("newLogin.html")


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes.login'))


@bp.route("/detail/<int:hotelId>")
def detail(hotelId):
    if current_user.is_authenticated:
        hotel = AddPlaceTo.query.get_or_404(hotelId)
        return render_template("Details.html", hotel=hotel)
    return redirect(url_for('routes.login'))


@bp.route("/GiftCard")
def GiftCard():
    if current_user.is_authenticated:
        return render_template("GiftCard.html")
    return redirect(url_for('routes.login'))


@bp.route('/reddemgiftcard', methods=['GET'])
def reddem():
    if current_user.is_authenticated:
        return render_template("RedeemCard.html")
    return redirect(url_for('routes.index'))


@bp.route('/api/reddemgiftcard', methods=['PUT', 'GET'])
def addGif():
    userId = current_user.id
    g_card = GiftCard.query.filter_by(user_id=userId).first()
    if request.method == 'PUT':
        g_card.usable = request.json["usable"]
        db.session.commit()
        return jsonify({"message": "Success"})
    return jsonable_encoder(g_card)


@bp.route('/api/giftcard', methods=['POST'])
def addGift():
    user_id = current_user.id
    num_gift_cards = GiftCard.query.filter_by(user_id=user_id).count()

    if num_gift_cards >= 1:
        return jsonify({"error": "You have reached the maximum limit of gift cards"}), 403

    dis_code = request.json['code']
    card = request.json['discount']
    newGift = GiftCard(user_id=user_id, dis_code=dis_code, card=card)
    db.session.add(newGift)
    db.session.commit()
    return jsonify({"success": "yeahhhhh"})


@bp.route('/api/all_hotels', methods=['GET'])
def all_hotels():
    hotels = AddPlaceTo.query.all()
    return jsonable_encoder(hotels)


@bp.route("/api/gethotel/<int:hotelId>")
def getHotel(hotelId):
    hotel = AddPlaceTo.query.get_or_404(hotelId)
    return jsonable_encoder(hotel)


@bp.route('/api/reserve', methods=['POST'])
def reserve():
    userId = current_user.id
    reservation = Reservation(hotel_id=request.json['hotelId'], user_id=userId, price=request.json['price'], date=request.json['date'])
    db.session.add(reservation)
    db.session.commit()
    return jsonify({"message": "Success"})


@bp.route('/api/getreserve', methods=['GET'])
def getreserv():
    userId = current_user.id
    reservation = Reservation.query.filter_by(user_id=userId).all()
    return jsonable_encoder(reservation)


@bp.route('/api/searchText/<string:text>', methods=['GET'])
def search(text):
    hotels = AddPlaceTo.query.filter(AddPlaceTo.placeName.ilike(f"%{text}%")).all()
    return jsonable_encoder(hotels)


@bp.route("/addPlace", methods=['GET', 'POST'])
@login_required
def addPlace():
    if current_user.is_authenticated and request.method == 'GET':
        return render_template("addPlace.html", user=current_user)
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

        check = AddPlaceTo.query.filter_by(placeName=placeName1).all()

        if not check:
            newHotel = AddPlaceTo(placeName=placeName1, location=location, placeDescription=placeDescription, maxNumPeop=maxNumPeop, maxNumRoom=maxNumRoom, imgofplace=imgPath, placePrice=placePrice, garage=garage, camera=camera, pool=pool, paw=paw, grill=grill, washer=washer, router=router, screen=screen, drinks=drinks)
            db.session.add(newHotel)
            db.session.commit()
            user_id = current_user.id
            detail = Details(user_id=user_id, hotel_id=newHotel.placeId)

            db.session.add(detail)
            db.session.commit()
            return redirect(url_for('routes.index'))
        return redirect(url_for('routes.addPlace'))

    return render_template("newLogin.html")


@bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        fullName = request.form.get("name")
        Email = request.form.get("email")
        role = request.form.get("accountType")
        password = request.form.get("password")
        gender = request.form.get("gender")
        user = User(name=fullName, Email=Email, gender=gender, role=role, password= generate_password_hash(password))
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('routes.index'))

    return render_template('register.html')


@bp.route("/feedBack", methods=['GET', 'POST'])
def feedBack():
    if current_user.is_authenticated:
        if request.method == 'POST':
            Motivation = request.form.get("motivation")
            MostFeature = request.form.get("mostFeature")
            Opinion = request.form.get("opinion")
            feedBack = FeedBack(motivation=Motivation, mostFeature=MostFeature, opinion=Opinion, rate=5)
            db.session.add(feedBack)
            db.session.commit()

            return render_template('index.html')
        return render_template("feedBack.html", user=current_user)
    return render_template("newLogin.html")


@bp.route('/terms')
def terms():
    return render_template('terms.html')
