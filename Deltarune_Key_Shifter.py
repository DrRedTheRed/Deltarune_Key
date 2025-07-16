"""
Deltarune Key Shifter Script

Author: Dr. Red
Date: 2025-07-16

Description:
    比较暴力的爆改Deltarune的钢琴按键方法，真的超级暴力。脚本环境为python3.12，记得看readme.md。

License:
    MIT License
"""

from pynput import keyboard
from pynput.keyboard import Key, Controller
import threading
import time

kb = Controller()

direction_map = {
    '1': [],
    '2': [Key.right],
    '3': [Key.right, Key.down],
    '4': [Key.down],
    '5': [Key.left, Key.down],
    '6': [Key.left],
    '7': [Key.left, Key.up],
    '8': [Key.up],
    'r': ['c'],
    't': ['c', Key.right],
    'y': ['c', Key.right, Key.down],
    'u': ['c', Key.down],
    'i': ['c', Key.left, Key.down],
    'o': ['c', Key.left],
    'p': ['c', Key.left, Key.up]
}

pressed_keys = set()
held_directions = set()

def delayed_z():
    time.sleep(0.025) # magic number。如果不流畅的话改这两个数字试试
    kb.press('z')
    time.sleep(0.075) # magic number2。
    kb.release('z')

def press_directions(directions):
    for d in directions:
        if d not in held_directions:
            kb.press(d)
            held_directions.add(d)

def on_press(key):
    try:
        k = key.char
        if k in direction_map:
            if k in pressed_keys:
                return
            pressed_keys.add(k)

            press_directions(direction_map[k])

            threading.Thread(target=delayed_z, daemon=True).start()

    except AttributeError:
        pass

def on_release(key):
    try:
        k = key.char
        if k in direction_map:
            pressed_keys.discard(k)
            for d in direction_map[k]:
                if d in held_directions:
                    kb.release(d)
                    held_directions.remove(d)

    except AttributeError:
        pass

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    print("脚本启动，按Ctrl+C退出，弹爆Kris")
    listener.join()
