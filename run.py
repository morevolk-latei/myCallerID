#run a test server
from app import app

HOST_ADDR  =  '0.0.0.0'
PORT 	   =  8080

app.run(host = HOST_ADDR, port = PORT, debug = True)
