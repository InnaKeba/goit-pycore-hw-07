"""addressbook.py
Файл містить класи для моделювання адресної книги:
Field: Базовий клас для полів запису.
Name: Клас для зберігання імені контакту. Обов'язкове поле.
Phone: Клас для зберігання номера телефону. Має валідацію формату (10 цифр).
Record: Клас для зберігання інформації про контакт, включаючи ім'я, список телефонів та день народження.
AddressBook: Клас для зберігання та управління записами.
*new Birthday: Клас для зберігання дня народження. Має валідацію формату (YYYY-MM-DD).
"""
from collections import UserDict
from datetime import datetime, timedelta  # Імпорт datetime для роботи з перевіркою дати в класі Birthday та timedelta для обчислення днів тижня

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Номер телефону має складатися рівно з 10 цифр.")
        super().__init__(value)

class Birthday(Field): # 🔹 Додано клас Birthday
    def __init__(self, value):
        try:
            datetime.strptime(value, "%Y-%m-%d")  # Формат YYYY-MM-DD
        except ValueError:
            raise ValueError("Не вірний формат дати. Дата народження має бути у форматі YYYY-MM-DD.")
        super().__init__(value)

class Record:
    def __init__(self, name, birthday=None):  # Додано birthday 
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else None 

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return True
        return False

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p.value
        return None

    def __str__(self):
        phones = '; '.join(p.value for p in self.phones)
        bday = f", birthday: {self.birthday.value}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {phones}{bday}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self): # get_upcoming_birthdays із hw_03
        today = datetime.today().date()
        end_date = today + timedelta(days=7)
        congratulations = {}

        for record in self.data.values():
            if record.birthday: 
                try:
                    bday = datetime.strptime(record.birthday.value, "%Y-%m-%d").date()
                except ValueError:
                    continue  

                bday_this_year = bday.replace(year=today.year)
                if bday_this_year < today:
                    bday_this_year = bday.replace(year=today.year + 1)

                if today <= bday_this_year <= end_date:
                    day = bday_this_year.weekday()
                    if day in [5, 6]:  # Якщо день народження припадає на вихідний (субота або неділя
                        bday_this_year += timedelta(days=(7 - day))
                    weekday = bday_this_year.strftime("%A")
                    congratulations.setdefault(weekday, []).append(record.name.value)

        return congratulations