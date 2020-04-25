import json
from datetime import datetime

from mongo_c import find_speed
import app
from object_detections.yolo_video import Video_Detection
from json import dumps

if __name__ == '__main__':

    '''
    licence_plate = PlateDetection()
    licence_plate.start()
    
    video = Video_Detection()
    video.start()

    ocr = Ocr()
    p = ocr.merge_plates()        
    
    car = Video_Detection()
    car.start()
        '''
    total_distance = 0
    total_time = 0
    while(1):
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
                        "cam1" : data.__getitem__("cam1"),
                        "cam2": data.__getitem__("cam2"),
                        "tarih": response.__getitem__("tarih")

                    }
                    total_distance += data.__getitem__("mesafe")
                    total_time += data.__getitem__("time")
                    print(json_data)
                    app.postValues('http://localhost:3000/klnistek/', json_data)

                total_speed = total_distance / total_time

                json = {
                    "_id": id,
                    "plaka": response.__getitem__("plaka"),
                    "hız": total_speed,
                    "mesafe": total_distance,
                    "tarih": response.__getitem__("tarih")

                }
                app.updateValues('http://localhost:3000/klnistek/' + id,json)


