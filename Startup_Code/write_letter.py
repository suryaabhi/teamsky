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
        "diagonal_back_right": diagonal_back_right_
        }
    return mov_dict

def write_letter(letter, movements):
    letter_movements = {
        'a': [("diagonal_front_right", 4), ("diagonal_back_right", 4), ("diagonal_front_left", 2), ("strafe_left", 2)],
        'b': [("forward", 4), ("strafe_right", 2), ("backward", 2), ("strafe_left", 2), ("strafe_right", 2), ("backward", 2), ("strafe_left", 2)],
        'c': [("strafe_left", 2), ("forward", 4), ("strafe_right", 2)],
        'd': [("forward", 4), ("strafe_right", 2), ("backward", 4), ("strafe_left", 2)],
        'e': [("strafe_left", 2), ("forward", 2), ("strafe_right", 2), ("strafe_left", 2), ("forward", 2), ("strafe_right", 2)],
        'f': [("forward", 2), ("strafe_right", 2), ("strafe_left", 2), ("forward", 2), ("strafe_right", 2)],
        'g': [("forward", 2), ("strafe_right", 1), ("strafe_left", 1), ("backward", 1), ("strafe_left", 2), ("forward", 2), ("strafe_right", 2)],
        'h': [("forward", 4), ("backward", 2), ("strafe_right", 2), ("backward", 2), ("forward", 4)],
        'i': [("strafe_right", 2), ("strafe_left", 1), ("forward", 4), ("strafe_right", 1), ("strafe_left", 2)],
        'j': [("backward", 2), ("strafe_rigth", 2), ("forward", 4), ("strafe_left", 2), ("strafe_left", 4)],
        'k': [("forward", 4), ("backward", 2), ("diagonal_back_right", 2), ("diagonal_front_left", 2), ("diagonal_front_right", 2)],
        'l': [("strafe_left", 2), ("forward", 4)],
        'm': [("forward", 4), ("diagonal_back_right", 2), ("diagonal_front_right", 2), ("backward", 4)],
        'n': [],
        'o': [],
        'p': [],
        'q': [],
        'r': [],
        's': [],
        't': [],
        'u': [],
        'v': [],
        'w': [],
        'x': [],
        'y': [],
        'z': []
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