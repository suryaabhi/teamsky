from Utils.MotorUtils import move, stop, DEFAULT_SPEED
from time import sleep
from Utils.MotorUtils import front, rotate_right, rotate_left, back, strafe_left, strafe_right, stop, diagonal_back_left, diagonal_back_right, diagonal_front_left, diagonal_front_right
from Utils.ServoUtils import pen_up, pen_down
 
def front_(num=1, time=None, speed=DEFAULT_SPEED):
    num = num/4
    front(num, speed)
   
def back_(num=1, time=None, speed=DEFAULT_SPEED):
    num = num/4
    back(num, speed)
 
def rotate_left_(num=1, time=None, speed=DEFAULT_SPEED):
    num = num/4
    rotate_left(num, speed)
 
def rotate_right_(num=1, time=None, speed=DEFAULT_SPEED):
    num = num/4
    rotate_right(num, speed)
 
def strafe_left_(num=1, time=None, speed=DEFAULT_SPEED):
    num = num/4
    speed = speed*2
    strafe_left(num, speed)
 
def strafe_right_(num=1, time=None, speed=DEFAULT_SPEED):
    num = num/4
    speed = speed*2
    strafe_right(num, speed)
 
def diagonal_front_left_(num=1, time=None, speed=DEFAULT_SPEED):
    num = num/4
    diagonal_front_left(num, speed)
 
def diagonal_front_right_(num=1, time=None, speed=DEFAULT_SPEED):
    num = num/4
    diagonal_front_right(num, speed)
 
def diagonal_back_left_(num=1, time=None, speed=DEFAULT_SPEED):
    num = num/4
    diagonal_back_left(num, speed)
       
def diagonal_back_right_(num=1, time=None, speed=DEFAULT_SPEED):
    num = num/4
    diagonal_back_right(num, speed)
 
def up_(num=1, time=None, speed=DEFAULT_SPEED):
    pen_up()
    return
 
def down_(num=1, time=None, speed=DEFAULT_SPEED):
    pen_down()
    return
 
def movement():
    mov_dict = {
        "forward": front_,
        "backward": back_,
        "strafe_left": strafe_left_,
        "strafe_right": strafe_right_,
        "rotate_left": rotate_left_,
        "rotate_right": rotate_right_,
        "diagonal_front_left": diagonal_front_left_,
        "diagonal_front_right": diagonal_front_right_,
        "diagonal_back_left": diagonal_back_left_,
        "diagonal_back_right": diagonal_back_right_,
        "up": up_,
        "down": down_,
        }
    return mov_dict
 
def write_letter(letter, k = 1 , gap = 1):
    letter = letter.lower()
    movements = movement()
 
    gap = gap*k
    letter_movements = {
        'a': [("down", 1), ("diagonal_front_right", 5.656*k), ("diagonal_back_right", 5.656*k), ("diagonal_front_left", 2.828*k), ("strafe_left", 4*k), ("up", 1), ("strafe_right", 4*k), ("diagonal_back_right", 2.828*k), ("strafe_right", 2*k)],
        'b': [("down", 1), ("forward", 4*k), ("strafe_right", 2*k), ("backward", 2*k), ("strafe_left", 2*k), ("strafe_right", 2*k), ("backward", 2*k), ("strafe_left", 2*k), ("up", 1), ("strafe_right", 4*k)],
        'c': [("strafe_right", 2*k), ("down", 1), ("strafe_left", 2*k), ("forward", 4*k), ("strafe_right", 2*k), ("up", 1), ("backward", 4*k), ("strafe_right", 2*k)],
        'd': [("down", 1), ("forward", 4*k), ("strafe_right", 2*k), ("backward", 4*k), ("strafe_left", 2*k), ("up", 1), ("strafe_right", 4*k)],
        'e': [("strafe_right", 2*k), ("down", 1), ("strafe_left", 2*k), ("forward", 2*k), ("strafe_right", 2*k), ("strafe_left", 2*k), ("forward", 2*k), ("strafe_right", 2*k), ("up", 1), ("backward", 4*k), ("strafe_right", 2*k)],
        'f': [("down", 1), ("forward", 2*k), ("strafe_right", 2*k), ("strafe_left", 2*k), ("forward", 2*k), ("strafe_right", 2*k), ("up", 1), ("backward", 4*k), ("strafe_right", 2*k)],
        'g': [("down", 1), ("forward", 4*k), ("strafe_right", 2*k), ("strafe_left", 2*k), ("backward", 4*k), ("strafe_right", 2*k), ("forward", 2*k), ("strafe_left", k), ("up", 1), ("backward", 2*k), ("strafe_right", 3*k)],
        'h': [("down", 1), ("forward", 4*k), ("backward", 2*k), ("strafe_right", 2*k), ("forward", 2*k), ("backward", 4*k), ("up", 1), ("strafe_right", 2*k)],
        'i': [("down", 1), ("strafe_right", 2*k), ("strafe_left", 1*k), ("forward", 4*k), ("strafe_left", 1*k), ("strafe_right", 2*k), ("up", 1), ("backward", 4*k), ("strafe_right", 2*k)],
        'j': [("forward", 2*k), ("down", 1), ("backward", 2*k), ("strafe_right", 2*k), ("forward", 4*k), ("strafe_left", 2*k), ("strafe_right", 4*k), ("up", 1), ("backward", 4*k), ("strafe_right", 2*k)],
        'k': [("down", 1), ("forward", 4*k), ("backward", 2*k), ("diagonal_front_right", 2.828*k), ("diagonal_back_left", 2.828*k), ("diagonal_back_right", 2.828*k), ("up", 1), ("strafe_right", 2*k)],
        'l': [("forward", 4*k), ("down", 1), ("backward", 4*k), ("strafe_right", 2*k), ("up", 1), ("strafe_right", 2*k)],
        'm': [("down", 1), ("forward", 4*k), ("diagonal_back_right", 2.828*k), ("diagonal_front_right", 2.828*k), ("backward", 4*k), ("up", 1), ("strafe_right", 2*k)],
        'n': [("down", 1), ("forward", 4*k), ("diagonal_back_right", 5.656*k), ("forward", 4*k), ("up", 1), ("strafe_right", 2*k), ("backward", 4*k)],
        'o': [("down", 1), ("forward", 4*k), ("strafe_right", 2*k), ("backward", 4*k), ("strafe_left", 2*k), ("up", 1), ("strafe_right", 4*k)],
        'p': [("down", 1), ("forward", 4*k), ("strafe_right", 2*k), ("backward", 2*k), ("strafe_left", 2*k), ("diagonal_back_right", 2.828*k), ("forward", 2*k), ("up", 1), ("strafe_right", 2*k)],
        'q': [("down", 1), ("strafe_right", 2*k), ("forward", 4*k), ("strafe_left", 2*k), ("backward", 4*k), ("strafe_right", 2*k), ("up", 1), ("strafe_right", 4*k)],
        'r': [("down", 1), ("forward", 4*k), ("strafe_right", 2*k), ("backward", 2*k), ("strafe_left", 2*k), ("diagonal_back_right", 2.828*k), ("up", 1), ("strafe_right", 2*k)],
        's': [("down", 1), ("strafe_right", 2*k), ("forward", 2*k), ("strafe_left", 2*k), ("forward", 2*k), ("strafe_right", 2*k), ("up", 1), ("backward", 4*k), ("strafe_right", 2*k)],
        't': [("strafe_right", 2*k), ("down", 1), ("forward", 4*k), ("strafe_left", 2*k), ("strafe_right", 4*k), ("up", 1), ("backward", 4*k), ("strafe_right", 2*k)],
        'u': [("forward", 4*k), ("down", 1), ("backward", 4*k), ("strafe_right", 2*k), ("forward", 4*k), ("up", 1), ("strafe_right", 2*k), ("backward", 4*k)],
        'v': [("forward", 4*k), ("down", 1), ("diagonal_back_right", 5.656*k), ("diagonal_front_left", 5.656*k), ("up", 1), ("strafe_right", 2*k), ("backward", 4*k)],
        'w': [("forward", 4*k), ("down", 1), ("backward", 4*k), ("diagonal_front_right", 2.828*k), ("diagonal_back_right", 2.828*k), ("forward", 4*k), ("up", 1), ("strafe_right", 2*k), ("backward", 4*k)],
        'x': [("down", 1), ("diagonal_front_right", 5.656*k), ("up", 1), ("strafe_left", 4*k), ("down", 1), ("diagonal_back_right", 5.656*k), ("up", 1), ("strafe_right", 2*k)],
        'y': [("forward", 4*k), ("down", 1), ("diagonal_back_right", 2.828*k), ("diagonal_front_right", 2.828*k), ("diagonal_back_left", 2.828*k), ("backward", 2*k), ("up", 1), ("strafe_right", 4*k)],
        'z': [("forward", 4*k), ("down", 1),  ("strafe_right", 4*k), ("diagonal_back_left", 5.656*k), ("strafe_right", 4*k), ("up", 1), ("strafe_right", 2*k)],
        '0': [("down", 1), ("forward", 4*k), ("strafe_right", 2*k), ("backward", 4*k), ("strafe_left", 2*k), ("up", 1), ("strafe_right", 4*k)],
        '1': [("down", 1), ("forward", 4*k), ("up", 1), ("strafe_right", 2*k), ("backward", 4*k)],
        '2': [("forward", 4*k), ("down", 1), ("strafe_right", 2*k), ("backward", 2*k), ("strafe_left", 2*k), ("backward", 2*k), ("strafe_right", 2*k), ("up", 1), ("strafe_right", 2*k)],    
        '3': [("down", 1), ("strafe_right", 2*k), ("forward", 2*k), ("strafe_left", 2*k), ("strafe_right", 2*k), ("forward", 2*k), ("strafe_left", 2*k), ("up", 1), ("strafe_right", 4*k), ("backward", 4*k)],
        '4': [("forward", 4*k), ("down", 1), ("backward", 2*k), ("strafe_right", 2*k), ("forward", 2*k), ("backward", 4*k), ("up", 1), ("strafe_right", 2*k)],
        '5': [("down", 1), ("strafe_right", 2*k), ("forward", 2*k), ("strafe_left", 2*k), ("forward", 2*k), ("strafe_right", 2*k), ("up", 1), ("backward", 4*k), ("strafe_right", 2*k)],
        '6': [("forward", 2*k), ("down", 1), ("strafe_right", 2*k), ("backward", 2*k), ("strafe_left", 2*k), ("forward", 4*k), ("strafe_right", 2*k), ("up", 1), ("strafe_right", 2*k), ("backward", 4*k)],
        '7': [("down", 1), ("diagonal_front_right", 5.656*k), ("strafe_left", 4*k), ("up", 1), ("strafe_right", 6*k), ("backward", 4*k)],
        '8': [("down", 1), ("forward", 4*k), ("strafe_right", 2*k), ("backward", 2*k), ("strafe_left", 2*k), ("strafe_right", 2*k), ("backward", 2*k), ("strafe_left", 2*k), ("up", 1), ("strafe_right", 4*k)],
        '9': [("down", 1), ("strafe_right", 2*k), ("forward", 4*k), ("strafe_left", 2*k), ("backward", 2*k), ("strafe_right", 2*k), ("up", 1), ("backward", 2*k), ("strafe_right", 2*k)],
    }
 
    if letter in letter_movements:
        for move in letter_movements[letter]:
            sleep(0.2)
            movements[move[0]](move[1])
        return
    else:
        return "Movement pattern for the letter not defined."
 
 
if __name__ == "__main__":
    # Example usage
    # movements_dict["diagonal_front_left"](4)
    # movements_dict["backward"](4)
    # movements_dict["forward"](4)
    # movements_dict["strafe_right"](4)
    # movements_dict["strafe_left"](4)
    # movements_dict["rotate_left"](6)
    # movements_dict["rotate_right"](2)
    # movements_dict["diagonal_front_left"](2)
    # movements_dict["diagonal_front_right"](4)
    # movements_dict["diagonal_back_left"](2)
    # movements_dict["diagonal_back_right"](2)
# a,
    write_letter("1")