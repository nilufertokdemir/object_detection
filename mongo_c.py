from datetime import datetime

import find_distance
import app

def find_speed(url, req):
    response = app.aracApiConnection(url)

    dates = []
    items = []
    camIds = []
    total_distance = 0.0
    total_time = 0.0
    times = []
    d = []

    for data in response:
        items.append(data.__getitem__('plate') + "_" + str(data.__getitem__('camId')) + "_" + str(data.__getitem__('time')))


    for item in items:
       if req == item.split("_")[0]:
            date = item.split("_")[2]
            dates.append(date.split(":")[0])
            camIds.append(item.split("_")[1])
            time = date.split(":")[1] + ":" + date.split(":")[2]
            times.append(time.split(".")[0])
            if len(camIds) == 2 and all(x == dates[0] for x in dates):
                d.append(item.split("_")[2])
                dates.reverse()
                format = '%H:%M'
                total_time += (datetime.strptime(times[0], format) - datetime.strptime(times[1], format)).total_seconds()

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
                camIds.pop(0)
                times.pop(0)
                dates.pop(1)

    speed = total_distance / (total_time/3600.0)
    data = []

    data.append(speed)
    data.append(total_distance)
    #app.postValues('http://localhost:3003/klnistek/', json_data)
    return data
