#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import with_statement
from __future__ import absolute_import



"""r0c.py: retr0chat Telnet/Netcat Server"""
__version__   = "0.9"
__author__    = "ed <a@ocv.me>"
__credits__   = ["stackoverflow.com"]
__license__   = "MIT"
__copyright__ = 2017



import sys
import signal

if sys.version_info[0] == 2:
	sys.dont_write_bytecode = True

from r0c.config   import *
from r0c.util     import *
from r0c.c_vt100  import *
from r0c.c_telnet import *
from r0c.chat     import *



if __name__ != '__main__':
	print('this is not a library')
	sys.exit(1)

if len(sys.argv) != 3:
	print('need argument 1:  telnet port (or 0 to disable)')
	print('need argument 2:  netcat port (or 0 to disable)')
	sys.exit(1)

telnet_port = int(sys.argv[1])
netcat_port = int(sys.argv[2])

print('  *  Telnet server on port', telnet_port)
print('  *  NetCat server on port', netcat_port)

p = Printer()

p.p('  *  Capturing ^C')
signal.signal(signal.SIGINT, signal_handler)

p.p('  *  Creating world')
world = World()

p.p('  *  Starting telnet server')
telnet_host = TelnetHost(p, '0.0.0.0', telnet_port, world)

p.p('  *  Starting push driver')
push_thr = threading.Thread(target=push_worker, args=([telnet_host],))
push_thr.daemon = True
push_thr.start()

p.p('  *  Running')
asyncore.loop(0.05)

print(" !!! you shouldn't be seeing this")
sys.exit(1)
