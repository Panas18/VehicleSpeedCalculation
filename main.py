import cv2 as cv
import time

KERNEL = cv.getStructuringElement(cv.MORPH_ELLIPSE, (2, 2))
FGBG = cv.createBackgroundSubtractorKNN()
DIM = (960, 540)


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


def create_lines(img, a1=357, a2=232, b1=159, b2=279,
                 c1=467, c2=260, d1=324, d2=341):
    color = (255, 255, 255)
    cv.line(img, (a1, a2), (c1, c2), color, 1)
    cv.line(img, (a1, a2), (b1, b2), color, 1)
    cv.line(img, (c1, c2), (d1, d2), color, 1)
    cv.line(img, (b1, b2), (d1, d2), color, 1)


if __name__ == "__main__":
    try:
        new_frame_time, prev_frame_time = (0, 0)
        cap = cv.VideoCapture("cars.mp4")

        while cap.isOpened():
            new_frame_time, prev_frame_time = calculate_fps(
                new_frame_time, prev_frame_time)
            _, img = cap.read()
            resized = cv.resize(img, DIM, interpolation=cv.INTER_AREA)
            fgmask = background_sub(resized, KERNEL, FGBG)
            create_lines(fgmask)
            cv.imshow("bgmask", fgmask)
            cv.imshow("img", resized)
            if cv.waitKey(1) & 0xff == ord("q"):
                break

    except Exception:
        # print(e)
        pass

    cap.release()
    cv.destroyAllWindows()
