import json
from time import sleep

import requests

#Kamera Bilgileri için GET
def camApiConnection(url):
    myResponse = requests.get(url)
    if(myResponse.ok):

        jData = json.loads(myResponse.content)
        response_list = []

        for item in jData:
            response_details = {"_id": None, "camId": None, "lat": None, "long": None, "__v": None}
            response_details['_id'] = item['_id']
            response_details['camId'] = item['camId']
            response_details['lat'] = item['lat']
            response_details['long'] = item['long']
            response_details['__v'] = item['__v']
            response_list.append(response_details)

        return response_list
    else:
        myResponse.raise_for_status()

#Lat Long bilgileri için GET
def camApiLatLong(id):

    response = camApiConnection("http://localhost:3000/cam/list")
    response_details = {"camId": None, "lat": None, "long": None}
    response_list = []

    for item in response:
        if item['camId'] == id:
            response_details['lat'] = item['lat']
            response_details['long'] = item['long']
            response_list.append(response_details)

    return response_list

#Kullanıcı istekleri için GET fonk.
def klnIst(url):
    myResponse = requests.get(url)
    if (myResponse.ok):

        jData = json.loads(myResponse.content)
        response_list = []
        for item in jData:
            response_details = {"_id": None, "plaka": None, "hız": None, "mesafe": None,  "tarih": None}
            response_details['_id'] = item['_id']
            response_details['plaka'] = item['plaka']
            response_details['hız'] = item['hız']
            response_details['mesafe'] = item['mesafe']
            response_list.append(response_details)

        return response_list

    else:
        myResponse.raise_for_status()


def userApi(url):

    myResponse = requests.get(url)
    if (myResponse.ok):

        jData = json.loads(myResponse.content)
        response_list = []

        for item in jData:
            response_details = {"_id": None, "plaka": None, "camId_1": None, "mesafe": None, "__v": None}
            response_details['_id'] = item['_id']
            response_details['camId'] = item['camId']
            response_details['lat'] = item['lat']
            response_details['long'] = item['long']
            response_details['__v'] = item['__v']
            response_list.append(response_details)

        return response_list;

    else:
        myResponse.raise_for_status()

def aracApiConnection(url):
    myResponse = requests.get(url)
    if(myResponse.ok):

        jData = json.loads(myResponse.content)
        response_list = []

        for item in jData:
            response_details = {"_id": None, "plate": None, "time": None, "camId": None, "__v": None}
            response_details['_id'] = item['_id']
            response_details['plate'] = item['plate']
            response_details['time'] = item['time']
            response_details['camId'] = item['camId']
            #response_details['_v'] = item['_v']
            response_list.append(response_details)

        return response_list;

    else:
        myResponse.raise_for_status()


#------------- POST----------------------
def postValues(api_url, json_data):
    response = requests.post(api_url,json=json_data)
    if response.status_code >= 500:
        print('[!] [{0}] Server Error'.format(response.status_code))
        return None
    elif response.status_code == 404:
        print('[!] [{0}] URL not found: [{1}]'.format(response.status_code, api_url))
        return None
    else:
        print('[?] Unexpected Error: [HTTP {0}]: Content: {1}'.format(response.status_code, response.content))
        return None

#-------------UPDATE-------------------------
def updateValues(api_url, json_data):
    response = requests.put(api_url,json=json_data)
    if response.status_code >= 500:
        print('[!] [{0}] Server Error'.format(response.status_code))
        return None
    elif response.status_code == 404:
        print('[!] [{0}] URL not found: [{1}]'.format(response.status_code, api_url))
        return None
    else:
        print('[?] Unexpected Error: [HTTP {0}]: Content: {1}'.format(response.status_code, response.content))
        return None



def deleteValues(api_url):
    response = requests.delete(api_url)
    if response.status_code >= 500:
        print('[!] [{0}] Server Error'.format(response.status_code))
        return None
    elif response.status_code == 404:
        print('[!] [{0}] URL not found: [{1}]'.format(response.status_code, api_url))
        return None
    else:
        print('[?] Unexpected Error: [HTTP {0}]: Content: {1}'.format(response.status_code, response.content))
        return None


