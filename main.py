import cv2 as cv
import time

VIDEO = 'highway.mp4'
KERNEL = cv.getStructuringElement(cv.MORPH_ELLIPSE, (2, 2))
FGBG = cv.createBackgroundSubtractorKNN()
AREA = 80


def background_sub(img, kernel, fgbg):
    fgmask = fgbg.apply(img)
    fgmask = cv.morphologyEx(fgmask, cv.MORPH_OPEN, kernel)
    return fgmask


def calculate_fps(new_frame_time, prev_frame_time):
    new_frame_time = time.time()
    time_taken = new_frame_time - prev_frame_time
    prev_frame_time = new_frame_time
    fps = 1/time_taken
    print(f"FPS: {fps}")
    return new_frame_time, prev_frame_time


def bounding_box(fgmask, img):
    contours, _ = cv.findContours(fgmask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv.contourArea(cnt)
        if area > AREA:
            cv.drawContours(img, [cnt], -1, (0, 255, 0), 2)


if __name__ == "__main__":
    try:
        new_frame_time, prev_frame_time = (0, 0)
        cap = cv.VideoCapture(VIDEO)

        while True:
            new_frame_time, prev_frame_time = calculate_fps(
                new_frame_time, prev_frame_time)
            _, img = cap.read()
            fgmask = background_sub(img, KERNEL, FGBG)
            bounding_box(fgmask, img)
            cv.imshow("bgmask", fgmask)
            cv.imshow("img", img)
            key = cv.waitKey(27)
            if key == 27:
                break

    except Exception as e:
        print(e)

    cap.release()
    cv.destroyAllWindows()
