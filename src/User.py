
"""Klasa opisująca użytkownika zapisanego na wizyty"""
class User(dict):
    name = ''
    surname = ''
    pesel = ""

    def __init__(self, imie, nazwisko, pesel):
        super().__init__(name=imie, surname=nazwisko, pesel=pesel)
        self.name = imie
        self.surname = nazwisko
        self.pesel = pesel

    def __str__(self) -> str:
        return super().__str__()

    def __eq__(self, other) -> bool:
        if isinstance(other, User):
            return self.name == other.name and self.surname == other.surname and self.pesel == other.pesel
