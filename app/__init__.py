from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()
login_manager = LoginManager()





def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@127.0.0.1:3306/carros_e_clientes'
    app.config['SECRET_KEY'] = 'fabricio'

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from .models import Clientes
        from .routes import main, auth, cars, images
        
        @login_manager.user_loader
        def load_user(Clientes_id):
            return Clientes.query.get(int(Clientes_id))


        app.register_blueprint(main.bp)
        app.register_blueprint(auth.bp)
        app.register_blueprint(cars.bp)
        app.register_blueprint(images.bp)
        db.create_all()

    return app

