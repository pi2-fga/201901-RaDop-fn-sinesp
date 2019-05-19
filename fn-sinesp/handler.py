import json
import warnings
from sinesp_client import SinespClient

# Ignore warnings due implementation of SinespCliente
warnings.simplefilter('ignore')

# Define the type of call of the function
SINESP_CALL = 'sinesp-call'

# Globa SINESP Client variable
sc = SinespClient()


def error_message(message):
    status_code = 500
    response = {'status_code':  status_code, 'response_message': message}
    return response


def get_plate_status(plate):
    try:
        result = sc.search(plate)
        return_code = result['return_code']
        if int(return_code) != 0:
            return_message = result['return_message']
            raise Exception(f'Error while trying to get plate status. '
                            f'Response message from SINESP: {return_message}')
    except Exception as err:
        msg = (f'Unknown error while trying to get plate status. Traceback'
               f': {err}')
        raise Exception(msg)
    else:
        return result


def handle(req):
    """
    Handle calls with car plates to verify the car status within the SINESP
    database (brazilian car plates)
    Args:
        req (str): request body
    """
    try:
        package = json.loads(req)
        # TODO: send received package to audit DB
        request_type = package['type']
        request_payload = package['payload']
        plate = request_payload['plate']

        if request_type != SINESP_CALL:
            msg = 'Error!! The message header indicates other function call.' \
                  'Verify if the correct service was called.'
        if not plate:
            msg = 'Error trying to get the SINESP plate!' \
                  'Verify service to correct error'
            return json.dumps(error_message(msg))
        result = get_plate_status(plate)
    except Exception as err:
        msg = f'Unknown error while trying to execute the SINESP service' \
              f'Verify service to correct error. Traceback: {err}'
        return json.dumps(error_message(msg))
    else:
        return json.dumps(
            {
                'status_code': 200,
                'response': result
            },
            ensure_ascii=False)
