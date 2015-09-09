#!venv/bin/python
from app import app

import socket
import os
server_ip = str(socket.gethostbyname(socket.gethostname()))
if os.path.exists('config/_ip.inf'): 
	in_file = open('config/_ip.inf',"r")
	server_ip = in_file.read().replace("\n", "").strip()
	in_file.close()


# Load default config and override config from an environment variable
app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='development key',
    API_SERVER_IP = server_ip,
    API_SERVER_PORT = '5003'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

server_port = 5005
if server_ip == "137.110.160.48": server_port = 80

app.run(host=server_ip, port=server_port)
