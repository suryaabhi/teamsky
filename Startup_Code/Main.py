from Bot import Bot
from time import sleep

def Run():
    bot = Bot()
    # bot.follow_line()
    sleep(3)
    bot.seek_object("right")


if __name__ == "__main__":
    Run()