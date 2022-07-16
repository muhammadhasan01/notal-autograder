from flask_restful import Resource

from web_service.src.utils.logz import create_logger
from web_service.src.utils.wrapper import get_response


class Description(Resource):
    def __init__(self):
        self.logger = create_logger()

    def get(self):
        self.logger.info("receiving description endpoint")
        return get_response(err=False, msg='success', data={
            "imageName": "mhasan01/notal-autograder:3.0",
            "displayedName": "Algorithmic Notation Autograder",
            "description": "Algorithmic Notation Autograder using Control Flow Graph (CFG) Similarity."
        })
