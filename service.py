from abc import ABC


class Service(ABC):
    def save_image(self,image, extention, c):
        pass
    def get_model(self):
        pass
    def start(self):
        pass