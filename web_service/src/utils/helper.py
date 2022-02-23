from common.src.classes.constants import Constants


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Constants.ALLOWED_EXTENSIONS
