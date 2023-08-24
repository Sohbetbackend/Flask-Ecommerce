from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_restful import Api
from flask_msearch import Search
from flask_login import LoginManager
from flask_babel import Babel, lazy_gettext as _l
from flask_moment import Moment
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
api = Api()
search = Search()
babel = Babel()
moment = Moment()
migrate = Migrate()
bcrypt = Bcrypt()

login_manager = LoginManager()
login_manager.login_view='customerLogin'
login_manager.needs_refresh_message_category='danger'
login_manager.login_message = _l(u"Please login first")
photos = UploadSet('photos', IMAGES)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    login_manager.init_app(app)
    db.init_app(app)
    api.init_app(app)
    search.init_app(app)
    babel.init_app(app)
    moment.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    configure_uploads(app, photos)
    patch_request_class(app)

    from shop.products import bp as products_bp
    app.register_blueprint(products_bp)

    from shop.admin import bp as admin_bp
    app.register_blueprint(admin_bp)

    from shop.carts import bp as carts_bp
    app.register_blueprint(carts_bp)

    from shop.customers import bp as customers_bp
    app.register_blueprint(customers_bp)

    from shop.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from shop.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    @app.context_processor
    def inject_conf_var():
        return dict(
            AVAILABLE_LANGUAGE=app.config['LANGUAGES'],
            CURRENT_LANGUAGE=session.get('language', 'en')
        )

    return app


@babel.localeselector
def get_locale():
    try:
        language = session['language']
    except KeyError:
        language = None
    if language:
        return language
    return 'tk'
