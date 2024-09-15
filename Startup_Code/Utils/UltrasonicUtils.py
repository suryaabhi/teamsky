import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
# GPIO pin numbers for the ultrasonic sensor
TRIG_PIN = 17  # Equivalent to pin 11
ECHO_PIN = 27  # Equivalent to pin 13
# Threshold distance in centimeters
THRESHOLD_DISTANCE_CM = 20


def get_distance():
    GPIO.output(TRIG_PIN, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, GPIO.LOW)

    pulse_start = pulse_end = 0
    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    speed_of_sound = 34300  # Speed of sound in cm/s
    distance = (pulse_duration * speed_of_sound) / 2
    return distance

#before editing check outlier detection part
RUNS = 10

def getNormalizedDistance():
    d = []
    for i in range(RUNS):
        d.append(round(get_distance(), 2))
    
    d.sort()
    d = d[2:-2]
    ret = sum(d) / len(d)
    print("normalized distance", ret)
    return ret


GPIO.setmode(GPIO.BCM)

GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

GPIO.output(TRIG_PIN, GPIO.LOW)


if __name__ == "__main__":
    try:
        while True:
            distance = get_distance()
            print("Distance: " + str(distance))
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Program terminated")
        GPIO.cleanup()
