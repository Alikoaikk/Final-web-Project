from flask import Flask
from flask_login import LoginManager
from models import db, User
from routes import bp as routes_bp

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:ali12345@localhost/webp'
app.config['SECRET_KEY'] = 'your_secret_key'

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'routes.login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


app.register_blueprint(routes_bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)