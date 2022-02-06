from flask import Flask
from flask_restful import Api

from web_service.resources.health_check import HealthCheck

app = Flask(__name__)
api = Api(app)

api.add_resource(HealthCheck, '/healthcheck')

if __name__ == '__main__':
    app.run(debug=True)
