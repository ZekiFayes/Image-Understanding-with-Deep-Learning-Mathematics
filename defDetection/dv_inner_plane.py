from dv_basic_functions import BasicLib, dv_right, dv_left, dv_quadratic
import cv2


class InnerPlane(BasicLib):

    def innerPlaneDetection(self, src):

        binary_thresh, area_thresh = 60, 3000
        roi, rect = self.segmentROI(src, binary_thresh, area_thresh)
        binary_roi = self.binariezImage(roi, 110, cv2.THRESH_BINARY)
        self.showImage("roi", roi)
        binary_roi = self.removeNoise(binary_roi, area_thresh)
        h, w = self.getImageShape(roi)
        right_points = self.getEdgePoints(binary_roi, h//5, 4*h//5, 200, dv_right)
        left_points = self.getEdgePoints(binary_roi, h//5, 4*h//5, 200, dv_left)
        right_points_hat = self.fitQuadraticCurve(right_points)
        left_points_hat = self.fitQuadraticCurve(left_points)
        delta = 70
        binary_roi_image = self.scanRows(roi, left_points_hat, right_points_hat, delta)
        self.showImage("binary_roi_image", binary_roi_image)

    def segmentROI(self, src, binary_thresh, area_thresh):
        binary_image = self.binariezImage(src, binary_thresh, cv2.THRESH_BINARY)
        re_binary_image = self.removeNoise(binary_image, area_thresh)
        rect = self.getMaxBoundingRectOfContoursInImage(re_binary_image)
        roi = self.getROIWithRect(src, rect)
        return roi, rect

    def fitQuadraticCurve(self, points):

        points_yx = self.swapXY(points)
        points_hat_yx = self.polynomialFitting(points_yx, dv_quadratic)
        points_hat_xy = self.swapXY(points_hat_yx)

        return points_hat_xy
