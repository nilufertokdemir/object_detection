from mongo_c import find_speed
import app
from object_detections.plate_detection import PlateDetection
from object_detections.yolo_video import Video_Detection


if __name__ == '__main__':


    total_distance = 0
    total_time = 0
    while True:
        responses = app.klnIst("http://localhost:3000/klnistek/list")
        for response in responses:
            if response.__getitem__("hız") == "" and response.__getitem__("mesafe") == "":
                id = response.__getitem__("_id")
                datas = find_speed("http://localhost:3000/arac/list", response.__getitem__("plaka"))
                for data in datas:
                    json_data = {
                        "plaka": response.__getitem__("plaka"),
                        "hız": data.__getitem__("hız"),
                        "mesafe": data.__getitem__("mesafe"),
                        "lat1" : data.__getitem__("lat1"),
                        "long1": data.__getitem__("long1"),
                        "lat2": data.__getitem__("lat2"),
                        "long2": data.__getitem__("long2"),
                        "adres":  data.__getitem__("adres"),
                        "adres2": data.__getitem__("adres2"),
                        "tarih": data.__getitem__("tarih").split("T")[0]

                    }
                    total_distance += data.__getitem__("mesafe")
                    total_time += data.__getitem__("time")
                    #print(json_data)
                    app.postValues('http://localhost:3000/klnistek/', json_data)

                total_speed = total_distance / total_time

                json = {
                    "_id": id,
                    "plaka": response.__getitem__("plaka"),
                    "hız": total_speed,
                    "mesafe": total_distance,
                    "tarih": response.__getitem__("tarih")
                }
                #print(json)
                app.updateValues('http://localhost:3000/klnistek/' + id,json)


