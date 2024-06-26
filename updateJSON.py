#!/usr/bin/python3
# line above allows this file to be directly executable under linux

import json
import pandas as pd
import time
import numpy as np


local = False

if local:
    dataFilePath = "./latest_values.dat"
    thiesFilePath = "./latest_thies.dat"
    jsonFilePath = "./data.json"
    cl51FilePath = "./last_cbh.txt"
    ozoneFilePath = "./latest_ozone.dat"
else:
    dataFilePath = "/data/obs/site/cgn/meteo_sport/latest_values.dat"
    cl51FilePath = "/data/obs/site/cgn/cl51/l0/last_cbh.txt"
    thiesFilePath = "/data/obs/site/cgn/thies/latest_thies.dat"
    ozoneFilePath = "/data/obs/site/cgn/aqm/latest_ozone.dat"
    jsonFilePath = "/home/citystation/public_html/webDashboard/data.json"
# jsonFilePath = "data.json"


def float_format(x, n_digits):
    # function to format x with n_digits after the decimal point
    # replace decimal point with comma, replace 'nan' with three dashes '---'
    # this works with also with integers or n_digits=0, in contrast to e.g. round( 1.23, 0) which generates '1.0'
    s = (
        ("{0:." + str(n_digits) + "f}")
        .format(x)
        .replace(".", ",")
        .replace("nan", "---")
    )
    return s


def dew_point(T, RH):
    # Function from dx.doi.org/10.1175/BAMS-86-2-225
    # T in Celsius, RH in %
    A = 17.625
    B = 243.04
    frac_1 = B * (np.log(RH / 100) + (A * np.divide(T, np.add(B, T))))
    frac_2 = A - np.log(RH / 100) - A * np.divide(T, np.add(B, T))
    return np.divide(frac_1, frac_2)


# formatting of cloud base heights
def cbh_to_str(cbh_m, cbh_s, n_digits):
    # create string of the form   'mean +/- stddev' (cbh_m+/-cbh_s) with n_digits after the decimal point
    # if  cbh_s == 0  or  cbh_s==nan  only cbh_m is provided, nan is replaced by '---'
    sm = float_format(cbh_m, n_digits)
    ss = float_format(cbh_s, n_digits)

    if (cbh_s == 0) or (sm == "---"):
        s = sm
    else:
        s = sm + "&pm;" + ss
    return s


def updateJSON():
    # read data from files
    df = pd.read_csv(dataFilePath, header=1, skiprows=[2, 3])
    df_cl51 = pd.read_csv(cl51FilePath, header=0, comment="#")
    df_thies = pd.read_csv(thiesFilePath)
    df_ozone = pd.read_csv(ozoneFilePath, header=0)

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

    directionLetter = dir_name[int(df["WindDir_D1_WVT"].values.item() / 22.5 + 0.5)]

    # speed in km/h with one digit after the decimal point
    speed = round(float(df["WS_ms_S_WVT"].values.item()) * 3.6, 1)

    # convert utc time stamp into python datetime
    datetime = pd.to_datetime(df["TIMESTAMP"].values.item())

    datetime = datetime.tz_localize("utc").tz_convert("Europe/Berlin")

    df["dewpoint"] = dew_point(df["AirTC_2_Avg"], df["RH_2"])
    # create a dict with nicely formatted strings for the variables
    dict = {
        "datetime": datetime.strftime("%Y-%m-%d %H:%M:%S"),
        "temperature": {
            "value": round(df["AirTC_2_Avg"].values.item(), 1),
            "unit": "°C",
            "string": str(round(df["AirTC_2_Avg"].values.item(), 1)).replace(".", ","),
        },
        "dewpoint": {
            "value": round(df["dewpoint"].values.item(), 1),
            "unit": "°C",
            "string": str(round(df["dewpoint"].values.item(), 1)).replace(".", ","),
        },
        "humidity": {"value": round(df["RH_2"].values.item(), 0), "unit": "%"},
        "pressure": {
            "value": round(df["BP_mbar_sl_Avg"].values.item(), 0),
            "unit": "hPa",
        },
        "ground-pressure": {
            "value": round(df["BP_mbar_Avg"].values.item(), 0),
            "unit": "hPa",
        },
        "uv": {"value": round(df["UVind_Avg"].values.item(), 0), "unit": ""},
        "wind_direction": {
            "value": df["WindDir_D1_WVT"].values.item(),
            "unit": "°",
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
                "value": round(df_thies["accum_precip_1_hour"].values.item(), 1),
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
        "ozone": {
            "value": round(max(0, df_ozone.values.item())),
            "unit": "ppb",
        },
    }

    # export these strings in data.json
    with open(jsonFilePath, "w") as f:
        json.dump(dict, f)


# run this function twice ...
updateJSON()
time.sleep(30)
updateJSON()
