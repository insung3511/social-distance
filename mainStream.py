import numpy as np
import utills
import plot
import time
import cv2
import os

confid = 0.5
thresh = 0.5
mouse_pts = []
encodingImg = 0

class VideoCamera(object):
    def get_frame(self):
        
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

def get_mouse_points(event, x, y, flags, param):
    global mouse_pts
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(mouse_pts) < 4:
            cv2.circle(image, (x, y), 5, (0, 0, 255), 3)
        else:
            cv2.circle(image, (x, y), 5, (255, 0, 0), 10)
        
        if len(mouse_pts) >= 1 and len(mouse_pts) <= 3:
            cv2.line(image, (x, y), (mouse_pts[len(mouse_pts)-1][0], mouse_pts[len(mouse_pts)-1][1]), (70, 70, 70), 2)
            if len(mouse_pts) == 3:
                cv2.line(image, (x, y), (mouse_pts[0][0], mouse_pts[0][1]), (70, 70, 70), 2)
        
        if "mouse_pts" not in globals():
            mouse_pts = []
        mouse_pts.append((x, y))

def calculate_social_distancing(vid_path, net, output_dir, output_vid, ln1, sleepTime):    
    count = 0
    vs = cv2.VideoCapture(vid_path)    

    height = int(vs.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = int(vs.get(cv2.CAP_PROP_FRAME_WIDTH))
    fps = int(vs.get(cv2.CAP_PROP_FPS))
    
    scale_w, scale_h = utills.get_scale(width, height)

    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    output_movie = cv2.VideoWriter("./output_vid/distancing.avi", fourcc, fps, (width, height))
    bird_movie = cv2.VideoWriter("./output_vid/bird_eye_view.avi", fourcc, fps, (int(width * scale_w), int(height * scale_h)))
        
    points = []
    global image
    global highRisk, low_Risk, safeRisk

    print("************************************")
    print("[INFO] Starting Calculating...")
    print("[RSCT] : (Risk, Waring, Safe)")    
    while True:
        (grabbed, frame) = vs.read()

        if not grabbed:
            print('here')
            break
            
        (H, W) = frame.shape[:2]
        
        if count == 0:
            while True:
                image = frame
                cv2.imshow("image", image)
                cv2.waitKey(1)
                if len(mouse_pts) == 8:
                    cv2.destroyWindow("image")
                    break
               
            points = mouse_pts
                 
        src = np.float32(np.array(points[:4]))
        dst = np.float32([[0, H], [W, H], [W, 0], [0, 0]])
        prespective_transform = cv2.getPerspectiveTransform(src, dst)

        pts = np.float32(np.array([points[4:7]]))
        warped_pt = cv2.perspectiveTransform(pts, prespective_transform)[0]
        
        distance_w = np.sqrt((warped_pt[0][0] - warped_pt[1][0]) ** 2 + (warped_pt[0][1] - warped_pt[1][1]) ** 2)
        distance_h = np.sqrt((warped_pt[0][0] - warped_pt[2][0]) ** 2 + (warped_pt[0][1] - warped_pt[2][1]) ** 2)
        pnts = np.array(points[:4], np.int32)
        cv2.polylines(frame, [pnts], True, (70, 70, 70), thickness=2)
    
        blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
        net.setInput(blob)
        start = time.time()
        layerOutputs = net.forward(ln1)
        end = time.time()
        boxes = []
        confidences = []
        classIDs = []   
    
        for output in layerOutputs:
            for detection in output:
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]
                if classID == 0:
                    if confidence > confid:
                        box = detection[0:4] * np.array([W, H, W, H])
                        (centerX, centerY, width, height) = box.astype("int")
                        x = int(centerX - (width / 2))
                        y = int(centerY - (height / 2))

                        boxes.append([x, y, int(width), int(height)])
                        confidences.append(float(confidence))
                        classIDs.append(classID)
                    
        idxs = cv2.dnn.NMSBoxes(boxes, confidences, confid, thresh)
        font = cv2.FONT_HERSHEY_PLAIN
        boxes1 = []
        for i in range(len(boxes)):
            if i in idxs:
                boxes1.append(boxes[i])
                x,y,w,h = boxes[i]
                
        if len(boxes1) == 0:
            count = count + 1
            continue
            
        person_points = utills.get_transformed_points(boxes1, prespective_transform)
        
        distances_mat, bxs_mat = utills.get_distances(boxes1, person_points, distance_w, distance_h)
        risk_count = utills.get_count(distances_mat)

        RiskList = list(risk_count)
        
        highRisk = int(str(RiskList[0]))
        low_Risk = int(str(RiskList[1]))
        safeRisk = int(str(RiskList[2]))
        print("High Risk: ", highRisk, end='')
        print("\tLow Risk: ", low_Risk, end='')
        print("\tSafe : ", safeRisk, end='')

        try:
            noneCompliance = ((int(highRisk) + int(low_Risk)) / (int(highRisk) + int(low_Risk) + int(safeRisk))) * 100
        
        except ZeroDivisionError:
            noneCompliance = 0

        print("\tNon-compliance rate : ", round(noneCompliance, 1), "%")
        frame1 = np.copy(frame)
        
        img = plot.social_distancing_view(frame1, bxs_mat, boxes1, risk_count)
        
        if count != 0:
            output_movie.write(img)
            
            cv2.imshow('CCTV View', img)
            cv2.imwrite(output_dir + "result.jpg", img)
            encodingImg = cv2.imencode('.jpg', img)

        count = count + 1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    time.sleep(sleepTime)
    vs.release()
    cv2.destroyAllWindows()
        

if __name__== "__main__":
    print("[INFO] File Direcotry Settting up...")
    
    output_dir = "./output/"
    model_path = "./models/"
    output_vid = "./output_vid/"
    print("[DIR] Output Directory: ", output_dir)
    print("[DIR] Module Directory: ", model_path)

    if model_path[len(model_path) - 1] != '/':
        model_path = model_path + '/'
    
    if output_dir[len(output_dir) - 1] != '/':
        output_dir = output_dir + '/'
    
    if output_vid[len(output_vid) - 1] != '/':
        output_vid = output_vid + '/'

    weightsPath = "models/yolov3.weights"
    configPath = "models/yolov3.cfg"
    print("[DIR] YOLOv3 Weights path: ", weightsPath)
    print("[DIR] YOLOv3 Config  path: ", configPath)

    net_yl = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
    ln = net_yl.getLayerNames()
    ln1 = [ln[i[0] - 1] for i in net_yl.getUnconnectedOutLayers()]

    cv2.namedWindow("image")
    cv2.setMouseCallback("image", get_mouse_points)
    np.random.seed(42)
    
    print("[INFO] Directory from ./data: ", os.listdir("./data"))
    sdc_path = input("[REQU] Input video Path.. \n:: ")

    if (sdc_path == "0" or sdc_path == "-1" or sdc_path == "1"):
        sdc_path = int(sdc_path)

    elif(sdc_path == "q"):
        os._exit(1)
        
    sdc_path = "./data/" + sdc_path    
    sleepTime = int(input("[REQU] Type Sleep second.. (Type int number) \n:: "))
    calculate_social_distancing(sdc_path, net_yl, output_dir, output_vid, ln1, sleepTime) 
