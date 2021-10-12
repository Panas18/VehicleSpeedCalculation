import cv2
import time
from tracker import EuclideanDistanceTracker


VIDEO = 'highway.mp4'
KERNEL = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
FGBG = cv2.createBackgroundSubtractorKNN()
AREA = 60
ROI = (238, 400, 173, 461, 117, 172)  # (x1, x2, x3, x4, y1, y2)
tracker = EuclideanDistanceTracker()

def background_sub(img, kernel, fgbg):
    fgmask = fgbg.apply(img)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
    return fgmask


def create_lines(img, roi):
    x1, x2, x3, x4, y1, y2 = roi
    cv2.line((img), (x1, y1), (x2, y1), (0, 255, 0))
    cv2.line(img, (x3, y2), (x4, y2), (0, 255, 0))


def calculate_fps(new_frame_time, prev_frame_time):
    new_frame_time = time.time()
    time_taken = new_frame_time - prev_frame_time
    prev_frame_time = new_frame_time
    fps = 1/time_taken
    # print(f"FPS: {fps}")
    return new_frame_time, prev_frame_time


def bounding_box(fgmask, img):
    centers = []
    contours, _ = cv2.findContours(
            fgmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > AREA:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 1)
            center = ((x+(w//2)), (y+(h//2)))
            cv2.circle(img, center, 2, (0, 0, 255), cv2.FILLED)
            centers.append(center)
    return centers


def roi_center(img, roi, centers):
    x1, x2, x3, x4,  y1, y2 = roi
    inside_roi = []
    for center in centers:
        if (center[1] >= y1 and center[1] <= y2) and (center[0] >= x3 and center[0] <= x4):
            cv2.circle((img), center, 5, (255, 0, 0), cv2.FILLED)
            inside_roi.append(center)
    return inside_roi

if __name__ == "__main__":
    new_frame_time, prev_frame_time = (0, 0)
    cap = cv2.VideoCapture(VIDEO)

    while True:
        new_frame_time, prev_frame_time = calculate_fps(
                new_frame_time, prev_frame_time)
        _, img = cap.read()
        if type(img) == type(None):
            break
        fgmask = background_sub(img, KERNEL, FGBG)
        create_lines(img, ROI)
        centers = bounding_box(fgmask, img)
        centers=roi_center(img, ROI, centers)
        tracker.update(centers)
        cv2.imshow("img", img)
        key = cv2.waitKey(27)
        if key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
