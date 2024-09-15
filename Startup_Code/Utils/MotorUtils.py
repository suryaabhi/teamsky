import RPi.GPIO as GPIO
from time import sleep
from adafruit_pca9685 import PCA9685
from adafruit_motor import motor
import board
import busio

DEFAULT_SPEED = 20

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Initialize I2C and PCA9685
i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)
pca.frequency = 50  # Set PWM frequency to 1kHz

# Define motor/servo channels on PCA9685
motors = {
    "front_right": {"channel": 15, "in1": 14, "in2": 13},
    "rear_left": {"channel": 4, "in1": 5, "in2": 6},
    "front_left": {"channel": 9, "in1": 7, "in2": 8}, 
    "rear_right": {"channel": 10, "in1": 12, "in2": 11}, 
}
servos = {
    "gripper": 3,
    "main_arm": 1, 
    "camera_tilt": 2,
}


def set_servo_angle(servo, angle):
    ### THIS IS RISKY CODE AND CAN PERMANENTLY DAMAGE THE SERVOS ###
    ### !!! NO REPLACEMENTS WILL BE PROVIDED !!! ###
    ### UNCOMMENT ONLY POST INSTRUCTIONS FROM US ###
    # Convert the angle to a duty cycle value (typically 2.5% to 12.5%)
    duty = 2.5 + (angle / 180.0) * 10
    set_pin_pwm(servo, duty)
    return


def set_pin_pwm(pin, duty):
    # Map speed from 0 to 100 to PWM range (0 to 65535)
    pwm_value = int((duty) * (65535 / 100))
    pca.channels[pin].duty_cycle = pwm_value


def move_motor(motor, direction, speed=DEFAULT_SPEED):
    # Direction value 1 is forward, -1 is backward
    set_pin_pwm(motor["channel"], speed)
    if direction == 1:
        set_pin_pwm(motor["in1"], 100)
        set_pin_pwm(motor["in2"], 0)
    elif direction == -1:
        set_pin_pwm(motor["in1"], 0)
        set_pin_pwm(motor["in2"], 100)
    else:
        set_pin_pwm(motor["in1"], 0)
        set_pin_pwm(motor["in2"], 0)


def stop(stop_servos=False):
    for motor in motors.values():
        pca.channels[motor["in1"]].duty_cycle = 0
        pca.channels[motor["in2"]].duty_cycle = 0
        pca.channels[motor["channel"]].duty_cycle = 0
    if stop_servos:
        for servo in servos.values():
            pca.channels[servo].duty_cycle = 0


def move(motor1, motor2, motor3, motor4, speed=DEFAULT_SPEED):
    move_motor(motors["front_left"], motor1, speed)
    move_motor(motors["front_right"], motor2, speed)
    move_motor(motors["rear_left"], motor3, speed)
    move_motor(motors["rear_right"], motor4, speed)
    print("Moving motors: ", motor1, motor2,
          motor3, motor4, " at speed: ", speed)


# Passing time=None will disable the time based movement
# Else it will stop after running for the specified time.

def front(time=None, speed=DEFAULT_SPEED):
    move(1, 1, 1, 1, speed)
    if time is not None:
        sleep(time)
        stop()


def back(time=None, speed=DEFAULT_SPEED):
    move(-1, -1, -1, -1, speed)
    if time is not None:
        sleep(time)
        stop()


def rotate_left(time=None, speed=DEFAULT_SPEED):
    move(-1, 1, -1, 1, speed)
    if time is not None:
        sleep(time)
        stop()


def rotate_right(time=None, speed=DEFAULT_SPEED):
    move(1, -1, 1, -1, speed)
    if time is not None:
        sleep(time)
        stop()


def strafe_left(time=None, speed=DEFAULT_SPEED):
    move(-1, 1, 1, -1, speed)
    if time is not None:
        sleep(time)
        stop()


def strafe_right(time=None, speed=DEFAULT_SPEED):
    move(1, -1, -1, 1, speed)
    if time is not None:
        sleep(time)
        stop()


def diagonal_front_left(time=None, speed=DEFAULT_SPEED):
    move(0, 1, 1, 0, speed)
    if time is not None:
        sleep(time)
        stop()


def diagonal_front_right(time=None, speed=DEFAULT_SPEED):
    move(1, 0, 0, 1, speed)
    if time is not None:
        sleep(time)
        stop()


def diagonal_back_left(time=None, speed=DEFAULT_SPEED):
    move(-1, 0, 0, -1, speed)
    if time is not None:
        sleep(time)
        stop()


def diagonal_back_right(time=None, speed=DEFAULT_SPEED):
    move(0, -1, -1, 0, speed)
    if time is not None:
        sleep(time)
        stop()


def move_gripper_to_angle(angle):
    set_servo_angle(servos["gripper"], angle)


def move_main_arm_to_angle(angle):
    set_servo_angle(servos["main_arm"], angle)


def move_camera_tilt_to_angle(angle):
    set_servo_angle(servos["camera_tilt"], angle)


def set_all_servos(main_arm_angle, camera_tilt_angle, gripper_angle=None):
    if gripper_angle is not None:
        move_gripper_to_angle(gripper_angle)
    move_main_arm_to_angle(main_arm_angle)
    move_camera_tilt_to_angle(camera_tilt_angle)


if __name__ == "__main__":
    try:
        while True:
            commands = input("Enter commands: ")
            # commands = "wxadqezcopt."
            for command in commands:
                if command == '.':
                    for servo in servos.values():
                        set_pin_pwm(servo, 2.5)
                elif command == 'w':
                    front()  # Move forward
                elif command == 'x':
                    back()  # Move backward
                elif command == 'a':
                    strafe_left()  # Strafe left
                elif command == 'd':
                    strafe_right()  # Strafe right
                elif command == 'o':
                    rotate_left()  # Rotate left
                elif command == 'p':
                    rotate_right()  # Rotate right
                elif command == 'q':
                    diagonal_front_left()  # Diagonal front left
                elif command == 'e':
                    diagonal_front_right()  # Diagonal front right
                elif command == 'z':
                    diagonal_back_left()  # Diagonal back leftw
                elif command == 'c':
                    diagonal_back_right()  # Diagonal back right
                elif command == 't':
                    # Test all motors with speeds from 10 to 100 in increments of 10
                    for speed in range(10, 101, 10):
                        move_motor(motors["front_left"], 1, speed)
                        sleep(1)
                        stop()
                        move_motor(motors["front_right"], 1, speed)
                        sleep(1)
                        stop()
                        move_motor(motors["rear_left"], 1, speed)
                        sleep(1)
                        stop()
                        move_motor(motors["rear_right"], 1, speed)
                        sleep(1)
                        stop()
                elif command == 'g':
                    while True:
                        angle = int(
                            input("Enter gripper angle (-1 to exit): "))
                        if angle < 0 or angle > 180:
                            break
                        move_gripper_to_angle(angle)
                elif command == 'h':
                    while True:
                        angle = int(
                            input("Enter main arm angle (-1 to exit): "))
                        if angle < 0 or angle > 180:
                            break
                        move_main_arm_to_angle(angle)
                elif command == 'j':
                    while True:
                        angle = int(
                            input("Enter camera tilt angle (-1 to exit): "))
                        if angle < 0 or angle > 180:
                            break
                        move_camera_tilt_to_angle(angle)
                else:
                    print("Invalid command")
                sleep(1)
                stop()

    except KeyboardInterrupt:
        stop(stop_servos=True)
        print("Program terminated")
