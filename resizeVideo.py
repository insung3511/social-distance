import numpy as np
import cv2
import os

print("[INFO] Directory from ./data: ", os.listdir("./data"))
sdc_path = input("[REQU] Input video Path.. \n:: ")
sdc_path = "./data/" + sdc_path

cap = cv2.VideoCapture(sdc_path)

output_vid = input("[REQU] Type output video name.. ex) output.mov, result.mp4 \n:: ")
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(output_vid, fourcc, 5, (1280,720))

print("[INFO] Starting resizing")

while True:
	print(".", end='')
	ret, frame = cap.read()
	if (ret == True):
		print("!", end='')
		b = cv2.resize(frame, (1280, 720), fx=0, fy=0, interpolation=cv2.INTER_CUBIC)
		out.write(b)

	else:
		print("?", end='')
		break

cap.release()
out.release()
