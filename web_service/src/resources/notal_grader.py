from flask import request
from flask_restful import Resource

from graph_grader.src.grader.notal_grader import notal_grader
from web_service.src.utils.check_file import check_file
from web_service.src.utils.logz import create_logger
from web_service.src.utils.wrapper import get_response
from http import HTTPStatus


class NotalGrader(Resource):
    def __init__(self):
        self.logger = create_logger()

    def post(self):
        if 'src_refs' not in request.files:
            return get_response(err=True, msg='Source notal reference required', status_code=HTTPStatus.BAD_REQUEST)
        if 'src' not in request.files:
            return get_response(err=True, msg='Source notal submission required', status_code=HTTPStatus.BAD_REQUEST)

        notal_files_ref = request.files.getlist("src_refs")
        notal_file_src = request.files["src"]

        files = notal_files_ref + [notal_file_src]
        for file in files:
            err_file, msg_file = check_file(file)
            if err_file:
                return get_response(err=err_file, msg=msg_file, status_code=HTTPStatus.BAD_REQUEST)

        src_refs = [src.read().decode("UTF-8") for src in notal_files_ref]
        src = notal_file_src.read().decode("UTF-8")
        try:
            self.logger.info("CFG grading started...")
            score, total, details = notal_grader(src_refs, src)
            self.logger.info("CFG grading successfully done!")
            return get_response(err=False,
                                msg=f"Grading successfully done!",
                                data={'score': score, 'total': total, 'details': details},
                                status_code=HTTPStatus.ACCEPTED)
        except Exception as e:
            self.logger.error("An error occurred", e)
            return get_response(err=True, msg='An error occurred', status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
