#!/usr/bin/python
# -*- coding: utf8 -*-
import os
import sys

import face_recognition
from PIL import Image, ImageDraw
import pickle
from cv2 import cv2



# face_enc = face_recognition.face_encodings(face_img)
# result = face_recognition.compare_faces([face_enc], known_encodings[item])
# data = {
#     "name": name,
#     "encodings": known_encodings
# }
#
# with open(f"{name}_encodings.pickle", "wb") as file:
#     file.write(pickle.dumps(data))


def detect_person_in_video():
    cap = cv2.VideoCapture("My.mp4")
    count = 0

    if not os.path.exists("dataset_from_video"):
        os.mkdir("dataset_from_video")

    while True:
        ret, frame = cap.read()
        fps = cap.get(cv2.CAP_PROP_FPS)
        multiplier = int(fps)

        if ret:
            frame_id = int(round(cap.get(1)))

            cv2.imshow("Video", frame)
            k = cv2.waitKey(20)

            if frame_id % multiplier == 0:
                cv2.imwrite(f"dataset_from_video/{count}.jpg", frame)

                people_face_img = face_recognition.load_image_file(f"dataset_from_video/{count}.jpg")
                people_face_location = face_recognition.face_locations(people_face_img)

                if people_face_location:
                    top, right, bottom, left = people_face_location[0]

                    face_img = people_face_img[top:bottom, left:right]

                    pil_img = Image.fromarray(face_img)
                    pil_img.save(f"dataset_from_video/faces/{count}_face_img.jpg")
                    os.remove(f"dataset_from_video/{count}.jpg")
                    count += 1

                    try:
                        data = pickle.loads(open("Person_name_encodings.pickle", "rb").read())
                    except Exception:
                        print("У вас ещё нет никаких данных")
                        data = []



                elif len(people_face_location) > 1:
                    print("Программа не поддерживает два лица в кадре. Пусть кто-то отойдёт!")
                    os.remove(f"dataset_from_video/{count}.jpg")

                else:
                    os.remove(f"dataset_from_video/{count}.jpg")

            # if k == ord(" "):
            #     cv2.imwrite(f"dataset_from_video/{count}_extra_scr.jpg", frame)
            #     print(f"Take an extra screenshot {count}")
            #     count += 1

            if k == ord("q"):
                print("Q pressed, closing the app")
                break

        else:
            print("[Error] Can't get the frame...")
            break


def main():
    detect_person_in_video()


if __name__ == "__main__":
    main()