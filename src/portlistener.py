from bottle import request, run, route, get, post

from config.config import get_cfg_port
from common_functions.request_enable_cors import response_options
from resources.lang.enGB.logs import *
from resources.global_resources.log_vars import logPass
from service.xbox_one import Xboxone
from log.log import log_internal

from apis.get_config import get_config
from apis.get_powerstatus import get_powerstatus
from apis.post_command import post_command


def start_bottle():

    ################################################################################################
    # Create device
    ################################################################################################

    _xbox = Xboxone()

    log_internal(logPass, logDescDeviceObjectCreation, description='success')

    ################################################################################################
    # APIs
    ################################################################################################

    @route('/config', method=['OPTIONS'])
    @route('/powerstatus', method=['OPTIONS'])
    @route('/command', method=['OPTIONS'])
    def api_cors_options(**kwargs):
        return response_options()

    @get('/config')
    def api_get_config():
        response = get_config(request)
        return response

    @get('/powerstatus')
    def api_get_powerstatus():
        response = get_powerstatus(request, _xbox)
        return response

    @post('/command')
    def api_post_command():
        response = post_command(request, _xbox)
        return response

    ################################################################################################

    host = '0.0.0.0'
    port = get_cfg_port()
    run(host=host, port=port, server='paste', debug=True)

    log_internal(logPass, logDescPortListener.format(port=port), description='started')

    ################################################################################################
