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
    while(1):
        response = app.klnIst("http://localhost:3000/klnistek/list")
        response.reverse()
        if response[0].__getitem__("hız") == "" and response[0].__getitem__("mesafe") == "":
            id = response[0].__getitem__("_id")
            datas = find_speed("http://localhost:3000/arac/list", response[0].__getitem__("plaka"))
            format = '%d-%m-%Y'
            dt_obj = datetime.strptime(datas[0], '%d-%m-%Y')
            s = str(dt_obj)
            print(s)
            json_data = {
                "_id": id,
                "plaka": response[0].__getitem__("plaka"),
                "hız": datas[1],
                "mesafe": datas[2],
                "tarih": str(dt_obj).split(" ")[0]
            }

            print(json_data)
            app.updateValues('http://localhost:3000/klnistek/' + id, json_data)
            print("ok.")

