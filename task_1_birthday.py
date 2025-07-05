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
from datetime import datetime # Імпорт datetime для роботи з перевіркою дати в класі Birthday

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

# Додано клас Birthday
class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Дата народження має бути у форматі YYYY-MM-DD.")
        super().__init__(value)

class Record:
    def __init__(self, name, birthday=None): # Додано параметр birthday в клас Record
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

# Приклад використання з днем народження
if __name__ == "__main__":
    book = AddressBook()

    john_record = Record("John", birthday="1989-01-01")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    book.add_record(john_record)

    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    for name, record in book.data.items():
        print(record)

    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")
    print(john)

    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")

    book.delete("Jane")