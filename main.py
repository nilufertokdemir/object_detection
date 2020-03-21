from car_detection import Car_image_detection
from plate_detection import PlateDetection


if __name__ == '__main__':

    car_detect = Car_image_detection()
    car_detect.start()
    licence_plate = PlateDetection()
    licence_plate.start()