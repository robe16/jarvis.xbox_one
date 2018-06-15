from bottle import HTTPResponse, HTTPError

from common_functions.request_enable_cors import enable_cors
from common_functions.request_log_args import get_request_log_args
from log.log import log_inbound
from resources.global_resources.log_vars import logPass, logException
from resources.global_resources.variables import *
from validation.validation import validate_command


def post_command(request, _xbox):
    #
    args = get_request_log_args(request)
    #
    try:
        #
        data_dict = request.json
        #
        if validate_command(data_dict):
            #
            command = data_dict['command']
            r = _xbox.sendCmd(command)
            #
            if r:
                status = httpStatusSuccess
            else:
                status = httpStatusFailure
        else:
            status = httpStatusBadrequest
        #
        args['result'] = logPass
        args['http_response_code'] = status
        args['description'] = '-'
        log_inbound(**args)
        #
        response = HTTPResponse()
        response.status = status
        enable_cors(response)
        #
        return response
        #
    except Exception as e:
        status = httpStatusServererror
        #
        args['result'] = logException
        args['http_response_code'] = status
        args['description'] = '-'
        args['exception'] = e
        log_inbound(**args)
        #
        raise HTTPError(status)
