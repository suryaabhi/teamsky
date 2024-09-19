from Utils.ARTagUtils import MarkerAction
from time import sleep
import Bot

def processReadBillBoard1(bot: Bot):
    bot.read_billboard_1()

def processPickObject(bot, dir):
    bot.seek_and_pick_object(dir)
    sleep(2)

    bot.find_way_back_to_path_ultrasonic(bot.oppositeDir(dir))
    sleep(1)

def processDropObject(bot, dir):
    bot.seek_and_drop_object(dir)
    sleep(2)

    bot.find_way_back_to_path_ultrasonic(bot.oppositeDir(dir))
    sleep(1)

def processReadBillboard2(bot: Bot):
    bot.read_billboard_2()

def processReadBillboard3(bot: Bot):
    bot.read_billboard_3()

def processLane(bot):
    bot.execute_lane()

def processPickAndWrite(bot, dir):
    bot.seek_and_pick_object("left", True)
    sleep(2)

    bot.write()
    sleep(1)



def processAruco(bot, aruco):
    # TODO: add visited 
    match aruco:
        case MarkerAction.READ_BILLBOARD_1:
            processReadBillBoard1(bot)
            sleep(2)
        
        case MarkerAction.PICK_OBJECT_RIGHT:
            processPickObject(bot, "right")

        case MarkerAction.PICK_OBJECT_LEFT:
            processPickObject(bot, "left")

        case MarkerAction.DROP_OBJECT_LEFT:
            processDropObject(bot, "left")

        case MarkerAction.DROP_OBJECT_RIGHT:
            processDropObject(bot, "right")

        case MarkerAction.READ_BILLBOARD_2:
            processReadBillboard2(bot)
            sleep(2)

        case MarkerAction.EXECUTE_LANE:
            processLane(bot)
            sleep(2)

        case MarkerAction.READ_BILLBOARD_3:
            processReadBillboard3(bot)
            sleep(2)

        case MarkerAction.WRITE_LETTER:
            processPickAndWrite(bot)
            sleep(2)

        case _:
            print('No action')
            sleep(1)
            bot.moveForward(0.3)

