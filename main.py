import cv2 as cv
import time

cap = cv.VideoCapture("cars.mp4")
prev_frame_time = 0
new_frame_time = 0

try:
    while cap.isOpened():
        _, img = cap.read()
        height, width = img.shape[0] // 2, img.shape[1]//2
        dim = (width, height)
        resized = cv.resize(img, dim, interpolation=cv.INTER_AREA)
        cv.imshow("frame", resized)
        new_frame_time = time.time()
        time_taken = new_frame_time - prev_frame_time
        prev_frame_time = new_frame_time
        print(f"Fps {1/time_taken}")
        if cv.waitKey(12) & 0xff == ord("q"):
            break

    cap.release()
    cv.destroyAllWindows()

except AttributeError:
    pass
