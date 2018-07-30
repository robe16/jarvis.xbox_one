from bottle import get, post
from bottle import request, run

from config.config import get_cfg_port
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

    @get('/config')
    def api_get_config():
        return get_config(request)

    @get('/powerstatus')
    def api_get_powerstatus():
        return get_powerstatus(request, _xbox)

    @post('/command')
    def api_post_command():
        return post_command(request, _xbox)

    ################################################################################################

    host = '0.0.0.0'
    port = get_cfg_port()
    run(host=host, port=port, server='paste', debug=True)

    log_internal(logPass, logDescPortListener.format(port=port), description='started')

    ################################################################################################
