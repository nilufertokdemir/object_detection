IMAGE_BASEWIDTH = 700

BOOTSTRAP_SERVER = "134.209.235.13:9092"

AVRO_SCHEMA = '''
{
"namespace": "example.avro",
 "type": "record",
 "name": "Car_Track",
 "fields": [
     {"name": "name", "type": "string"},
     {"name": "date",  "type": "string"},
     {"name": "frame", "type": "bytes"}
 ]
}
'''
MODEL_FILES = "model/"

VEHICLE_DETECTION_CFG = MODEL_FILES + "vehicle_detection.cfg"
VEHICLE_DETECTION_WEIGHT = MODEL_FILES + "vehicle_detection.weights"
CHARACTER_SEGMENTATION_CFG = MODEL_FILES + "character_segmentation.cfg"
CHARACTER_SEGMENTATION_WEIGHT = MODEL_FILES + "character_segmentation.weights"
LP_DETECTION_CFG = MODEL_FILES + "lp_detection.cfg"
LP_DETECTION_WEIGHT = MODEL_FILES + "lp_detection.weights"
DIGITS_CFG = MODEL_FILES + "digits.cfg"
DIGITS_WEIGHT = MODEL_FILES + "digits.weights"
LETTERS_CFG = MODEL_FILES + "letters.cfg"
LETTERS_WEIGHT = MODEL_FILES + "letters.weights"
YOLO9000_CFG = MODEL_FILES + "yolo9000.cfg"
YOLO9000_WEIGHT = MODEL_FILES + "yolo9000.weights"
YOLOV3_CFG = MODEL_FILES + "yolov3.cfg"
YOLOV3_WEIGHT = MODEL_FILES + "yolov3.weights"
YOLOV2_CFG = MODEL_FILES + "yolov2.cfg"
YOLOV2_WEIGHT = MODEL_FILES + "yolov2.weights"


LETTER_LABELS = MODEL_FILES + "letters.data"
DIGIT_LABELS = MODEL_FILES + "digits.data"
LP_LABELS = MODEL_FILES + "lp_detection.data"
SEGMENTATION_LABELS = MODEL_FILES + "lp_detection.data"
YOLO9000_LABELS = MODEL_FILES + "combine9k.data"
COCO_LABELS = MODEL_FILES + "coco.data"


