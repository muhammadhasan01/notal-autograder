from flask_restful import Resource
from flask import request

from notal_to_cfg_generator.src.api.functions import get_cfg
from notal_to_cfg_generator.src.api.visualize_cfg import convert_cfg_to_cfg_json
from web_service.src.utils.helper import allowed_file
from web_service.src.utils.logz import create_logger
from web_service.src.utils.wrapper import get_response


class NotalToCFG(Resource):
    def __init__(self):
        self.logger = create_logger()

    def post(self):
        if 'src' not in request.files:
            return get_response(err=True, msg='Source notal required', status_code=400)

        notal_file = request.files["src"]
        if notal_file.filename == '':
            return get_response(err=True, msg='Filename cannot be blank', status_code=400)

        if notal_file and not allowed_file(notal_file.filename):
            return get_response(err=True, msg='Extension file not supported', status_code=400)

        try:
            notal_src = notal_file.read().decode("UTF-8")
            self.logger.info("Generating Notal to CFG started...")
            cfg = get_cfg(None, notal_src)
            cfg_json = convert_cfg_to_cfg_json(cfg)
            self.logger.info("Successfully generated notal to cfg")
            return get_response(err=False, msg='Successfully generated cfg', additional={'cfg': cfg_json})
        except Exception as e:
            self.logger.error("An error occurred", e)
            return get_response(err=True, msg='An error occurred', status_code=500)
