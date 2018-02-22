import time
import socket, select
from multiprocessing import Manager, Process

from resources.lang.enGB.logs import *
from resources.global_resources.log_vars import logPass, logFail, logException
from log.log import log_outbound, log_internal
from config.config import get_cfg_details_ip, get_cfg_details_liveId


class Xboxone():

    _port = 5050
    _XBOX_PING = "dd00000a000000000000000400000002"

    def __init__(self):
        #
        self._xboxIsOn = False
        #
        self._socket = self._create_socket()
        #
        Process(target=self._thread_check_power).start()

    def _create_socket(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setblocking(0)
        s.bind(('0.0.0.0', 0))
        s.connect((get_cfg_details_ip(), self._port))
        return s

    def _xbox_live_id(self):
        #
        if isinstance(get_cfg_details_liveId(), str):
            return get_cfg_details_liveId().encode()
        else:
            return get_cfg_details_liveId()

    def _power_payload(self):
        power_payload = b'\x00' + chr(len(self._xbox_live_id())).encode() + self._xbox_live_id() + b'\x00'
        power_header = b'\xdd\x02\x00' + chr(len(power_payload)).encode() + b'\x00\x00'
        return power_header + power_payload

    def _send_power_on(self):
        #
        try:
            data = self._power_payload()
            #
            self._socket.send(data)
            #
            time.sleep(1)
            return True
        except Exception as e:
            #
            log_outbound(logException,
                         get_cfg_details_ip(), self._port, 'SOCKET', logDescDeviceTurnOn,
                         '-', '-', 'n/a',
                         exception=e)
            return False

    def _send_ping(self):
        s = self._create_socket()
        s.send(bytearray.fromhex(self._XBOX_PING))
        result = select.select([s], [], [], 5)[0]
        s.close()
        #
        # r_pass = logPass if len(result) else logFail
        #
        # Commented out log entry here as runs every 10 seconds
        # log_outbound(r_pass,
        #              get_cfg_details_ip(), self._port, 'SOCKET', logDescDeviceGetPowerStatus,
        #              '-', '-', 'n/a')
        #
        return result

    def _check_power(self):
        if len(self._send_ping()):
            self._xboxIsOn = True
        else:
            self._xboxIsOn = False

    def _thread_check_power(self):
        while True:
            self._check_power()
            time.sleep(10)  # 10 seconds

    def check_xbox_on(self):
        self._check_power()
        return self._xboxIsOn

    def turn_on(self):
        #
        for i in range(0, 5):
            self._send_power_on()
            result = self.check_xbox_on()
            #
            log_outbound(result,
                         get_cfg_details_ip(), self._port, 'SOCKET', logDescDeviceTurnOn,
                         '-', '-', 'n/a',
                         description='Attempt number {count}'.format(count=i))
            #
            if result:
                return True
        #
        return False

    def turn_off(self):
        #
        # TODO - turn off device
        #
        return False

    def cmd_power(self):
        if self.check_xbox_on():
            return self.turn_off()
        else:
            return self.turn_on()

    def sendCmd(self, command):
        try:
            #
            if command == 'power':
                r_pass = self.cmd_power()
            else:
                raise Exception('Requested command [{command}] not recognised'.format(command=command))
            #
            result = logPass if r_pass else logFail
            log_internal(result, logDescDeviceSendCommand)
            return r_pass
        except Exception as e:
            log_internal(logException, logDescDeviceSendCommand, exception=e)
            return False
