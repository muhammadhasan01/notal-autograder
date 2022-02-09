from flask_restful import Resource, reqparse

from notal_to_cfg_generator.src.api.functions import get_cfg
from notal_to_cfg_generator.src.api.visualize_cfg import convert_cfg_to_cfg_json
from web_service.src.utils.logz import create_logger


class NotalToCFG(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('src', type=str, required=True, help='Notal src required')

    def __init__(self):
        self.logger = create_logger()

    def post(self):
        data = NotalToCFG.parser.parse_args()
        try:
            self.logger.info("Starting generator notal to cfg")
            cfg = get_cfg(None, data["src"])
            cfg_json = convert_cfg_to_cfg_json(cfg)
            self.logger.info("Successfully generated notal to cfg")
            return {
                "error": False,
                "message": "CFG successfully generated",
                "cfg": cfg_json
            }
        except Exception as e:
            self.logger.error("An error occurred", e)
            return {
                       'error': True,
                       'message': 'An error occurred'
                   }, 500
