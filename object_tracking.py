import cv2
import imutils

# Initialize the first frame for comparison
firstFrame = None
is_streaming = True

def process_frame(frame):
    global firstFrame

    # Resize the frame, convert it to grayscale, and blur it
    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # If the first frame is None, initialize it
    if firstFrame is None:
        firstFrame = gray
        return frame

    # Compute the absolute difference between the current frame and first frame
    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

    # Dilate the thresholded image to fill in holes, then find contours
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    text = "Normal"
    for c in cnts:
        if cv2.contourArea(c) < 500:
            continue

        # Compute the bounding box for the contour, draw it on the frame, and update the text
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        text = "Moving Object detected"

    cv2.putText(frame, text, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    return frame

def generate_frames():
    global is_streaming
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("Error: Could not open camera.")
        return

    while True:
        if not is_streaming:
            cam.release()
            return

        ret, frame = cam.read()
        if not ret:
            break
        frame = process_frame(frame)
        _, jpeg = cv2.imencode('.jpg', frame)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    cam.release()
