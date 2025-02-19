import cv2


class Preprocessor(object):

    def __init__(self, width, height, inter=cv2.INTER_AREA):

        self.width = width
        self.height = height
        self.inter = inter

    def preprocess(self, src):

        return cv2.resize(src, (self.width, self.height),
                          interpolation=self.inter)
