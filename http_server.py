import SimpleHTTPServer
import SocketServer
import json
import time
import resourses
from resourses import *
from datetime import date

PORT = 8765

config = {
# 'filename': 'codes.csv',
}



def getShipByShipName(ShipName):
    Model = Ship.get(Ship.name == ShipName)
    return Model.json

class MyRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        print self.path
        code_str =  self.path[1:]
        tags = code_str.split("/")

        answer = ""
        if tags[0] == "ship":
            name = tags[1]
            answer = getShipByShipName(name)

        if answer:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
        else:
            self.send_response(404)
        self.end_headers()

        if answer:
            self.wfile.write(answer);
        self.wfile.close();

    def do_POST(self):
        print self.path
        code_str =  self.path[1:]
        tags = code_str.split("/")

        answer = ""
        if tags[0] == "order":

            content_len = int(self.headers.getheader('content-length', 0))
            post_body = self.rfile.read(content_len)
            order = json.loads(post_body)

            ship = Ship.get(Ship.name == order['shipName'])
            ShipModuleTask.create(module=order['moduleName'], 
                                    task=order['order'], ship=ship)

            answer = json.dumps({"status":True})

        if answer:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
        else:
            self.send_response(404)
        self.end_headers()

        if answer:
            self.wfile.write(answer);
        self.wfile.close();

Handler = MyRequestHandler
httpd = SocketServer.TCPServer(("", PORT), Handler)

print "serving at port", PORT
httpd.serve_forever()