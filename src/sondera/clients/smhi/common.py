import json
import requests
from ...exceptions import APIError


def _make_request(api_url, append_404_message=''):
    """ All SMHI Obs API requests are passed through this function """
    api_get_result = requests.get(api_url)

    if api_get_result.status_code == 200:
        return api_get_result

    try:
        api_error = json.loads(api_get_result.content)['error']
    except KeyError:
        api_error = ''

    api_message = api_get_result.reason + api_error

    message = ((api_message + append_404_message)
               if api_get_result.status_code == 404
               else api_message)

    raise APIError(api_get_result.status_code,
                   message)
