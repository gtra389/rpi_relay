#!/usr/bin/python
# -*- coding:utf-8 -*-
##################################################

#       P26 ----> Relay_Ch1
#	    P20 ----> Relay_Ch2
#	    P21 ----> Relay_Ch3

##################################################

import RPi.GPIO as GPIO
import os
#from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import BaseHTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler
import SocketServer
from threading import Condition
import io
import picamera


host_name = '0.0.0.0'    # Change this to your Raspberry Pi IP address
host_port = 8080

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Create a dictionary called pins to store the pin number, name, and pin state:
pins = [26, 20, 21]

# Set each pin as an output and make it low:
for pin in pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
print("Initiation is done.")
print("")


# Configuration of Pi camera
class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf) 


class MyServerHandler(BaseHTTPRequestHandler):
    """ A special implementation of BaseHTTPRequestHander for reading data from
        and control GPIO of a Raspberry Pi
    """

    def do_HEAD(self):
        """ do_HEAD() can be tested use curl command 
            'curl -I http://server-ip-address:port' 
        """
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        """ do_GET() can be tested using curl command 
            'curl http://server-ip-address:port' 
        """
        html = '''
            <head>
            <title>RPi Web Server</title>
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" integrity="sha384-1q8mTJOASx8j1Au+a5WDVnPi2lkFfwwEAa8hDDdjZlpLegxhjVME1fgjWPGmkzs7" crossorigin="anonymous">
            <!-- Optional theme -->
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap-theme.min.css" integrity="sha384-fLW2N01lMqjakBkx3l/M9EahuwpSfeNvV63J5ezn3uZzapT0u7EYsXMjQV+0En5r" crossorigin="anonymous">
            <!-- Latest compiled and minified JavaScript -->
            <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js" integrity="sha384-0mSbJDEHialfmuBBQP6A4Qrprq5OVfW37PRR3j5ELqxss1yVqOtnepnHVP9aJ7xS" crossorigin="anonymous"></script>
            </head>

            <body style="width:960px; margin: 20px auto;">
            <p>Current GPU temperature is {}</p>
            <p>Turn Relay Channel 1: <a href="/index.html/ch1_on">ON</a> <a href="/index.html/ch1_off">OFF</a></p>
            <p>Turn Relay Channel 2: <a href="/index.html/ch2_on">ON</a> <a href="/index.html/ch2_off">OFF</a></p>
            <p>Turn Relay Channel 3: <a href="/index.html/ch3_on">ON</a> <a href="/index.html/ch3_off">OFF</a></p>
            <p>Current status</p>
            <div id="current-status"></div>
            <script>
                document.getElementById("current-status").innerHTML="{}";
            </script>

            <h1>PiCamera MJPEG Streaming Demo</h1>
            <img src="stream.mjpg" width="640" height="480" />

            </body>
            </html>
        '''
        temp = os.popen("/opt/vc/bin/vcgencmd measure_temp").read()
        self.do_HEAD()
        status = ''
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
            
        elif self.path == '/index.html':
            content = html.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)

        elif self.path == '/stream.mjpg':                
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
    
        elif self.path=='/index.html/ch1_on':
            GPIO.output(26, GPIO.HIGH)
            status='Relay Channel 1 is On'
        elif self.path=='/index.html/ch1_off':
            GPIO.output(26, GPIO.LOW)
            status='Relay Channel 1 is Off'
        # elif self.path=='/ch2_on':
        #     GPIO.output(20, GPIO.HIGH)
        #     status='Relay Channel 2 is On'
        # elif self.path=='/ch2_off':
        #     GPIO.output(20, GPIO.LOW)
        #     status='Relay Channel 2 is Off'
        # elif self.path=='/ch3_on':
        #     GPIO.output(21, GPIO.HIGH)
        #     status='Relay Channel 3 is On'
        # elif self.path=='/ch3_off':
        #     GPIO.output(21, GPIO.LOW)
        #     status='Relay Channel 3 is Off'
        else:
            self.send_error(404)
            self.end_headers()        

        self.wfile.write(html.format(temp[5:], status).encode("utf-8"))

class StreamingServer(SocketServer.ThreadingMixIn, BaseHTTPServer.HTTPServer):
	allow_reuse_address = True
	daemon_threads = True

with picamera.PiCamera(resolution='640x480', framerate=24) as camera:
    output = StreamingOutput()
    camera.start_recording(output, format='mjpeg')
    try:
        address = (host_name, host_port)
        http_server = StreamingServer(address, MyServerHandler)
        print("Server Starts - %s:%s" % (host_name, host_port))
        server.serve_forever()

    except KeyboardInterrupt:
		http_server.server_close()

    finally:
        camera.stop_recording()