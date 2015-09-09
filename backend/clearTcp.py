#!venv/bin/python
import sys
import os
import time
from threading import Thread
import datetime
import subprocess

__BACKEND_SERVER_PORT = "5003"

if not 'SUDO_UID' in os.environ.keys():
  print "this program requires super user priv."
  sys.exit(1)


pid = None
try:
	grepOutput = subprocess.check_output("netstat -lpn | grep " + __BACKEND_SERVER_PORT, shell=True)
	grepOutput = grepOutput.replace("\n", "").strip()
	pid = grepOutput.split("LISTEN")[1].split("/")[0].strip()
except:
	pass

if pid:
	os.system('sudo kill -9 ' + pid)


