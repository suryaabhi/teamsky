from ARTagUtils import MarkerAction
from time import sleep

def procssReadBillBoard(bot):
    bot.read_billboard_1()

def processPickObject(bot, dir):
    bot.seek_and_pick_object(dir)
    sleep(2)

    bot.find_way_back_to_path(bot.oppositeDir(dir))
    sleep(1)

def processDropObject(bot, dir):
    bot.seek_and_drop_object(dir)
    sleep(2)

    bot.find_way_back_to_path(bot.oppositeDir(dir))
    sleep(1)

def processAruco(bot, aruco):
    # TODO: add visited 
    match aruco:
        case MarkerAction.READ_BILLBOARD_1:
            sleep(3)
            # procssReadBillBoard(bot)
        
        case MarkerAction.PICK_OBJECT_RIGHT:
            processPickObject(bot, "right")

        case MarkerAction.PICK_OBJECT_LEFT:
            processPickObject(bot, "left")

        case MarkerAction.DROP_OBJECT_LEFT:
            processDropObject(bot, "left")

        case MarkerAction.DROP_OBJECT_RIGHT:
            processDropObject(bot, "right")

