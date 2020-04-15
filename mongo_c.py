from datetime import datetime

import find_distance
import app

def find_speed(url, req):
    response = app.aracApiConnection(url)

    datas = []
    dates = []
    items = []
    camIds = []
    total_distance = 0.0
    total_time = 0.0
    times = []
    c = 0
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
                if c == 0:
                    d_t = dates[0].split("T")[0]
                    format = '%d-%m-%Y'
                    dt_obj = datetime.strptime(d_t, '%Y-%m-%d')
                    date_t = datetime.strftime(dt_obj, format)
                    datas.append(date_t)
                    print(date_t)
                    c += 1

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

    datas.append(speed)
    datas.append(total_distance)
    #app.postValues('http://localhost:3003/klnistek/', json_data)
    return datas
