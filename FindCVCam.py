import cv2

camCnt = 0
print("[INFO] Webcam Counting Start..")

while True:
    cap = cv2.VideoCapture(camCnt)
    try:
        if (cap.isOpened()):
            print("[FIND] Camera count : ", camCnt)
    except OpenCVCamFailed as o:
        print(o)

    camCnt = camCnt + 1
    if (camCnt == 400):
        break

cap.release()
