from pynput import keyboard
import time
import os

break_the_loop = 0
RGB_PATH = "data/rgb/"
DEPTH_PATH = "data/depth/"
CONF_PATH = "data/confidence/"
PC_PATH = "data/pointclouds/"
INTRINSICS_PATH = "data/intrinsics/"
ANNOTATIONS_PATH = "data/annotations/"

def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(key.char))
        if key.char == "s":
            print("Pressed 's'")
                
        if key.char == "c":
            remove_last()
            print("Pressed 'c'")

        if key.char == "r":
            print("Pressed 'r")

        if key.char == "q":
            print("pressed q")
            global break_the_loop
            break_the_loop = 1
    except AttributeError:
        print('special key {0} pressed'.format(key))

def remove_last():
    global RGB_PATH
    file_to_remove = get_filename(RGB_PATH)
    print(file_to_remove)
    file_to_remove = int(file_to_remove)
    print(file_to_remove)
    file_to_remove = file_to_remove - 1
    print(file_to_remove)
    file_to_remove = str(file_to_remove).zfill(5)
    print(file_to_remove)
    to_remove = os.path.join(RGB_PATH, file_to_remove + ".png")
    to_remove = os.path.join(DEPTH_PATH, file_to_remove + ".csv")
    to_remove = os.path.join(CONF_PATH, file_to_remove + ".csv")
    to_remove = os.path.join(PC_PATH, file_to_remove + ".ply")
    to_remove = os.path.join(INTRINSICS_PATH, file_to_remove + ".csv")
    to_remove = os.path.join(ANNOTATIONS_PATH, file_to_remove + ".csv")
    print("TODO")

def get_filename(path):
    number_of_files = len(os.listdir(path))
    #print(number_of_files)
    number_of_files += 1
    number_of_files = str(number_of_files).zfill(5)
    return  number_of_files


if __name__=="__main__":
    keyboard_listener = keyboard.Listener(on_press=on_press)
    keyboard_listener.start()

    while not break_the_loop:
        time.sleep(1)