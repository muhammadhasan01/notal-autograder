import base64

from flask_restful import Resource
from flask import request, json
from func_timeout import func_timeout, FunctionTimedOut

from cfg_generator.src.api.functions import get_cfg
from cfg_generator.src.api.visualize_cfg import convert_cfg_to_cfg_json
from web_service.src.utils.checker import check_notal_to_cfg_request, allowed_file
from web_service.src.utils.logz import create_logger
from web_service.src.utils.wrapper import get_response
from http import HTTPStatus


class NotalToCFG(Resource):
    def __init__(self):
        self.logger = create_logger()

    def post(self):
        self.logger.info("receiving notal to cfg request")

        request_data = json.loads(request.data.decode('utf-8'))
        err_req, msg_req, status_code_req = check_notal_to_cfg_request(request_data)
        if err_req:
            return get_response(err=err_req, msg=msg_req, status_code=status_code_req)

        encoded_solution_file = request_data['solution']
        solution_file_name = request_data['solutionFileName']
        time_limit = request_data['timeLimit']

        if not allowed_file(solution_file_name):
            return get_response(err=True,
                                msg=f'Request with file name={solution_file_name} is not valid',
                                status_code=HTTPStatus.BAD_REQUEST)

        notal_src = base64.b64decode(encoded_solution_file).decode('utf-8')

        try:
            self.logger.info("Generating Notal to CFG started...")
            cfg = func_timeout(time_limit / 1000, get_cfg, args=(None, notal_src))
            cfg_json = convert_cfg_to_cfg_json(cfg)
            self.logger.info("Successfully generated notal to cfg")
            return get_response(err=False,
                                msg='Successfully generated cfg',
                                data={'cfg': cfg_json, 'src': notal_src},
                                status_code=HTTPStatus.ACCEPTED
                                )
        except FunctionTimedOut:
            self.logger.error("FunctionTimedOut exception occurred")
            return get_response(err=True, msg='time limit exceeded', status_code=HTTPStatus.OK)
        except Exception as e:
            self.logger.error("An error occurred", e)
            return get_response(err=True, msg='An error occurred', status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
