#!venv/bin/python
from app import app



# Load default config and override config from an environment variable
app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='development key'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

import socket
import os
server_ip = str(socket.gethostbyname(socket.gethostname()))
if os.path.exists('config/_ip.inf'): 
	in_file = open('config/_ip.inf',"r")
	server_ip = in_file.read().replace("\n", "").strip()
	in_file.close()


app.run(host=server_ip, port=5003)
