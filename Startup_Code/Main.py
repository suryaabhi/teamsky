from Bot import Bot
from time import sleep
from Utils.MotorUtils import stop,front
from ArucoProcessor import processAruco

def Run():
    bot = Bot()

    while True:
        bot.read_billboard_1()
        # sleep(1)
        #processAruco(bot, aruco)
    

if __name__ == "__main__":
    try:
        Run()
    except KeyboardInterrupt:
        stop(1)
        print("Program terminated")

