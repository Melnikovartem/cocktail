from db import next_question
from random import randint
users = ['fshfwqe', 'fsh2fa4', "wowmem", "hihi", "kwoman"]

for user in users:
    while next_question(user, str(randint(1,9))) != -1:
        pass
