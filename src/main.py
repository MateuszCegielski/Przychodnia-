import calendar
import json
import random
import time
from datetime import date
from datetime import datetime

import requests
from termcolor import colored

from Day import Day
from User import User

"""AUTORZY PROJEKTU:
KACPER KILIANEK I MATEUSZ CEGIELSKI"""

""" Witamy w naszym programie, poniżej przedstawiamy krótką instrukcje, która pomoże poprawnie uruchomić nasz program: 
    1. Proszę uruchomić lokalny serwer 
    2. Przy pierwszym uruchomieniu proszę odkomentować wywołanie funkcji set_up i Wczytanie_i_wysyłka_na_serv (pierwsze uruchomienie aplikacji, załadowanie plików na serwer, ew. test dla pojedynczego użytkownika)
    3. Po wygenerowaniu plików nowych losowych zestawu danych i zapisaniu ich na lokalny serwer, można ponownie zakomentować powyzsze funkcje poniewaz nie bedą już potrzebne i tym razem odkomentować funkcję wczyt_serv()
    4. Teraz przy założeniu, że serwer cały czas działa, można dalej korzystać z programu wybierając poszczególne działania z menu
    5. Po wyłączeniu lokalnego serwera konieczna jest ponowna wysłanie plików na serwer """

"""FUNKCJA SŁUŻĄCA DO ZAPISÓW"""
def glowny():
    choice1 = int(input("Na kiedy chciałby Pan/chciałaby Pani się zapisać? Proszę podać rok: "))
    print()
    if choice1 < year:
        raise Exception("Rok przeszły jest zabroniony. Proszę podać rok teraźniejszy lub przyszły")
    elif choice1 > maxyear:
        raise Exception(
            "Aplikacja zaprojektowana do działania tylko rok w przód. Proszę wybrać rok teraźniejszy lub przyszły. ")
    print(calendar.calendar(choice1))
    choice2 = int(
        input("Na jaki miesiąc chciałby Pan/chciałaby Pani się zapisać? Proszę podać odpowiedni miesiąc:"))
    print()
    if choice1 == year and choice2 < curr_month:
        raise Exception("Ten miesiąc jest już tylko przeszłością, następnym razem proszę podać właściwą wartość ")
    elif choice2 > 12:
        raise Exception("Rok nie ma więcej niż 12 miesięcy. Spróbuj ponownie jeszcze raz.")
    print(calendar.month(choice1, choice2))
    choice3 = int(input("Na jaki dzień chciałby Pan/chciałaby Pani się zapisać? Proszę podać odpowiedni dzień: "))
    if choice1 == year and (choice2 < curr_month or choice3 < curr_day):
        raise Exception("Ten dzień odszedł już do przeszłości, następnym razem proszę podać właściwą wartość ")
    elif choice2 == 12 and choice3 > 31:
        raise Exception("Ten miesiąc nie ma tyle dni co podałeś. Przykro mi, spróbuj ponownie jeszcze raz.")
    elif choice2 != 12 and choice3 > (date(choice1, choice2 + 1, 1) - date(choice1, choice2, 1)).days:
        raise Exception("Ten miesiąc nie ma tyle dni co podałeś. Przykro mi, spróbuj ponownie jeszcze raz.")
    print("WYŚWIETLANIE GODZIN Z DANEGO DNIA:")
    print("-" * 50)
    wczyt_serv()
    temp = Days[(date(choice1, choice2, choice3) - date(maxyear, 12, 31)).days]
    for hour, value in temp.busyhours.items():
        if value[0] == False:
            print(colored(str(hour) + " " + (value[1]['name']) + " " + (value[1]['surname']), 'red'))
        elif value[0] == True:
            print(colored(str(hour) + " " + str(value[1]), 'green'))
    choice4 = (input(
        "Na którą godzinę chciałby Pan/chciałaby Pani się zapisać? \nProszę podać niezajętą godzinę (Kolor zielony oznacza możliwość zapisania się na daną godzinę, czerwony brak takowej możliwości): ")).strip()
    print("Proszę czekać, trwa przetwarzanie decyzji...")
    randomInt = random.randint(0, 500)
    time.sleep(randomInt / 100)
    wczyt_serv()
    for hour, value in temp.busyhours.items():
        if hour == choice4 and value[0] == False:
            print(colored("NIE UDAŁO SIĘ ZAPISAĆ! TERMIN JUŻ ZAJĘTY."))
        elif hour == choice4:
            temp.busyhours[hour] = (False, użytkownik)
    print("POMYŚLNIE UDAŁO SIĘ ZAPISAĆ NA PODANĄ GODZINĘ!")
    json_object = json.dumps(Days[(date(choice1, choice2, choice3) - date(maxyear, 12, 31)).days].__dict__(), indent=25)
    with open(
            "baza\\sample" + str((date(choice1, choice2, choice3) - date(maxyear, 12, 31)).days + len(Days)) + ".json",
            "w") as outfile:
        outfile.write(json_object)
        # print("PRZESYŁANIE KLUCZA:", Days.index(Days[(date(choice1, choice2, choice3) - date(maxyear, 12, 31)).days]))
        update(Days[(date(choice1, choice2, choice3) - date(maxyear, 12, 31)).days].__dict__(),
               Days.index(Days[(date(choice1, choice2, choice3) - date(maxyear, 12, 31)).days]))
    outfile.close()


"""FUNKCJA SŁUŻĄCA DO ODWOŁYWANIA WIZYT"""
def usuwanie():
    choice1 = int(input(" Proszę podać rok wizyty którą chce Pani/Pan odwołać : "))
    print()
    if choice1 < year:
        raise Exception("Rok przeszły jest zabroniony. Proszę podać rok teraźniejszy lub przyszły")
    elif choice1 > maxyear:
        raise Exception(
            "Aplikacja zaprojektowana do działania tylko rok w przód. Proszę wybrać rok teraźniejszy lub przyszły. ")
    print(calendar.calendar(choice1))
    choice2 = int(
        input(" Proszę podać odpowiedni miesiąc z którego chce Pani/Pan odwołać wizytę :"))
    print()
    if choice1 == year and choice2 < curr_month:
        raise Exception("Ten miesiąc jest już tylko przeszłością, następnym razem proszę podać właściwą wartość ")
    elif choice2 > 12:
        raise Exception("Rok nie ma więcej niż 12 miesięcy. Spróbuj ponownie jeszcze raz.")
    print(calendar.month(choice1, choice2))
    choice3 = int(input("Proszę podać dzień z którego chcesz usunąć wizytę: "))
    if choice1 == year and (choice2 < curr_month or choice3 < curr_day):
        raise Exception("Ten dzień odszedł już do przeszłości, następnym razem proszę podać właściwą wartość ")
    elif choice2 == 12 and choice3 > 31:
        raise Exception("Ten miesiąc nie ma tyle dni co podałeś. Przykro mi, spróbuj ponownie jeszcze raz.")
    elif choice2 != 12 and choice3 > (date(choice1, choice2 + 1, 1) - date(choice1, choice2, 1)).days:
        raise Exception("Ten miesiąc nie ma tyle dni co podałeś. Przykro mi, spróbuj ponownie jeszcze raz.")

    print("WYŚWIETLANIE GODZIN Z DANEGO DNIA:")
    print("-" * 50)
    wczyt_serv()
    temp = Days[(date(choice1, choice2, choice3) - date(maxyear, 12, 31)).days]
    for hour, value in temp.busyhours.items():
        if value[0] == False:
            print(colored(str(hour) + " " + (value[1]['name']) + " " + (value[1]['surname']), 'red'))
        elif value[0] == True:
            print(colored(str(hour) + " " + str(value[1]), 'green'))
    choice4 = (input(
        "Na którą godzinę była zapisana wizyta : ")).strip()
    for hour, value in temp.busyhours.items():
        if hour == choice4 and value[1] != użytkownik:
            raise Exception("Nie można odwołać nie swojej wizyty...")
        if hour == choice4 and value[0] == True:
            raise Exception("Nie można odwołać wolnego terminu!")
        elif hour == choice4:
            temp.busyhours[hour] = (True, None)
            print("WIZYTA ODWOŁANA")
            json_object = json.dumps(Days[(date(choice1, choice2, choice3) - date(maxyear, 12, 31)).days].__dict__(),
                                     indent=25)
            with open("baza\\sample" + str(
                    (date(choice1, choice2, choice3) - date(maxyear, 12, 31)).days + len(Days)) + ".json",
                      "w") as outfile:
                outfile.write(json_object)
                update(Days[(date(choice1, choice2, choice3) - date(maxyear, 12, 31)).days].__dict__(),
                       Days.index(Days[(date(choice1, choice2, choice3) - date(maxyear, 12, 31)).days]))
            outfile.close()


"""FUNCKJA SŁUŻĄCA DO PODEJRZENIA ZAPISANYCH WIZYT"""
def Podglad():
    choice1 = int(input("Proszę podać rok: "))
    print()
    if choice1 < year:
        raise Exception("Rok przeszły jest zabroniony. Proszę podać rok teraźniejszy lub przyszły")
    elif choice1 > maxyear:
        raise Exception(
            "Aplikacja zaprojektowana do działania tylko rok w przód. Proszę wybrać rok teraźniejszy lub przyszły. ")
    print(calendar.calendar(choice1))
    choice2 = int(
        input("Proszę podać miesiąc:"))
    print()
    if choice1 == year and choice2 < curr_month:
        raise Exception("Ten miesiąc jest już tylko przeszłością, następnym razem proszę podać właściwą wartość ")
    elif choice2 > 12:
        raise Exception("Rok nie ma więcej niż 12 miesięcy. Spróbuj ponownie jeszcze raz.")
    print(calendar.month(choice1, choice2))
    choice3 = int(input("Proszę podać odpowiedni dzień: "))
    if choice1 == year and (choice2 < curr_month or choice3 < curr_day):
        raise Exception("Ten dzień odszedł już do przeszłości, następnym razem proszę podać właściwą wartość ")
    elif choice2 == 12 and choice3 > 31:
        raise Exception("Ten miesiąc nie ma tyle dni co podałeś. Przykro mi, spróbuj ponownie jeszcze raz.")
    elif choice2 != 12 and choice3 > (date(choice1, choice2 + 1, 1) - date(choice1, choice2, 1)).days:
        raise Exception("Ten miesiąc nie ma tyle dni co podałeś. Przykro mi, spróbuj ponownie jeszcze raz.")
    temp = Days[(date(choice1, choice2, choice3) - date(maxyear, 12, 31)).days]
    print("WYŚWIETLANIE GODZIN Z DANEGO DNIA:")
    print("-" * 50)
    for hour, value in temp.busyhours.items():
        if value[0] == False:
            print(colored(str(hour) + " " + (value[1]['name']) + " " + (value[1]['surname']), 'red'))
        elif value[0] == True:
            print(colored(str(hour) + " " + str(value[1]), 'green'))


"""FUNKCJA WCZYTYWANIA Z SERWERA"""
def wczyt_serv():
    response = requests.get("http://127.0.0.1:5000/api/getdata")
    slownik = response.json()
    for i in range(len(Days)):
        Days[i].busyhours = slownik[str(i)]



"""SETUP PARAMETRÓW"""
flag = True
print("PROGRAM SŁUŻĄCY DO ZAPISU DO LEKARZA")
print("-" * 50)
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
print("AKTUALNA DATA I GODZINA: ", dt_string)
year = int(now.strftime("%Y"))
curr_month = int(now.strftime("%m"))
curr_day = int(now.strftime("%d"))
maxyear = year + 1
number_of_days = (date(maxyear, 12, 31) - date(year, curr_month, curr_day)).days
Days = [Day() for _ in range(number_of_days)]

"""FUNKCJA SŁUŻĄCA DO GENEROWANIA PLIKÓW(LOKALNIE), JEŚLI CHCESZ MIEĆ NOWE, URUCHOM TO"""
def set_up():
    for i in range(len(Days)):
        json_object = json.dumps(Days[i].__dict__(), indent=25)
        with open("baza\\sample" + str(i) + ".json", "w") as outfile:
            outfile.write(json_object)
    outfile.close()

"""FUNKCJA SŁUŻĄCA DO WCZYTYWANIA Z PLIKÓW I WYSŁANIA ICH ZAWARTOŚCI NA SERWER(METODA POST)"""
def Wczytanie_i_wyslanie_na_serv():
    # WCZYTYWANIE i WYSYŁANIE NA SERWER
    for i in range(len(Days)):
        with open("baza\\sample" + str(i) + ".json", "r") as openfile:
            json_object = json.load(openfile)
            Days[i].busyhours = json_object  # TUTAJ WCZYTYWANIE
            # print(json_object)
            mydata = {"id": i, "data": json_object}
            d = json.dumps(mydata)
            response = requests.post("http://127.0.0.1:5000/api/setdata", data=d,
                                     headers={'content-type': 'application/json'})
            # if response.status_code == 201:
            #     print("Success!")
            openfile.close()


"""SETUP APLIKACJI (ALBO GENEROWANIE PLIKÓW I WYSYŁANIE ICH NA SERWER(OPCJA STARTOWA DLA PIERWSZEGO URUCHOMIENIA) LUB WCZYTYWANIE Z SERWERA(DEFAULT DLA WSZYSTKICH UŻYTKOWNIKÓW))"""
"""WARIANT PIERWSZY"""
set_up()
Wczytanie_i_wyslanie_na_serv()
"""WARIANT DRUGI"""
# wczyt_serv()

"""FUNKCJA AKTUALIZUJĄCA WARTOŚCI NA SERWERZE(DZIĘKI METODZIE PUT)"""
def update(json_newobject, index):
    # response = requests.get("http://127.0.0.1:5000/api/getdata")
    # if response.status_code == 200:
    #     print(response.json())
    newdata = {"id": index, "data": json_newobject}
    d = json.dumps(newdata)
    response = requests.put("http://127.0.0.1:5000/api/updatedata", data=d,
                            headers={'content-type': 'application/json'})

    response = requests.get("http://127.0.0.1:5000/api/getdata")
    # if response.status_code == 200:
    #     print("Update zakończony kodem: ", response.status_code)


"""MENU DLA UŻYTKOWNIKA"""
imie = input("WITAJ UŻYTKOWNIKU! PROSZĘ PODAJ SWOJE IMIĘ: ")
nazwisko = input("TERAZ PODAJ NAZWISKO: ")
pesel = input("A TERAZ PESEL: ")
użytkownik = User(imie, nazwisko, pesel)
while (flag):
    print('#' * 30)
    print("1.ZAPIS DO SPECJALISTY\n2.ODWOŁANIE WIZYTY\n3.PODGLĄD ZAPISÓW\n9.ZAKOŃCZENIE PROGRAMU")
    try:
        wybor = (int)((input("JAKĄ CZYNNOŚĆ CHCESZ WYKONAĆ: ")))
    except ValueError:
        print("Nie podano cyfry. Spróbuj ponownie.")
        wybor = 0
    if (wybor == 1):
        glowny()
    elif (wybor == 2):
        usuwanie()
    elif (wybor == 3):
        Podglad()
    elif (wybor == 9):
        print('*' * 30)
        print("Kończę prace programu...")
        flag = False
    elif (wybor == 0):
        pass
    else:
        print('Nie podano cyfry do której została przypisana akcja. Spróbuj ponownie.')
