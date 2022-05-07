import datetime
import random

import names

from User import User

"""Klasa stanowiąca podstawę działania naszego programu, zawiera dane o wizytach i użytkownikach zapisanych na wizyty"""
class Day:
    busyhours = {}

    def __init__(self):
        users = list()
        hours = [(datetime.time(h, m).strftime('%H:%M')) for h in range(8, 21) for m in (00, 30)]
        hours.remove("20:30")
        _temp2 = list(bool(random.getrandbits(1)) for i in range(len(hours)))

        for i in range(len(_temp2)):
            users.append(None)
        for i in range(len(_temp2)):
            if _temp2[i] == True:
                pass
            elif _temp2[i] == False:
                name = names.get_first_name()
                surname = names.get_last_name()
                pesel = ''.join(["{}".format(random.randint(0, 9)) for num in range(0, 11)])
                year = random.randint(1900, 2021)
                u = User(name, surname,pesel)
                users[i] = u
        self.busyhours = dict(zip(hours, zip(_temp2, users)))

    def __dict__(self):
        return self.busyhours