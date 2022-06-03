from http import HTTPStatus

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


def check_grade_request(request_data):
    mandatory_attributes = ['references', 'referencesFileNames', 'solution', 'solutionFileName', 'timeLimit']
    error_message = None
    if not request_data or not all(key in request_data for key in mandatory_attributes):
        error_message = "Invalid request body"
    elif not isinstance(request_data['references'], list):
        error_message = "references must be a list of string"
    elif not isinstance(request_data['referencesFileNames'], list):
        error_message = "referencesFileNames must be a list of string"
    elif not isinstance(request_data['solution'], str):
        error_message = "solution must be a string"
    elif not isinstance(request_data['solutionFileName'], str):
        error_message = "solutionFileName must be a string"
    elif not isinstance(request_data['timeLimit'], int):
        error_message = "timeLimit must be an integer"
    if error_message is None:
        return False, error_message, HTTPStatus.ACCEPTED
    return True, error_message, HTTPStatus.BAD_REQUEST


def check_notal_to_cfg_request(request_data):
    mandatory_attributes = ['solution', 'solutionFileName', 'timeLimit']
    error_message = None
    if not request_data or not all(key in request_data for key in mandatory_attributes):
        error_message = "Invalid request body"
    elif not isinstance(request_data['solution'], str):
        error_message = "solution must be a string"
    elif not isinstance(request_data['solutionFileName'], str):
        error_message = "solutionFileName must be a string"
    elif not isinstance(request_data['timeLimit'], int):
        error_message = "timeLimit must be an integer"
    if error_message is None:
        return False, error_message, HTTPStatus.ACCEPTED
    return True, error_message, HTTPStatus.BAD_REQUEST
