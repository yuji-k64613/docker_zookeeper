#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kazoo.client import KazooClient
from kazoo.protocol.states import KazooState
import sys
import time
import threading
import logging

zk = KazooClient()
zk.start()

# cmd send status value timeout
# cmd recv status timeout
argv = sys.argv
argc = len(argv) - 1
if argc < 1:
  sys.exit(1)
mode = argv[1]
if mode != "send" and mode != "recv":
    sys.exit(2)

status = argv[2]
if mode == "send":
    if argc < 4:
      sys.exit(1)
    value = argv[3]
    timeout = int(argv[4])
else:
    if argc < 3:
      sys.exit(1)
    timeout = int(argv[3])

exitCode = 0

def send(event):
    global value

    if event is None:
        zk.create("/message/{0}/{1}".format(status, mode),
            value, ephemeral=True)
    list = zk.get_children("/message/{0}".format(status), watch=send)
    if len(list) < 3:
        return
    t.cancel()

def recv(event):
    global value

    if event is None:
        zk.create("/message/{0}/{1}".format(status, mode),
            "", ephemeral=True)
    list = zk.get_children("/message/{0}".format(status), watch=recv)
    if len(list) < 2:
        return
    if len(list) == 2:
        values = zk.get("/message/{0}/{1}".format(status, "send"))
        value = values[0]
        zk.create("/message/{0}/{1}".format(status, "done"),
            "", ephemeral=True)
        return
    t.cancel()

def finish():
    global exitCode
    exitCode = 100

t = threading.Timer(timeout, finish)
if __name__ == '__main__':
    logging.basicConfig()
    zk.ensure_path('/message/{0}'.format(status))

    if mode == "send":
        send(None)
    else:
        recv(None)
    t.start()
    t.join()
    if mode == "recv" and exitCode == 0:
        print(value)
    sys.exit(exitCode)
