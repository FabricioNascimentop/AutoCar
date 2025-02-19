from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv # type: ignore
import os

load_dotenv()
USER = os.getenv("user")
PASSWORD = os.getenv("password")
PASSWORD = PASSWORD.replace('[','').replace(']','')
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")
db = SQLAlchemy()
login_manager = LoginManager()





def create_app():
    app = Flask(__name__)
    DATABASE_URI = f'postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require'
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI 
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

app = create_app()
if __name__ == "__main__":
    app.run(debug=True)
