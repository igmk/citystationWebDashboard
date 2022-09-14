# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import datetime
import json

hostName = "localhost"
serverPort = 80

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/data.json":
            dict = {
                "datetime": datetime.datetime.now().strftime("%d.%m.%Y %H:%M"),
                "temperature": 20.0,
                "humidity": 35,
                "pressure": 1013,
                "uv": 3,
                "direction": "NW",
                "speed": 7
            }
            #read last entry from data file and update dict
            # To do
            #serve json
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(bytes(json.dumps(dict, ensure_ascii=False), 'utf-8'))
        else:
            #f = open("./index.html")
            self.send_response(200)
            self.send_header('Content-type',"text/html")
            self.end_headers()
            #self.wfile.write(bytes(f.read(), 'utf-8'))
            #f.close()
            with open('./index.html', 'rb') as file: 
                self.wfile.write(file.read()) # Read the file and send the contents 
            


if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")