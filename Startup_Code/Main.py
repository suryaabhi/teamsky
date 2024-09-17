from Bot import Bot
from time import sleep
from Utils.MotorUtils import stop,front
from ArucoProcessor import processAruco

def Run():
    bot = Bot()
    # bot.follow_line()
    # sleep(2)
    # front(0.4)
    # sleep(2)
    # bot.seek_and_pick_object("left")
    # sleep(2)
    # bot.find_way_back_to_path("right")
    # sleep(1)
    # bot.follow_line()
    # sleep(2)
    # bot.seek_and_drop_object("right")
    # sleep(1)
    # bot.find_way_back_to_path("left")
    # sleep(1)
    # bot.follow_line()
    # sleep(2)

    while True:
        aruco = bot.follow_line()
        sleep(1)
        processAruco(bot, aruco)
    
    
    # # Follow path
    # aruco = Bot.follow_line()
    # # bot stopped at AR marker 1/2 and turns left/right
    # direction = None
    # if aruco == 1:
    #     direction = "left"
    # elif aruco == 2:
    #     direction = "right"
    # # Find the object to pick
    # Bot.seek_and_pick_object(direction)
    # # Find the way back to path using orange dot (or any other marker specified)
    # Bot.find_way_back_to_path()
    # # Follow path
    # aruco = Bot.follow_line()
    # # bot stopped at AR marker 3/4 and turns left/right
    # direction = None
    # if aruco == 3:
    #     direction = "left"
    # elif aruco == 4:
    #     direction = "right"
    # # Drop the object at the shape and colour specified
    # Bot.seek_and_drop_object(direction)
    # # Find the way back to path using orange dot (or any other marker specified)
    # Bot.find_way_back_to_path()
    # # Follow path
    # aruco = Bot.follow_line()
    # # bot stopped at AR marker 5
    # if aruco == 5:
    #     pass
    # # Read Billboard 2 which contains puzzle to decide left/right/straight path
    # Bot.read_billboard_2()
    # # Follow path
    # Bot.follow_line()
    # # bot stopped at AR marker 6 for intersection
    # # maneuver the bot to the path specified
    # Bot.move_to_answer_path()
    # # Follow path
    # aruco = Bot.follow_line()
    # # bot stopped at AR marker 7
    # if aruco == 7:
    #     pass
    # # Read Billboard 3 which contains a question to decide what to draw
    # Bot.read_billboard_3()
    # # Follow path
    # aruco = Bot.follow_line()
    # # bot stopped at AR marker 8
    # if aruco == 8:
    #     pass
    # # Draw the object/characters specified
    # Bot.draw_object()
    # # end of path

if __name__ == "__main__":
    try:
        Run()
    except KeyboardInterrupt:
        stop(1)
        print("Program terminated")

