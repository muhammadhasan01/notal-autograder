from flask_restful import Resource, reqparse

from cfg_grader.src.grader.notal_grader import notal_grader
from web_service.src.utils.logz import create_logger


class NotalGrader(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('srcAnswers', type=list[str], required=True, help='List of notal source answers required')
    parser.add_argument('src', type=str, required=True, help='Notal src required')

    def __init__(self):
        self.logger = create_logger()

    def post(self):
        data = NotalGrader.parser.parse_args()
        try:
            self.logger.info("grading notal started...")
            score, total, details = notal_grader(data["srcAnswers"], data["src"])
            self.logger.info(f"Received successful grade notal with a score of {score}")
            return {
                       'error': False,
                       'message': 'Grade successful',
                       'score': score,
                       'total': total,
                       'details': details
                   }, 200
        except Exception as e:
            self.logger.error("An error occurred", e)
            return {
                       'error': True,
                       'message': 'An error occurred'
                   }, 500
