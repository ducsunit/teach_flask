from flask import Flask

from app.errors import register_error_handlers

from .extensions import db

def create_app():
    app = Flask(__name__)
    
    # config database
    # mysql+pymysql://username:password@host:port/db_name
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/flask_courses'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        from .models import Course
        db.create_all() 

    from .routes import course_bp

    app.register_blueprint(course_bp)

    register_error_handlers(app)
    
    return app