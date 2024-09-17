from Utils.MotorUtils import move, stop, DEFAULT_SPEED
from time import sleep
from Utils.MotorUtils import front, rotate_right, rotate_left, back, strafe_left, strafe_right, stop, diagonal_back_left, diagonal_back_right, diagonal_front_left, diagonal_front_right

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
    strafe_left(num, speed)

def strafe_right_(num=1, time=None, speed=DEFAULT_SPEED):
    num = num/4
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
    pass

def down_(num=1, time=None, speed=DEFAULT_SPEED):
    pass

def movement():
    mov_dict = {
        "forward": front_,
        "backward": back_,
        "strafe_left": strafe_left_,
        "strafe_right": strafe_right_,
        "rotate_left": rotate_left_,
        "rotate_right": rotate_right_,
        "diagonal_front_left": diagonal_back_left_,
        "diagonal_front_right": diagonal_back_right_,
        "diagonal_back_left": diagonal_back_left_,
        "diagonal_back_right": diagonal_back_right_,
        "up": up_,
        "down": down_,
        }
    return mov_dict

def write_letter(letter, movements, k = 1 , gap = 1):
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
        'j': [("forward", 2*k), ("down", 1), ("backward", 2*k), ("strafe_rigth", 2*k), ("forward", 4*k), ("strafe_left", 2*k), ("strafe_right", 4*k), ("up", 1), ("backward", 4*k), ("strafe_right", 2*k)],
        'k': [("down", 1), ("forward", 4*k), ("backward", 2*k), ("diagonal_front_right", 2.828*k), ("diagonal_back_left", 2.828*k), ("diagonal_back_right", 2.828*k), ("up", 1), ("strafe_right", 2*k)],
        'l': [("forward", 4*k), ("down", 1), ("backward", 4*k), ("strafe_rigth", 2*k), ("up", 1), ("strafe_right", 2*k)],
        'm': [("down", 1), ("forward", 4*k), ("diagonal_back_right", 2.828*k), ("diagonal_front_right", 2.828*k), ("backward", 4*k), ("up", 1), ("strafe_right", 2*k)],
        'n': [("down", 1), ("forward", 4*k), ("diagonal_back_right", 5.656*k), ("forward", 4*k), ],
        'o': [("down", 1), ],
        'p': [("down", 1), ],
        'q': [("down", 1), ],
        'r': [("down", 1), ],
        's': [("down", 1), ],
        't': [("down", 1), ],
        'u': [("down", 1), ],
        'v': [("down", 1), ],
        'w': [("down", 1), ],
        'x': [("down", 1), ],
        'y': [("down", 1), ],
        'z': [("down", 1), ]
    }

    if letter in letter_movements:
        return [movements[move[0]](move[1]) for move in letter_movements[letter]]
    else:
        return "Movement pattern for the letter not defined."

if __name__ == "__main__":
    movements_dict = movement()
    # Example usage
    # movements_dict["diagonal_front_left"](4)
    # movements_dict["backward"](2)
    movements_dict["strafe_left"](4)
    # movements_dict["strafe_right"](2)
    # movements_dict["strafe_right"](2)
    # movements_dict["rotate_left"](2)
    # movements_dict["rotate_right"](2)
    # movements_dict["diagonal_front_left"](2)
    # movements_dict["diagonal_front_right"](2)
    # movements_dict["diagonal_back_left"](2)
    # movements_dict["diagonal_back_right"](2)

    # write_letter("a", movements_dict)