from datetime import datetime
import urllib.request
import json

import find_distance
import app


def convert_adress(latitude,longitude,cam1,cam2):
    bingMapsKey = "Ajlc9FeCH2OGYiNdqYQAZAdHkuEVx61ZrNvNzM2SA8ksjTyKdzJwuyItDffHsW0U"
    routeUrl = "http://dev.virtualearth.net/REST/v1/Locations/"+str(latitude)+","+str(longitude)+"?key="+bingMapsKey

    request = urllib.request.Request(routeUrl)
    response = urllib.request.urlopen(request)

    r = response.read().decode(encoding="utf-8")
    result = json.loads(r)
    itineraryItems = result["resourceSets"][0]["resources"][0]["name"]
    print("cam1 : "+cam1+"cam2: "+cam2)
    return itineraryItems


def find_speed(url, req):
    response = app.aracApiConnection(url)

    datas = []
    dates = []
    items = []
    camIds = []
    total_distance = 0.0
    total_time = 0.0
    times = []
    for data in response:
        items.append(data.__getitem__('plate') + "_" + str(data.__getitem__('camId')) + "_" + str(data.__getitem__('time')))


    for item in items:
       if req == item.split("_")[0]:
            date = item.split("_")[2]
            dates.append(date.split("T")[0])
            camIds.append(item.split("_")[1])
            d_1 = date.split("T")[1]
            hours_minutes = d_1.split(".")[0]
            times.append(hours_minutes.split(":")[0] + ":" +hours_minutes.split(":")[1])

            if len(camIds) == 2 and all(x == dates[0] for x in dates):

                dates.reverse()
                format = '%H:%M'
                total_time += (datetime.strptime(times[0], format) - datetime.strptime(times[1], format)).total_seconds()
                date = item.split("_")[2]
                src = app.camApiLatLong(int(camIds[0]))
                lat = src[0].__getitem__('lat')
                long = src[0].__getitem__('long')
                #print("lat : " + lat + "long : " + long )
                dest = app.camApiLatLong(int(camIds[1]))
                lat1 = dest[0].__getitem__('lat')
                long1 = dest[0].__getitem__('long')
                #print("lat : " + lat1 + "long : " + long1 )

                distance = find_distance.find_distance(lat, long, lat1, long1)
                total_distance += distance
                print("total time :" + str(total_time))
                speed = total_distance / (total_time/3600.0)

                json_data = {
                    "hız": speed,
                    "mesafe": total_distance,
                    "lat1": lat,
                    "long1": long,
                    "lat2": lat1,
                    "long2": long1,
                    "adres":convert_adress(lat,long,camIds[0],camIds[1]),
                    "adres2": convert_adress(lat1,long1,camIds[0],camIds[1]),
                    "tarih": date,
                    "time": (total_time/3600.0)

                }
                datas.append(json_data)

                camIds.pop(0)
                times.pop(0)
                dates.pop(1)


    return datas
