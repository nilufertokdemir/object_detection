from object_detections.car_detection import Car_image_detection
from object_detections.plate_detection import PlateDetection
from object_detections.yolo_video import Video_Detection

from ocr_pth.demo import Ocr

if __name__ == '__main__':

    '''
    licence_plate = PlateDetection()
    licence_plate.start()
    ocr = Ocr()
    p = ocr.merge_plates()
    '''
    video = Video_Detection()
    video.start()
