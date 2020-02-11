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
import sqlite3
from Gui import *
from order_manager import *

order = ['asylum', 'taurus', 'gargoyle',
         'butterfly', 'capra', 'gaping',
         'spider', 'iron_golem', 'o_s',
         'stray', 'priscilla', 'ceaseless',
         'sif', 'kings', 'firesage', 'centipede',
         'chaosbed', 'seath', 'pinwheel', 'nito',
         'gwyndolin', 'sanctuary', 'artorias', 'manus',
         'kalameet', 'gwyn']

connection = sqlite3.connect("dark_souls.db", check_same_thread=False)
curs = connection.cursor()


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


def imagesearch_loop(image, player, timesample, precision=0.8):
    pos = imagesearch(image, precision)
    print(f"Searching for {image}")
    while pos[0] == -1:
        if player.dead:
            print("you died")
            return None
        # print("...")
        time.sleep(timesample)
        pos = imagesearch(image, precision)
    return pos


def target(player, run_name, image, image2=None):
    print("targeting")
    pos = imagesearch_loop(image, player, 0.5, 0.8)
    if pos is None:
        time.sleep(5)
        if not player.dead:
            target(player, image, image2)
        return
    print("position : ", pos[0], pos[1])
    if image2 is not None:
        pos = imagesearch_loop(image2, player, 0.5)
        if pos is None:
            time.sleep(5)
            if not player.dead:
                target(player, run_name, image, image2)
            return
        print("position : ", pos[0], pos[1])
        player.current_boss += 1
        curs.execute(f"UPDATE runs SET current_boss=? WHERE run_name=?", (str(player.current_boss), run_name))
        connection.commit()


def death_search(player, run_name):
    while True:
        imagesearch_loop('ded.png', player, 0.5, 0.5)
        player.dead = True
        player.deaths += 1
        player.total_deaths += 1
        curs.execute(f"UPDATE runs SET deaths=?, total_deaths=? WHERE run_name=?",
                     (str(player.deaths), str(player.total_deaths), run_name))
        connection.commit()
        print("Deaths: ", player.deaths)
        time.sleep(3)
        player.dead = False


def main_thread(player, run_name):
    game_on = True
    while game_on:
        if len(order) - 1 <= player.current_boss:
            game_on = False
        pathname = os.path.dirname(sys.argv[0]) + "/boss_imgs/" + order[player.current_boss]
        print(pathname)
        files = []
        for file in os.listdir(os.path.abspath(pathname)):
            files.append(os.fsdecode(file))
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
            target(player, run_name, name, reward)
    print("you won! ☺")
    player.new_game += 1
    player.deaths = 0
    curs.execute(f"UPDATE runs SET deaths=?, new_game=? WHERE run_name=?", (str(player.deaths), str(player.new_game), run_name))

'''Priscilla not fixed.... :/ both name and reward.'''


def get_tables():
    curs.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='runs'")
    hej = curs.fetchone()
    names = None
    print(hej)
    if hej is not None:
        curs.execute("SELECT run_name FROM runs")
        names = curs.fetchall()
    return names


def resume_run(run_name):
    print(run_name)
    curs.execute(f"SELECT * FROM runs WHERE run_name=?", (run_name,))
    name, deaths, current_boss, total_deaths, new_game = curs.fetchall()[0]
    print(deaths, current_boss, total_deaths, new_game)
    p = Player(deaths, current_boss, total_deaths, new_game)
    threading.Thread(target=death_search, args=(p, run_name)).start()
    threading.Thread(target=main_thread, args=(p, run_name)).start()


def start_new_run(run_name, app):
    print(run_name)
    curs.execute("CREATE TABLE IF NOT EXISTS runs(run_name TEXT, deaths INTEGER NOT NULL, "
                 "current_boss INTEGER NOT NULL, total_deaths INTEGER NOT NULL, new_game INTEGER NOT NULL)")
    curs.execute("INSERT INTO runs(run_name, deaths, current_boss, total_deaths, new_game) "
                 "VALUES(?,0,0,0,0)", (run_name,))
    connection.commit()
    # app = QApplication(sys.argv)
    order_list = OrderGui()
    order_list.show()
    app.exec_()
    p = Player(0, 0, 0, 0)
    threading.Thread(target=death_search, args=(p, run_name)).start()
    threading.Thread(target=main_thread, args=(p, run_name)).start()


def delete_table(run_name):
    print("deleting", run_name)
    curs.execute(f"DELETE FROM runs WHERE run_name=?", (run_name,))
    connection.commit()


if __name__ == "__main__":
    # start GUI
    app = QApplication(sys.argv)
    gui = GUI(app=app)
    gui.show()
    app.exec_()



