### Python script that checks when you enter a boss fight and then tells you when you get the item from the boss. // also counts how many times you've died.
### all of the image finding cred goes to drov0 using his project https://github.com/drov0/python-imagesearch

import cv2
import numpy as np
import pyautogui
import platform
import subprocess
import time
import sys
import os
import threading
from player import Player

is_retina = False
if platform.system() == "Darwin":
    is_retina = subprocess.call("system_profiler SPDisplaysDataType | grep 'retina'", shell=True)


def imagesearch(image, precision=0.8):
    im = pyautogui.screenshot()
    if is_retina:
        im.thumbnail((round(im.size[0] * 0.5), round(im.size[1] * 0.5)))
    # im.save('testarea.png') useful for debugging purposes, this will save the captured region as "testarea.png"
    img_rgb = np.array(im)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(image, 0)
    template.shape[::-1]

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if max_val < precision:
        return [-1, -1]
    return max_loc


def imagesearch_loop(image, timesample, precision=0.8):
    pos = imagesearch(image, precision)
    print(f"Searching for {image}")
    while pos[0] == -1:
        if p.dead:
            print("you died")
            return None
        # print("...")
        time.sleep(timesample)
        pos = imagesearch(image, precision)
    return pos


def target(player, image, image2=None):
    print("targeting")
    pos = imagesearch_loop(image, 0.5, 0.8)
    if pos is None:
        time.sleep(5)
        if not player.dead:
            target(p, image, image2)
        return
    print("position : ", pos[0], pos[1])
    if image2 is not None:
        pos = imagesearch_loop(image2, 0.5)
        if pos is None:
            time.sleep(5)
            if not player.dead:
                target(p, image, image2)
            return
        print("position : ", pos[0], pos[1])
        p.current_boss += 1


def death_search(player):
    while True:
        imagesearch_loop('ded.png', 0.5)
        p.dead = True
        player.deaths += 1
        print("Deaths: ", player.deaths)
        time.sleep(3)
        p.dead = False


def main_thread(player):
    for i in range(len(order)-1):
        pathname = os.path.dirname(sys.argv[0]) + "/boss_imgs/" + order[player.current_boss]
        print(pathname)
        files = []
        for file in os.listdir(os.path.abspath(pathname)):
            filename = os.fsdecode(file)
            files.append(filename)
        print(len(files))
        if len(files) == 2:
            if 'name' in files[0]:
                name = pathname + '/' + files[0]
            elif 'name' in files[1]:
                name = pathname + '/' + files[1]
            if 'reward' in files[1]:
                reward = pathname + '/' + files[1]
            elif 'reward' in files[0]:
                reward = pathname + '/' + files[0]
            target(player, name, reward)

'''Priscilla not fixed.... :/ both name and reward.'''

order = ['asylum', 'taurus', 'gargoyle', 'butterfly',
         'capra', 'gaping', 'spider', 'iron_golem', 'o_s',
         'stray', 'priscilla', 'ceaseless', 'firesage']

if __name__ == "__main__":
    p = Player(False, 0, 9)
    threading.Thread(target=death_search, args=(p,)).start()
    threading.Thread(target=main_thread, args=(p,)).start()
    # for i in range(len(order)):
    #     pathname = os.path.dirname(sys.argv[0]) + "/boss_imgs/" + order[p.current_boss]
    #     files = []
    #     for file in os.listdir(os.path.abspath(pathname)):
    #         filename = os.fsdecode(file)
    #         files.append(filename)
    #     print(len(files))
    #     if len(files) == 2:
    #         if 'name' in files[0]:
    #             name = pathname + '/' + files[0]
    #         elif 'name' in files[1]:
    #             name = pathname + '/' + files[1]
    #         if 'reward' in files[1]:
    #             reward = pathname + '/' + files[1]
    #         elif 'reward' in files[0]:
    #             reward = pathname + '/' + files[0]
    #         target(p, name, reward)


