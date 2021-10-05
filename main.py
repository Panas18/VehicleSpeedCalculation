import cv2 as cv
import time

cap = cv.VideoCapture("cars.mp4")
prev_frame_time = 0
new_frame_time = 0
count = 0

while cap.isOpened():
    _, img = cap.read()
    new_frame_time = time.time()
    fps = 1/(new_frame_time - prev_frame_time)
    prev_frame_time = new_frame_time
    fps = str(int(fps))
    if count % 5 == 0:
        cv.putText(img, fps, (100, 100), cv.FONT_HERSHEY_SIMPLEX,
                   3, (100, 255, 0), 3, cv.LINE_AA)
    height, width = img.shape[0] // 2, img.shape[1]//2
    dim = (width, height)
    resized = cv.resize(img, dim, interpolation=cv.INTER_AREA)
    count += 1
    #cv.imshow("frame", img)
    cv.imshow("frame", resized)
    if cv.waitKey(1) & 0xff == ord("q"):
        break

cap.release()
cv.destroyAllWindows()
