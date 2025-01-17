import cv2q
import numpy as np
import time
from emailing import send_email
import glob
import os

video = cv2.VideoCapture(0)
time.sleep(1)

first_frame = None
status_list = []
count = 0


def clean_folder():
    images = glob.glob("2_Intermediate_Project/app9_webcam/images/*.png")
    for image in images:
        os.remove(image)


while True:
    status = 0
    check, frame = video.read()

    # Capture image by frame

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # set to gray color
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    if first_frame is None:
        first_frame = gray_frame_gau

    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)

    thresh_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)

    # 獲得輪廓
    contours, check = cv2.findContours(
        dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    for contour in contours:
        if cv2.contourArea(contour) < 5000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

        if rectangle.any():
            status = 1

    # Use status_list to track the last two output to see if it match [1,0] << disapear
    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[0] == 1 and status_list[1] == 0:
        cv2.imwrite(f"2_Intermediate_Project/app9_webcam/images/{count}.png", frame)
        count += 1

    all_images = glob.glob("2_Intermediate_Project/app9_webcam/images/*.png")

    for image in all_images:
        if len(all_images) == 2:
            send_email(image)
            break

    cv2.imshow("Video", frame)

    key = cv2.waitKey(1)
    # when user press Q, it will terminate the programme
    if key == ord("q"):
        break


video.release()
