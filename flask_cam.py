from flask import Flask, render_template_string, Response, send_file
from picamera2 import Picamera2, Preview
from picamera2.encoders import MJPEGEncoder
from picamera2.outputs import FileOutput
from datetime import datetime
import io

app = Flask(__name__)
picam2 = Picamera2()

# Configure video mode
video_config = picam2.create_video_configuration(main={"size": (640, 480)})
picam2.configure(video_config)
picam2.start()

picam2.set_controls({"AfMode": 2,"AfTrigger":0})  # Continuous autofocus
time.sleep(2)  # Allow camera to warm up


TEMPLATE = """
<html>
<head><title>Raspberry Pi Camera</title></head>
<body>
  <h1>Raspberry Pi Zero 2 Camera</h1>
  <img src="{{ url_for('video_feed') }}">
  <br><br>
  <a href="{{ url_for('capture') }}"><button>Capture Photo</button></a>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(TEMPLATE)

def gen_frames():
    stream = io.BytesIO()
    while True:
        stream.seek(0)
        picam2.capture_file(stream, format='jpeg')
        frame = stream.getvalue()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/capture')
def capture():
    filename = f"/home/picamera/capture_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    picam2.capture_file(filename)
    return send_file(filename, mimetype='image/jpeg')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)
