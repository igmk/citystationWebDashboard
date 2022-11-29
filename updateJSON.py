#!/usr/bin/python3
# line above allows this file to be directly executable under linux

import json
import pandas as pd
import time

dataFilePath = "/data/obs/site/cgn/meteo_sport/latest_values.dat"
jsonFilePath = "/home/citystation/public_html/webDashboard/data.json"
# jsonFilePath = "/home/jschween/public_html/citystation/webDashboard/data.json"

cl51_dataPath = "/data/obs/site/cgn/cl51/l0/last_cbh.txt"


# formatting of cloud base heights 
def cbh_to_str( cbh_m, cbh_s, digits ):
  sm = str(round(cbh_m,digits)).replace(".",",").replace('nan','---')
  ss = str(round(cbh_s,digits)).replace(".",",").replace('nan','---')
  if (cbh_s == 0) or (sm == '---') :
    s = sm
  else :
    s = sm+'&pm;'+ss
  return s


def updateJSON():

    # read data from files
    df      = pd.read_csv(dataFilePath, header=1, skiprows=[2,3])
    df_cl51 = pd.read_csv(cl51_dataPath, header=0, comment='#' )

    #convert wind direction
    dir_name=[ 'N', 'NNO', 'NO', 'ONO','O','OSO','SO','SSO','S','SSW','SW','WSW','W','WNW', 'NW', 'NNW', 'N' ]
    directionLetter = dir_name[int(df['WindDir_D1_WVT'].item()/22.5+0.5)]

    # speed in km/h with one digit after the decimal point 
    speed = round(float(df['WS_ms_S_WVT'].item())*3.6,1)

    # juggle with time to get a time string (you know: pyhton and time - sigh - )
    datetime = pd.to_datetime(df['TIMESTAMP'].item())
    datetime = datetime.tz_localize('utc').tz_convert('Europe/Berlin')
   
    # create a dict with nicely formatted strings for the variables 
    dict = {
        "datetime":         datetime.strftime("%d.%m.%Y %H:%M:%S"),
        "temperature":      str(round(df['AirTC_2_Avg'].item(),1)).replace(".",","),
        "humidity":         round(df['RH_2'].item(),0),
        "pressure":         round(df['BP_mbar_Avg'].item(),0),
        "uv":               round(df['UVind_Avg'].item(),0),
        "direction":        directionLetter,
        "speed":            str(speed).replace(".",","),
        "cbh_cur":          cbh_to_str( df_cl51['cbh[last] (km)'].values.item(), 0 , 2 ),  # .item() is deprecated - programming aesteticians have decided .values.item() is better than .item()  E-/
        "cbh_low":          cbh_to_str( df_cl51['cbh_low_m (km)'].values.item(), df_cl51['cbh_low_s (km)'].values.item(), 2 ),
        "cbh_mid":          cbh_to_str( df_cl51['cbh_mid_m (km)'].values.item(), df_cl51['cbh_mid_s (km)'].values.item(), 2 ),
        "cbh_hig":          cbh_to_str( df_cl51['cbh_hig_m (km)'].values.item(), df_cl51['cbh_hig_s (km)'].values.item(), 2 )
        }

    # export these strings in data.json
    with open(jsonFilePath, 'w') as f:
        json.dump(dict, f) 



# run this function twice ...
updateJSON()
time.sleep(30)
updateJSON()

