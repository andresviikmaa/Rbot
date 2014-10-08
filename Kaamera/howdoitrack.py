#!/usr/bin/env python

import cv2

class Target:

    def __init__(self):
        #self.capture = cv2.CaptureFromCAM(0)
        ret, self.capture = cap.read()
        cv2.NamedWindow("Target", 1)

    def run(self):
        # Capture first frame to get size
        frame = cv2.QueryFrame(self.capture)
        frame_size = cv2.GetSize(frame)
        color_image = cv2.CreateImage(cv2.GetSize(frame), 8, 3)
        grey_image = cv2.CreateImage(cv2.GetSize(frame), cv2.IPL_DEPTH_8U, 1)
        moving_average = cv2.CreateImage(cv2.GetSize(frame), cv2.IPL_DEPTH_32F, 3)

        first = True

        while True:
            closest_to_left = cv2.GetSize(frame)[0]
            closest_to_right = cv2.GetSize(frame)[1]

            color_image = cv2.QueryFrame(self.capture)

            # Smooth to get rid of false positives
            cv2.Smooth(color_image, color_image, cv2.CV_GAUSSIAN, 3, 0)

            if first:
                difference = cv2.CloneImage(color_image)
                temp = cv2.CloneImage(color_image)
                cv2.ConvertScale(color_image, moving_average, 1.0, 0.0)
                first = False
            else:
                cv2.RunningAvg(color_image, moving_average, 0.020, None)

            # Convert the scale of the moving average.
            cv2.ConvertScale(moving_average, temp, 1.0, 0.0)

            # Minus the current frame from the moving average.
            cv2.AbsDiff(color_image, temp, difference)

            # Convert the image to grayscale.
            cv2.CvtColor(difference, grey_image, cv2.CV_RGB2GRAY)

            # Convert the image to black and white.
            cv2.Threshold(grey_image, grey_image, 70, 255, cv2.CV_THRESH_BINARY)

            # Dilate and erode to get people blobs
            cv2.Dilate(grey_image, grey_image, None, 18)
            cv2.Erode(grey_image, grey_image, None, 10)

            storage = cv2.CreateMemStorage(0)
            contour = cv2.FindContours(grey_image, storage, cv2.CV_RETR_CCOMP, cv2.CV_CHAIN_APPROX_SIMPLE)
            points = []

            while contour:
                bound_rect = cv2.BoundingRect(list(contour))
                contour = contour.h_next()

                pt1 = (bound_rect[0], bound_rect[1])
                pt2 = (bound_rect[0] + bound_rect[2], bound_rect[1] + bound_rect[3])
                points.append(pt1)
                points.append(pt2)
                cv2.Rectangle(color_image, pt1, pt2, cv2.CV_RGB(255,0,0), 1)

            if len(points):
                center_point = reduce(lambda a, b: ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2), points)
                cv2.Circle(color_image, center_point, 40, cv2.CV_RGB(255, 255, 255), 1)
                cv2.Circle(color_image, center_point, 30, cv2.CV_RGB(255, 100, 0), 1)
                cv2.Circle(color_image, center_point, 20, cv2.CV_RGB(255, 255, 255), 1)
                cv2.Circle(color_image, center_point, 10, cv2.CV_RGB(255, 100, 0), 1)

            cv2.ShowImage("Target", color_image)

            # Listen for ESC key
            c = cv2.WaitKey(7) % 0x100
            if c == 27:
                break

if __name__=="__main__":
    t = Target()
    t.run()
