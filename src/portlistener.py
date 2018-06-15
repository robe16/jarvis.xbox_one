import threading
from bottle import get, post
from bottle import request, run

from config.config import get_cfg_port_listener
from resources.lang.enGB.logs import *
from resources.global_resources.log_vars import logPass
from service.xbox_one import Xboxone
from log.log import log_internal

from apis.uri_config import get_config
from apis.uri_get_powerstatus import get_powerstatus
from apis.uri_post_command import post_command


def start_bottle(port_threads):

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

    def bottle_run(x_host, x_port):
        log_internal(logPass, logDescPortListener.format(port=x_port), description='started')
        run(host=x_host, port=x_port, debug=True)

    ################################################################################################

    host = 'localhost'
    ports = get_cfg_port_listener()
    for port in ports:
        t = threading.Thread(target=bottle_run, args=(host, port,))
        port_threads.append(t)

    # Start all threads
    for t in port_threads:
        t.start()
    # Use .join() for all threads to keep main process 'alive'
    for t in port_threads:
        t.join()
