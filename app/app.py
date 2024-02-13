from flask import Flask, jsonify, request
from prometheus_flask_exporter import PrometheusMetrics
from database import db
from models import Item
from redis import Redis
import logging
from logging.handlers import RotatingFileHandler

def configure_logging(app):
    if not app.debug:
        # Set up a file handler
        file_handler = RotatingFileHandler('/var/log/flask_app.log', maxBytes=10240, backupCount=10)
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Application startup')


def create_app():
    app = Flask(__name__)
    metrics = PrometheusMetrics(app, path='/metrics')
    configure_logging(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://newuser:userpassword@mysql/db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.logger.error('Test error message')

    db.init_app(app)

    with app.app_context():
        # Initialize the database (create tables if they don't exist)
        db.create_all()

    redis = Redis(host='redis', port=6379)  # Update this if necessary

    @app.route('/item/<string:name>', methods=['GET'])
    def get_item(name):
        cached_item = redis.get(name)
        if cached_item:
            return jsonify({'name': name, 'cached': True})

        item = Item.query.filter_by(name=name).first()
        if item:
            redis.set(name, str(item.id))
            return jsonify({'name': item.name, 'cached': False})

        return jsonify({'message': 'Item not found'}), 404

    @app.route('/item', methods=['POST'])
    def add_item():
        data = request.get_json()
        item = Item(name=data['name'])
        db.session.add(item)
        try:
            db.session.commit()
            return jsonify({'name': item.name}), 201
        except Exception as e:
            db.session.rollback()
            app.logger.error('Failed to add item: %s', str(e), exc_info=False)
            return jsonify({'error': str(e)}), 500

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5001)
