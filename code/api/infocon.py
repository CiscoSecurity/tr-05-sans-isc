import requests
import re
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

def get_infocon():
    url = "https://isc.sans.edu/daily_alert.html"
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    threat_level = re.search('<b>(.*)</b>', response.text).group(1).upper()
    try :
        diary_name = re.search(';(.*)</a>', response.text).group(1)
    except:
        diary_name = '----'
    url = re.search('<a href="(.*)">', response.text).group(1)
    return threat_level, diary_name, url

def get_attack_summary(date_range):
    end_day = str(datetime.now().strftime("%Y-%m-%d"))
    date_range = date_range - 1
    start_day = str((datetime.now() - timedelta(days=date_range)).strftime("%Y-%m-%d"))
    url = 'https://isc.sans.edu/api/dailysummary/{}/{}'.format(start_day, end_day)
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    myroot = ET.fromstring(response.text)
    return myroot, start_day, end_day

def get_topports():
    today = str(datetime.now().strftime("%Y-%m-%d"))
    url = "https://isc.sans.edu/api/topports/records/10/{}?json".format(today)
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()
    return data, today

def get_topip():
    today = str(datetime.now().strftime("%Y-%m-%d"))
    url = "https://isc.sans.edu/api/sources/attacks/10/{}?json".format(today)
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()
    return data, today
