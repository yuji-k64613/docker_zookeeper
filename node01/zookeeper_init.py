#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kazoo.client import KazooClient
from kazoo.protocol.states import KazooState
import sys
import time
import threading
import logging

# cmd nodename nodes timeout
argv = sys.argv
argc = len(argv) - 1

if argc < 3:
  print("ARG")
  sys.exit(0)
nodename = argv[1]
nodes = int(argv[2])
timeout = int(argv[3])

exitCode = 0

zk = KazooClient()
zk.start()

def init(event):
  list = zk.get_children("/message/init", watch=init)
  if len(list) < nodes:
    return
  t.cancel()

def finish():
  global exitCode
  exitCode = 10

t = threading.Timer(timeout, finish)
if __name__ == '__main__':
  logging.basicConfig()
  zk.ensure_path('/message/init')

  zk.create("/message/init/" + nodename, "", ephemeral=True)
  init(None)
  t.start()
  t.join()
  sys.exit(exitCode)
