from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from picamera2 import Picamera2
import io
import threading
import time

# Initialize camera
picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(main={"size": (640, 480)}))
picam2.start()

# Global JPEG frame storage
frame = None
lock = threading.Lock()

def capture_frames():
    global frame
    while True:
        buffer = io.BytesIO()
        picam2.capture_file(buffer, format='jpeg')
        with lock:
            frame = buffer.getvalue()
        time.sleep(0.05)  # ~20fps

class StreamingHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"""
                <html>
                  <head><title>Raspberry Pi Camera</title></head>
                  <body>
                    <h1>Live Stream</h1>
                    <img src="/stream.mjpg" />
                  </body>
                </html>
            """)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with lock:
                        if frame is None:
                            continue
                        output = frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.wfile.write(b'Content-Type: image/jpeg\r\n\r\n')
                    self.wfile.write(output)
                    self.wfile.write(b'\r\n')
                    time.sleep(0.05)
            except Exception as e:
                print(f"Client disconnected: {e}")
        else:
            self.send_error(404)
            self.end_headers()

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

if __name__ == '__main__':
    # Start frame capture thread
    t = threading.Thread(target=capture_frames)
    t.daemon = True
    t.start()

    # Start HTTP server
    address = ('', 8000)  # 0.0.0.0:8000
    server = ThreadedHTTPServer(address, StreamingHandler)
    print("Server started at http://<your-pi-ip>:8000")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        picam2.stop()
        server.server_close()
