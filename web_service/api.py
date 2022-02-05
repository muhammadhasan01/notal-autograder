from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)


class HealthCheck(Resource):
    @staticmethod
    def get():
        return "HEALTHY"


# Actually set up the Api resource routing here
api.add_resource(HealthCheck, '/healthcheck')

if __name__ == '__main__':
    app.run(debug=True)
