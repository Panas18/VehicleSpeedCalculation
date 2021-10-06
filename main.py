import cv2 as cv
import time

new_frame_time, prev_frame_time = (0, 0)
dim = (960, 540)
cap = cv.VideoCapture("cars.mp4")


def calculate_fps(new_frame_time, prev_frame_time):
    new_frame_time = time.time()
    time_taken = new_frame_time - prev_frame_time
    prev_frame_time = new_frame_time
    fps = 1/time_taken
    print(f"FPS: {fps}")
    return new_frame_time, prev_frame_time


def create_lines(img, a1=357, a2=232, b1=159, b2=279,
                 c1=467, c2=260, d1=324, d2=341):
    color = (0, 255, 0)
    cv.line(img, (a1, a2), (c1, c2), color, 1)
    cv.line(img, (a1, a2), (b1, b2), color, 1)
    cv.line(img, (c1, c2), (d1, d2), color, 1)
    cv.line(img, (b1, b2), (d1, d2), color, 1)


if __name__ == "__main__":
    try:
        while cap.isOpened():
            new_frame_time, prev_frame_time = calculate_fps(
                new_frame_time, prev_frame_time)
            _, img = cap.read()
            resized = cv.resize(img, dim, interpolation=cv.INTER_AREA)
            create_lines(resized)
            cv.imshow("frame", resized)
            if cv.waitKey(12) & 0xff == ord("q"):
                break

    except Exception as e:
        print(e)

    cap.release()
    cv.destroyAllWindows()
