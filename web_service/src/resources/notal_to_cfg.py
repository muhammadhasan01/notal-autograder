from flask_restful import Resource
from flask import request

from notal_to_cfg_generator.src.api.functions import get_cfg
from notal_to_cfg_generator.src.api.visualize_cfg import convert_cfg_to_cfg_json
from web_service.src.utils.check_file import check_file
from web_service.src.utils.logz import create_logger
from web_service.src.utils.wrapper import get_response
from http import HTTPStatus


class NotalToCFG(Resource):
    def __init__(self):
        self.logger = create_logger()

    def post(self):
        if 'src' not in request.files:
            return get_response(err=True, msg='Source notal required', status_code=HTTPStatus.BAD_REQUEST)

        notal_file = request.files["src"]
        err_file, msg_file = check_file(notal_file)
        if err_file:
            return get_response(err=err_file, msg=msg_file, status_code=HTTPStatus.BAD_REQUEST)

        try:
            notal_src = notal_file.read().decode("UTF-8")
            self.logger.info("Generating Notal to CFG started...")
            cfg = get_cfg(None, notal_src)
            cfg_json = convert_cfg_to_cfg_json(cfg)
            self.logger.info("Successfully generated notal to cfg")
            return get_response(err=False,
                                msg='Successfully generated cfg',
                                data={'cfg': cfg_json, 'src': notal_src},
                                status_code=HTTPStatus.ACCEPTED
                                )
        except Exception as e:
            self.logger.error("An error occurred", e)
            return get_response(err=True, msg='An error occurred', status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
