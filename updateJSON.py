import json
import pandas as pd
import time

dataFilePath = "/data/obs/site/cgn/meteo_sport/latest_values.dat"
jsonFilePath = "/home/citystation/public_html/webDashboard/data.json"

def updateJSON():
    df = pd.read_csv(dataFilePath, header=1, skiprows=[2,3])
    #convert wind direction
    dir_name=[ 'N', 'NNO', 'NO', 'ONO','O','OSO','SO','SSO','S','SSW','SW','WSW','W','WNW', 'NW', 'NNW', 'N' ]
    directionLetter = dir_name[int(df['WindDir_D1_WVT'].item()/22.5+0.5)]
    speed = round(float(df['WS_ms_S_WVT'].item())*3.6,1)
    dict = {
        "datetime":         df['TIMESTAMP'].item(),
        "temperature":      str(round(df['AirTC_2_Avg'].item(),1)).replace(".",","),
        "humidity":         round(df['RH_2'].item(),0),
        "pressure":         round(df['BP_mbar_Avg'].item(),0),
        "uv":               round(df['UVind_Avg'].item(),0),
        "direction":        directionLetter,
        "speed":            str(speed).replace(".",",")
    }
    with open(jsonFilePath, 'w') as f:
        json.dump(dict, f) 
updateJSON()
time.sleep(30)
updateJSON()
