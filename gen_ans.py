from db import next_question
from random import randint
from time import sleep
users = ['fshfwqe', 'fsh2fa4', "wowmem", "hihi", "kwoman"]

from threading import Thread

def f():
    while True:
        print(3)
        sleep(3)


Thread(target=f).start()

while True:
    print(5)
    sleep(5)
