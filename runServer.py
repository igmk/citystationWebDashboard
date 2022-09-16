# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import pandas as pd

hostName = "134.95.211.110"
serverPort = 8080
dataFilePath = "/data/obs/site/cgn/meteo_sport/latest_values.dat"

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/data.json":
            df = pd.read_csv(dataFilePath, header=1, skiprows=[2,3])
            #convert wind direction
            dir_name=[ 'N', 'NNO', 'NO', 'ONO','O','OSO','SO','SSO','S','SSW','SW','WSW','W','WNW', 'NW', 'NNW', 'N' ] 
            directionLetter = dir_name[int(df['WindDir_D1_WVT'].item()/22.5+0.5)]
            speed = round(df['WS_ms_S_WVT'].item()*3.6,1)
            dict = {
                "datetime":         df['TIMESTAMP'].item(),
                "temperature":      round(df['AirTC_2_Avg'].item(),1),
                "humidity":         round(df['RH_2'].item(),0),
                "pressure":         round(df['BP_mbar_Avg'].item(),0),
                "uv":               round(df['UVind_Avg'].item(),0),
                "direction":        directionLetter,
                "speed":            str(speed).replace(".",",")
            }
            #read last entry from data file and update dict
            # To do
            #serve json
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(bytes(json.dumps(dict, ensure_ascii=False), 'utf-8'))
        elif self.path == "/script.js":
            #f = open("./index.html")
            self.send_response(200)
            self.send_header('Content-type',"text/javascript")
            self.end_headers()
            #self.wfile.write(bytes(f.read(), 'utf-8'))
            #f.close()
            with open('./script.js', 'rb') as file: 
                self.wfile.write(file.read()) # Read the file and send the contents 
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
