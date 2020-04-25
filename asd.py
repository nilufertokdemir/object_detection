from datetime import datetime

import app

response = app.aracApiConnection("http://localhost:3003/arac/list")

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

    date = item.split("_")[2]
    dates.append(date.split(":")[0])
    format = '%d-%m-%Y'
    dt_obj = datetime.strptime(dates[0].split("T")[0],'%Y-%m-%d')
    x = datetime.strftime(dt_obj, format)
    print(x)