from flask import Flask
from flask_restful import Api

from web_service.src.resources.health_check import HealthCheck
from web_service.src.resources.notal_grader import NotalGrader
from web_service.src.resources.notal_to_cfg import NotalToCFG

app = Flask(__name__)
api = Api(app)

api.add_resource(HealthCheck, '/healthcheck')
api.add_resource(NotalToCFG, '/notal-to-cfg')
api.add_resource(NotalGrader, '/grade')

if __name__ == '__main__':
    app.run(host="0.0.0.0")
