from flask import Flask, render_template, Response, request, redirect, url_for
import cv2

# IMPORTANT:
# this only works if you run nmcli device wifi hotspot ssid autonet password mypass123
# the pass would be mypass123 btw if you didnt catch that!

# if connection refused:
# sudo firewall-cmd --add-port=5000/tcp --zone=nm-shared --permanent
# sudo firewall-cmd reload

# uses opencv
# pip install opencv-python

app = Flask(__name__)

def list_cameras(max_tested=5):
    cams = []
    for i in range(max_tested):
        cap = cv2.VideoCapture(i)
        if cap.read()[0]:
            cams.append(i)
        cap.release()
    return cams

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/webcamwatch")
def webcamwatch():
    cams = list_cameras()
    return render_template("webcamwatch.html", cameras=cams)

@app.route("/capture")
def capture():
    cam_id = int(request.args.get("cam", 0))
    cap = cv2.VideoCapture(cam_id)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        return "Camera capture failed"

    ret, jpeg = cv2.imencode('.jpg', frame)

    return Response(
        jpeg.tobytes(),
        mimetype='image/jpeg'
    )

if __name__ == '__main__':
    # 0.0.0.0 makes it listen to anything on the custom wifi
    app.run(host='0.0.0.0', port=5000)
