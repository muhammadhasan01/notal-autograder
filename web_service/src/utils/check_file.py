from werkzeug.datastructures import FileStorage

from common.src.classes.constants import Constants


def allowed_file(filename: str):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Constants.ALLOWED_EXTENSIONS


def check_file(file: FileStorage):
    if file.filename == '':
        return True, 'Filename cannot be blank'
    if file and not allowed_file(file.filename):
        return True, 'Extension file not supported'
    return False, ''
