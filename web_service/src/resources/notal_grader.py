import json

from flask import request, json
from flask_restful import Resource

from graph_grader.src.grader.notal_grader import notal_grader
from web_service.src.utils.checker import allowed_file, check_grade_request
from web_service.src.utils.logz import create_logger
from web_service.src.utils.wrapper import get_response
from http import HTTPStatus
import base64
from func_timeout import func_timeout, FunctionTimedOut


class NotalGrader(Resource):
    def __init__(self):
        self.logger = create_logger()

    def post(self):
        self.logger.info("receiving notal grade request")

        request_data = json.loads(request.data.decode('utf-8'))
        err_req, msg_req, status_code_req = check_grade_request(request_data)
        if err_req:
            return get_response(err=err_req, msg=msg_req, status_code=status_code_req)

        encoded_references_file = request_data['references']
        references_file_names = request_data['referencesFileNames']
        encoded_solution_file = request_data['solution']
        solution_file_name = request_data['solutionFileName']
        time_limit = request_data['timeLimit']

        for name_file in references_file_names + [solution_file_name]:
            if not allowed_file(name_file):
                return get_response(err=True,
                                    msg=f'Request with file name={name_file} is not valid',
                                    status_code=HTTPStatus.BAD_REQUEST)

        src_refs = [base64.b64decode(ref).decode('utf-8') for ref in encoded_references_file]
        src = base64.b64decode(encoded_solution_file).decode('utf-8')

        try:
            self.logger.info("CFG grading started...")
            score = func_timeout(time_limit / 1000, notal_grader, args=(src_refs, src))
            self.logger.info("CFG grading successfully done!")
            return get_response(err=False,
                                msg=f"Grading successfully done!",
                                data={'score': score},
                                status_code=HTTPStatus.ACCEPTED)
        except SyntaxError as e:
            self.logger.error("SyntaxError exception occurred")
            return get_response(err=True, msg=e.msg, status_code=HTTPStatus.OK)
        except FunctionTimedOut:
            self.logger.error("FunctionTimedOut exception occurred")
            return get_response(err=True, msg='time limit exceeded', status_code=HTTPStatus.OK)
        except Exception as e:
            self.logger.error("An error occurred", e)
            return get_response(err=True, msg='An error occurred', status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
