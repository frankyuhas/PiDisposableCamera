from picamera2 import Picamera2, Preview
from picamera2.encoders import MJPEGEncoder
from picamera2.outputs import FileOutput
import io

picam2 = Picamera2()
video_config = picam2.create_video_configuration()
picam2.configure(video_config)
#picam2.start_preview(Preview.QT)

# Start an MJPEG HTTP server on port 8000
picam2.start_recording(MJPEGEncoder(), FileOutput("server:8000"))

try:
    print("Camera stream running at http://<raspberrypi-ip>:8000")
    while True:
        pass  # keep alive
except KeyboardInterrupt:
    pass
finally:
    picam2.stop_recording()
