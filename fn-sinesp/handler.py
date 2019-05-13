import json
import warnings
from sinesp_client import SinespClient

warnings.simplefilter('ignore')

SINESP_CALL = 'sinesp-call'


def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """
    try:
        sc = SinespClient()
        package = json.loads(req)
        request_type = package['type']
        request_payload = package['payload']
        plate = request_payload['plate']

        if request_type != SINESP_CALL:
            status_code = 500
            msg = 'Error!! The message header indicates other function call.' \
                  'Verify if the correct service was called.'
            response = {'status_code': status_code, 'response_message': msg}
            return json.dumps(response)
        if not plate:
            status_code = 500
            msg = 'Error trying to get the SINESP plate!' \
                  'Verify service to correct error'
            response = {'status_code': status_code, 'response_message': msg}
            return json.dumps(response)
        result = sc.search(plate)
    except Exception as e:
        status_code = 500
        msg = f'Unknown error while trying to execute the SINESP service' \
              f'Verify service to correct error. Traceback: {e}'
        response = {'status_code': status_code, 'response_message': msg}
        return json.dumps(response)
    else:
        return json.dumps(
            {'status_code': 200, 'response': result},
            ensure_ascii=False
            )
