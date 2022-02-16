from flask_restful import Resource, reqparse

from cfg_grader.src.grader.notal_grader import notal_grader
from web_service.src.utils.logz import create_logger


class NotalGrader(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('src_answer', type=list[str], required=True, help='Notal source answer required')
    parser.add_argument('src', type=str, required=True, help='Notal src required')

    def __init__(self):
        self.logger = create_logger()

    def post(self, grade_type: str):
        data = NotalGrader.parser.parse_args()
        src, src_answer = data["src"], None
        if grade_type == "single":
            src_answer = [data["src_answer"]]
        elif grade_type == "multiple":
            src_answer = data["src_answer"]
        else:
            return {'error': True, 'message': 'endpoint cannot be found'}, 404
        try:
            self.logger.info("grading notal started...")
            score, total, details = notal_grader(src_answer, src)
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
