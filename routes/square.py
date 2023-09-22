import json
import logging

from flask import request

from routes import app

from routes.lazydeveloper import getNextProbableWords

logger = logging.getLogger(__name__)

@app.route('/lazy-developer', methods=['POST'])
def hello():
    data = request.get_json()
    logging.info("Input :{}".format(data))
    input_value = data.get("classes")
    statement = data.get("statements")
    result = getNextProbableWords(input_value, statement)
    return result