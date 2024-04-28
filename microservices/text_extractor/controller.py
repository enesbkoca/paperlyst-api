from flask import Blueprint, jsonify, request
import requests
from service import Microservice1Service

microservice1_controller = Blueprint('microservice1', __name__)
microservice1_service = Microservice1Service()
@microservice1_controller.route('/endpoint', methods=['POST'])
def endpoint_handler():
    file_path = request.json['file_path']

    # Call service method for microservice 1
    result = microservice1_service.process_data(file_path)

    # Send HTTP POST request with the extracted text
    response = requests.post('http://localhost:9021', data=result)

    # Format and return response
    return jsonify(response.text)