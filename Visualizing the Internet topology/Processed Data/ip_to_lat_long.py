import requests
import csv
from ipstack import GeoLookup

import sys
import json

sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')


seethis = "50f141082fc71e5c61bce75b79f35ff7"



geo_lookup = GeoLookup("50f141082fc71e5c61bce75b79f35ff7")

count = 1


def get_location(ip_address,count):
    location = geo_lookup.get_location(ip_address)

    # print(location)
    
    location_data = {
        "Id": count,
        "ip": ip_address,
        "latitute": location.get("latitude"),
        "longitude": location.get("longitude"),
        # "AS_NUMBER": location.get("connection")
    }

    if(location.get("latitude") == 0.0):
        return {}
    return location_data

filename = '1.json'

lst = []

with open('Amazon.csv',encoding='utf-8') as file_obj:
    reader_obj = csv.DictReader(file_obj)
    for row in reader_obj:
       with open(filename,mode='w') as f:
            temp = get_location(row['Ip'],count)
            if(temp != {}):
                lst.append(get_location(row['Ip'],count))
                count = count + 1
            json.dump(lst,f)

import pandas as pd

df = pd.read_json("1.json")

df.to_csv("output_ama.csv",index=False)