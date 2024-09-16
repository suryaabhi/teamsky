from Bot import Bot
from time import sleep
from Utils.MotorUtils import stop

def Run():
    bot = Bot()
    bot.find_way_back_to_path()
    sleep(1)
    bot.follow_line()
    sleep(5)
    # # while True:
    #     # bot.follow_line()
    #     # sleep(5)


    #  ## start here   
    # # Follow path
    # aruco = Bot.follow_line()
    # # bot stopped at AR marker 0
    # if aruco == 0:
    #     pass
    # # Read Billboard 1 which contains pick and drop instructions
    # Bot.read_billboard_1()
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

