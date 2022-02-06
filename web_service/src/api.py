from flask import Flask
from flask_restful import Api

from web_service.src.resources.health_check import HealthCheck
from web_service.src.resources.notal_grader import NotalGrader

app = Flask(__name__)
api = Api(app)

api.add_resource(HealthCheck, '/healthcheck')
api.add_resource(NotalGrader, '/grade')

if __name__ == '__main__':
    app.run(debug=True)
