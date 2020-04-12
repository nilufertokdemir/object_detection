
from mongo_c import find_speed
import app
if __name__ == '__main__':

    '''
    licence_plate = PlateDetection()
    licence_plate.start()
    
    video = Video_Detection()
    video.start()

    ocr = Ocr()
    p = ocr.merge_plates()        
    '''

    while(1):
        response = app.klnIst("http://localhost:3003/klnistek/list")
        response.reverse()
        if response[0].__getitem__("hız") == "" and response[0].__getitem__("mesafe") == "":
            id = response[0].__getitem__("_id")
            datas = find_speed("http://localhost:3003/arac/list",response[0].__getitem__("plaka"))
            json_data = {
                "_id":response[0].__getitem__("_id"),
                "plaka": response[0].__getitem__("plaka"),
                "hız": datas[0],
                "mesafe": datas[1],
                "tarih": response[0].__getitem__("tarih"),
            }
            app.updateValues('http://localhost:3003/klnistek/' + id, json_data)
            print("ok.")


