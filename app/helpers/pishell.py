"""
    PiShell
"""

from datetime import timedelta
import subprocess

from flask import flash
from flask import current_app as app

class PiShell(object):

    def network_inferfaces( self ):
        interfaces_types = ['eth0','wlan0','wlan1']
        p = subprocess.Popen('ifconfig', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        response = out.split('\n')


        raw_interfaces = []
        for r in response:
            if 'eth0' in r or 'wlan0' in r:
                i_lines = []
                t = 0
                while True:
                    if response[t].strip() == '':
                        break
                    i_lines.append( response[t] )
                    t += 1
                raw_interfaces.append( i_lines )

        interfaces = []
        c          = 0
        for i in raw_interfaces:
            interface        = {}
            print i
            interface['mac'] = self.__find_segment( interface, 'HWaddr')
            # interface['mac'] = response[c].split('HWaddr')[1].strip()
            interface['ip']  = response[c+1].split('Bcast')[0].split('addr:')[1].strip()
            interface['rx']  = {
                'name'      : '',
                'packets'   : response[c+4].split('packets:')[1].split(' errors')[0].strip(),
                'errors'    : response[c+4].split('errors:')[1].split(' dropped')[0].strip(),
                'dropped'   : response[c+4].split('dropped:')[1].split(' overruns')[0].strip(),
                'bytes_raw' : response[c+7].split('RX bytes:')[1].split('(')[0].strip()
            }
            interface['tx']  = {
                'name'      : '',
                'packets'   : response[c+5].split('packets:')[1].split(' errors')[0].strip(),
                'errors'    : response[c+5].split('errors:')[1].split(' dropped')[0].strip(),
                'dropped'   : response[c+5].split('dropped:')[1].split(' overruns')[0].strip(),
                'bytes_raw' : response[c+7].split('TX bytes:')[1].split('(')[0].strip()
            }
            response[c+5]
            interfaces.append( interface )
            c += 1
        return interfaces

    def uptime( self ):
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
            uptime_string = str(timedelta(seconds = uptime_seconds))
        return uptime_string

    def __find_segment( self, _list, search_segment ):
        c = 0
        for line in _list:
            if search_segment in line:
                return _list[ c ]
            c += 1


# End File: app/helpers/pishell.py
