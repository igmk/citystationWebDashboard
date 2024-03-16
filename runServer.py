# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
from updateJSON import cbh_to_str
import json
import pandas as pd


local = False
if local:
    hostName = "localhost"
    serverPort = 8080
    dataFilePath = "./latest_values.dat"
    thiesFilePath = "./latest_thies.dat"
    cl51FilePath = "./last_cbh.txt"

else:
    hostName = "134.95.211.110"
    serverPort = 8080
    dataFilePath = "/data/obs/site/cgn/meteo_sport/latest_values.dat"
    thiesFilePath = "/data/obs/site/cgn/thies/latest_thies.dat"
    jsonFilePath = "/home/citystation/public_html/webDashboard/data.json"
    cl51FilePath = "/data/obs/site/cgn/cl51/l0/last_cbh.txt"


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/data.json":
            df = pd.read_csv(dataFilePath, header=1, skiprows=[2, 3])
            df_cl51 = pd.read_csv(cl51FilePath, header=0, comment="#")
            df_thies = pd.read_csv(thiesFilePath)

            datetime = pd.to_datetime(df["TIMESTAMP"].values.item())
            datetime = datetime.tz_localize("utc").tz_convert("Europe/Berlin")

            # convert wind direction
            dir_name = [
                "N",
                "NNO",
                "NO",
                "ONO",
                "O",
                "OSO",
                "SO",
                "SSO",
                "S",
                "SSW",
                "SW",
                "WSW",
                "W",
                "WNW",
                "NW",
                "NNW",
                "N",
            ]
            directionLetter = dir_name[int(df["WindDir_D1_WVT"].item() / 22.5 + 0.5)]
            speed = round(df["WS_ms_S_WVT"].item() * 3.6, 1)
            dict = dict = {
                "datetime": datetime.strftime("%Y-%m-%d %H:%M:%S"),
                "temperature": {
                    "value": round(df["AirTC_2_Avg"].values.item(), 1),
                    "unit": "°C",
                    "string": str(round(df["AirTC_2_Avg"].values.item(), 1)).replace(
                        ".", ","
                    ),
                },
                "humidity": {"value": round(df["RH_2"].values.item(), 0), "unit": "%"},
                "pressure": {
                    "value": round(df["BP_mbar_sl_Avg"].values.item(), 0),
                    "unit": "hPa",
                },
                "uv": {"value": round(df["UVind_Avg"].values.item(), 0), "unit": ""},
                "wind_direction": {
                    "value": df["WindDir_D1_WVT"].values.item(),
                    "unit": "",
                    "string": directionLetter,
                },
                "wind_speed": {
                    "value": speed,
                    "unit": "km/h",
                    "string": str(speed).replace(".", ","),
                },
                "global_radiation": {
                    "value": round(max(0, df["SWUpper_Avg"].values.item())),
                    "unit": "W/m²",
                },
                "cbh_cur": {
                    "string": cbh_to_str(
                        df_cl51["cbh[last] (km)"].values.item() * 1000.0, 0, 0
                    ),
                    "unit": "m",
                },
                "precip": {
                    "precip_last_hour": {
                        "value": round(
                            df_thies["accum_precip_1_hour"].values.item(), 1
                        ),
                        "unit": "mm",
                        "string": str(
                            round(df_thies["accum_precip_1_hour"].values.item(), 1)
                        ).replace(".", ","),
                    },
                    "precip_type": {
                        "value": df_thies["precip_type"].values.item(),
                        "unit": "METAR 4678",
                    },
                    "precip_rate": {
                        "value": round(df_thies["precip_rate"].values.item(), 1),
                        "unit": "mm/min",
                    },
                },
            }
            # read last entry from data file and update dict
            # To do
            # serve json
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(json.dumps(dict, ensure_ascii=False), "utf-8"))
        elif self.path == "/script.js":
            # f = open("./index.html")
            self.send_response(200)
            self.send_header("Content-type", "text/javascript")
            self.end_headers()
            # self.wfile.write(bytes(f.read(), 'utf-8'))
            # f.close()
            with open("./script.js", "rb") as file:
                self.wfile.write(file.read())  # Read the file and send the contents
        else:
            # f = open("./index.html")
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            # self.wfile.write(bytes(f.read(), 'utf-8'))
            # f.close()
            with open("./index.html", "rb") as file:
                self.wfile.write(file.read())  # Read the file and send the contents


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
