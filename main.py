
from mongo_c import find_speed
import app
from object_detections.plate_detection import PlateDetection
from object_detections.yolo_video import Video_Detection

def compare(json_data, responses):
    comp = []
    for response in responses:
        if response.__getitem__("hız") !=0 and response.__getitem__("mesafe") != 0:
            json = {
                "hız": response.__getitem__("hız"),
                "adres": response.__getitem__("adres"),
                "adres2": response.__getitem__("adres2"),
                "tarih": response.__getitem__("tarih").split("T")[0]
            }
            comp.append(json)

    json_data = {
                "hız": json_data.__getitem__("hız"),
                "adres": json_data.__getitem__("adres"),
                "adres2": json_data.__getitem__("adres2"),
                "tarih": json_data.__getitem__("tarih").split("T")[0]
            }

    if not json_data in comp:
        return 1
    else:
        return 0

if __name__ == '__main__':

    #video = Video_Detection()
    #video.start()

    while True:
        responses = app.klnIst("http://localhost:3000/klnistek/list")
        for response in responses:
            if response.__getitem__("hız") == 0 and response.__getitem__("mesafe") == 0:
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
                    responses = app.klnIst("http://localhost:3000/klnistek/list")
                    if len(responses) > 0:
                        result = compare(json_data, responses)
                        if result == 1:
                            app.postValues('http://localhost:3000/klnistek/', json_data)
                    elif len(responses) == 0:
                        app.postValues('http://localhost:3000/klnistek/', json_data)
                app.deleteValues('http://localhost:3000/klnistek/sil/' + id)





