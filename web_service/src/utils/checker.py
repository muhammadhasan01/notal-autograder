from http import HTTPStatus

from flask import Request
from werkzeug.datastructures import FileStorage

from intermediate.src.classes.constants import Constants


def allowed_file(filename: str):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Constants.ALLOWED_EXTENSIONS


def check_file(file: FileStorage):
    if file.filename == '':
        return True, 'Filename cannot be blank'
    if file and not allowed_file(file.filename):
        return True, 'Extension file not supported'
    return False, ''


def check_grade_request(request: Request):
    request_data = request.get_json()

    # check request data is valid
    mandatory_attributes = ['references', 'referencesFileNames', 'solution', 'solutionFileName', 'timeLimit']
    if not request_data or not all(key in request_data for key in mandatory_attributes):
        return (
            True,
            "invalid request body",
            HTTPStatus.BAD_REQUEST
        )
    if not isinstance(request_data['references'], list):
        return (
            True,
            "references must be a list of string",
            HTTPStatus.BAD_REQUEST
        )
    if not isinstance(request_data['referencesFileNames'], list):
        return (
            True,
            "referencesFileNames must be a list of string",
            HTTPStatus.BAD_REQUEST
        )
    if not isinstance(request_data['solution'], str):
        return (
            True,
            "solution must be a string",
            HTTPStatus.BAD_REQUEST
        )
    if not isinstance(request_data['solutionFileName'], str):
        return (
            True,
            "solutionFileName must be a string",
            HTTPStatus.BAD_REQUEST
        )
    if not isinstance(request_data['timeLimit'], int):
        return (
            True,
            "timeLimit must be an integer",
            HTTPStatus.BAD_REQUEST
        )
