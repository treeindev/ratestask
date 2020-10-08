from flask import Blueprint, jsonify, request
from services.request_validator import RequestValidatorService
from services.rates import RatesService
import constants

api = Blueprint("api_ratestask", __name__)
validator = RequestValidatorService()
rates = RatesService()

@api.route('/rates', methods=['GET'])
def get_rate():
    params = validator.validate_query_params(request.args)
    if not params:
        return invalid_request('', constants.MESSAGE_INVALID_QUERIES)
    try:
        return jsonify(rates.get_rate(False, *params))
    except:
        return invalid_request('', constants.MESSAGE_INTERNAL_ERROR, 500)

@api.route('/rates_null', methods=['GET'])
def get_rate_null():
    params = validator.validate_query_params(request.args)
    if not params:
        return invalid_request('', constants.MESSAGE_INVALID_QUERIES)
    try:
        return jsonify(rates.get_rate(True, *params))
    except:
        return invalid_request('', constants.MESSAGE_INTERNAL_ERROR, 500)

@api.route('/price', methods=['POST'])
def create_price():
    params = request.get_json()
    if 'currency' not in params:
        params['currency'] = constants.DEFAULT_CURRENCY
    params = validator.validate_body_params(params)

    if not params:
        return invalid_request('', constants.MESSAGE_INVALID_QUERIES)
    try:
        rates.create_rate(*params)
        return jsonify({"Message": constants.MESSAGE_VALID_INSERT}), 201
    except:
        return invalid_request('', constants.MESSAGE_INTERNAL_ERROR, 500)

@api.route('/<path>', methods=['GET', 'POST'])
def invalid_request(path, message=constants.MESSAGE_INVALID_ENDPOINT, code=400):
    return jsonify({"Error": message}), code