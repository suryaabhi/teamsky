DEBUG_MODE = True

import cv2
import math

from flask import Flask, render_template, Response
from flask_socketio import SocketIO
from picamera2 import Picamera2

import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

import ImageUtils

if not DEBUG_MODE:
    import MotorUtils

async_mode = None
app = Flask(__name__)
socketio = SocketIO(app, async_mode=async_mode)

def gen_frames():  
    while True:
        frame = ImageUtils.get_frame()  # Capture frame using your get_frame function
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB
        ret, buffer = cv2.imencode('.jpg', frame)  # Encode frame to JPEG
        frame = buffer.tobytes()  # Convert to bytes
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def get_direction_and_speed(x, y):
    # Calculate the magnitude of the joystick displacement
    speed = math.sqrt(x**2 + y**2)
 
    # Calculate the angle in degrees
    angle = math.degrees(math.atan2(y, x))
 
    # Normalize the angle to be between 0 and 360 degrees
    if angle < 0:
        angle += 360
 
    # Determine the direction based on the angle
    if 337.5 <= angle or angle < 22.5:
        direction = 'E'
    elif 22.5 <= angle < 67.5:
        direction = 'NE'
    elif 67.5 <= angle < 112.5:
        direction = 'N'
    elif 112.5 <= angle < 157.5:
        direction = 'NW'
    elif 157.5 <= angle < 202.5:
        direction = 'W'
    elif 202.5 <= angle < 247.5:
        direction = 'SW'
    elif 247.5 <= angle < 292.5:
        direction = 'S'
    elif 292.5 <= angle < 337.5:
        direction = 'SE'
 
    return direction, speed

@app.route('/')
def home():
    return render_template('index.html', async_mode=socketio.async_mode)

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@socketio.event
def stop(message):
    print("Stopping")
    if not DEBUG_MODE:
        MotorUtils.stop()

@socketio.event
def gripper(isGripped):
    if isGripped:
        print("Opening gripper")
        if not DEBUG_MODE:
            # [TODO] Get the correct angles for opening the gripper
            MotorUtils.set_servo_angle(MotorUtils.servos["gripper"], 120)
    else:
        print("Closing gripper")
        if not DEBUG_MODE:
            # [TODO] Get the correct angles for opening the gripper
            MotorUtils.set_servo_angle(MotorUtils.servos["gripper"], 70)

@socketio.event
def bottomElbowArticulate(articulation):
    print("Bottom elbow:", articulation)
    if not DEBUG_MODE:
        MotorUtils.set_servo_angle(MotorUtils.servos["main_arm"], float(articulation))

@socketio.event
def topElbowArticulate(articulation):
    print("Top elbow:", articulation)
    if not DEBUG_MODE:
        MotorUtils.set_servo_angle(MotorUtils.servos["camera_tilt"], float(articulation))

@socketio.event
def rotateLeft(message):
    print("Rotating left")
    if not DEBUG_MODE:
        MotorUtils.move(-1, 1, -1, 1)


@socketio.event
def rotateRight(message):
    print("Rotating right")
    if not DEBUG_MODE:
        MotorUtils.move(1, -1, 1, -1)

@socketio.event
def joystick_position_changed(message):
    x = int(message['data']['x'])/100.0
    y = int(message['data']['y'])/100.0

    direction, speed = get_direction_and_speed(x, y)

    if x == 0.0 and y == 0.0:
        print("Stopping")
        if not DEBUG_MODE:
            MotorUtils.stop()
    elif direction == 'N':
        print("Moving forward")
        if not DEBUG_MODE:
            MotorUtils.move(1, 1, 1, 1)
    elif direction == 'S':
        print("Moving backward")
        if not DEBUG_MODE:
            MotorUtils.move(-1, -1, -1, -1)
    elif direction == 'W':
        print("Strafing left")
        if not DEBUG_MODE:
            MotorUtils.move(-1, 1, 1, -1)
    elif direction == 'E':
        print("Strafing right")
        if not DEBUG_MODE:
            MotorUtils.move(1, -1, -1, 1)
    elif direction == 'NW':
        print("Moving forward and left")
        if not DEBUG_MODE:
            MotorUtils.move(0, 1, 1, 0)
    elif direction == 'NE':
        print("Moving forward and right")
        if not DEBUG_MODE:
            MotorUtils.move(1, 0, 0, 1)
    elif direction == 'SW':
        print("Moving backward and left")
        if not DEBUG_MODE:
            MotorUtils.move(-1, 0, 0, -1)
    elif direction == 'SE':
        print("Moving backward and right")
        if not DEBUG_MODE:
            MotorUtils.move(0, -1, -1, 0)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=False)
