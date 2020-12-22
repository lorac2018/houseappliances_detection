

import cv2
import numpy as np

# Load Yolo
net = cv2.dnn.readNet("yolo.weights", "yolo.cfg")
classes = []
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

colors = np.random.uniform(0, 255, size=(len(classes), 3))

# Loading web cam
camera = cv2.VideoCapture(0)

frame_id = 0

while True:
    _, img = camera.read()
    height, width, channels = img.shape

    # Detecting objects
    blob = cv2.dnn.blobFromImage(img, 0.00392, (320, 320), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)
    print(outs[1])

    # Showing informations on the screen/ get confidence score of algorithm in detecting an object in blob
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.7:
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])  # put all rectangle areas

                confidences.append(
                    float(confidence))  # how confidence was that object detected and show that percentage
                print(confidences)
                class_ids.append(class_id)  # name of the object that was detected

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.4, 0.6)

    font = cv2.FONT_HERSHEY_PLAIN
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            color = colors[i]
            confidence = confidences[i]
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            cv2.putText(img, label + " " + str(round(confidence, 2)), (x, y + 30), font, 1, (255, 255, 255), 2)



    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == 27:
        break

camera.release()
cv2.destroyAllWindows()
