from flask_restful import Resource

from web_service.src.utils.logz import create_logger


class HealthCheck(Resource):
    def __init__(self):
        self.logger = create_logger()

    def get(self):
        self.logger.info("receiving health check endpoint")
        return {'error': False, 'message': 'healthy'}, 200
