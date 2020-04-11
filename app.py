import requests
import json

def camApiConnection(url):
    myResponse = requests.get(url)
    if(myResponse.ok):

        jData = json.loads(myResponse.content)
        #print("The response contains {0} properties".format(len(jData)))
        response_list = []

        for item in jData:
            response_details = {"_id": None, "camId": None, "lat": None, "long": None, "__v": None}
            response_details['_id'] = item['_id']
            #print(item['_id']+'**')
            response_details['camId'] = item['camId']
            response_details['lat'] = item['lat']
            response_details['long'] = item['long']
            response_details['__v'] = item['__v']
            response_list.append(response_details)


        return response_list

    else:
        myResponse.raise_for_status()

def camApiLatLong(id):
    response_list = []
    response = camApiConnection("http://localhost:3000/cam/list")
    response_details = {"camId": None, "lat": None, "long": None}

    for item in response:
        if item['camId'] == id:
            response_details['lat'] = item['lat']
            response_details['long'] = item['long']
            response_list.append(response_details)


    return response_list



def userApi(url):
    myResponse = requests.get(url)
    if (myResponse.ok):

        jData = json.loads(myResponse.content)
        # print("The response contains {0} properties".format(len(jData)))
        response_list = []

        for item in jData:
            response_details = {"_id": None, "plaka": None, "camId_1": None, "mesafe": None, "__v": None}
            response_details['_id'] = item['_id']
            print(item['_id'] + '**')
            response_details['camId'] = item['camId']
            response_details['lat'] = item['lat']
            response_details['long'] = item['long']
            response_details['__v'] = item['__v']
            response_list.append(response_details)

        return response_list;

    else:
        myResponse.raise_for_status()
"""response=[]
response=camApiConnection("http://localhost:3000/cam/list")
print(response[0].__getitem__('_id'))"""

def aracApiConnection(url):
    myResponse = requests.get(url)
    if(myResponse.ok):

        jData = json.loads(myResponse.content)
        response_list = []

        for item in jData:
            response_details = {"_id": None, "plate": None, "time": None, "camId": None, "__v": None}
            response_details['_id'] = item['_id']
            #print(item['_id']+'**')
            response_details['plate'] = item['plate']
            response_details['time'] = item['time']
            response_details['camId'] = item['camId']
            response_details['__v'] = item['__v']
            response_list.append(response_details)

        return response_list;

    else:
        myResponse.raise_for_status()

response=[]
#response=aracApiConnection("http://localhost:3000/arac/list")
#response=aracApiConnection("http://localhost:3000/arac/list")

#print(response[0].__getitem__('_id'))

#------------- POST----------------------
def postValues(api_url, json_data):

    for data in json_data:
        response = requests.post(api_url,json=data)
    if response.status_code >= 500:
        print('[!] [{0}] Server Error'.format(response.status_code))
        return None
    elif response.status_code == 404:
        print('[!] [{0}] URL not found: [{1}]'.format(response.status_code, api_url))
        return None
    else:
        print('[?] Unexpected Error: [HTTP {0}]: Content: {1}'.format(response.status_code, response.content))
        return None


