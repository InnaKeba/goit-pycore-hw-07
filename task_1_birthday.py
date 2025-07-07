"""addressbook.py
Файл містить класи для моделювання адресної книги:
Field: Базовий клас для полів запису.
Name: Клас для зберігання імені контакту. Обов'язкове поле.
Phone: Клас для зберігання номера телефону. Має валідацію формату (10 цифр).
Record: Клас для зберігання інформації про контакт, включаючи ім'я, список телефонів та день народження.
AddressBook: Клас для зберігання та управління записами.
*new Birthday: Клас для зберігання дня народження.
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

class Birthday(Field):  #Додано клас Birthday
    def __init__(self, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")  # формат DD.MM.YYYY
        except ValueError:
            raise ValueError("Не вірний формат дати. Дата народження має бути у форматі DD.MM.YYYY.")
        super().__init__(value)

class Record:
    def __init__(self, name, birthday=None):  #Додано birthday
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

    def get_upcoming_birthdays(self):  #додано get_upcoming_birthdays
        today = datetime.today().date()
        end_date = today + timedelta(days=7)
        congratulations = {}

        for record in self.data.values():
            if record.birthday:
                try:
                    bday = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()
                except ValueError:
                    continue

                bday_this_year = bday.replace(year=today.year)
                if bday_this_year < today:
                    bday_this_year = bday.replace(year=today.year + 1)

                if today <= bday_this_year <= end_date:
                    day = bday_this_year.weekday()
                    if day in [5, 6]:
                        bday_this_year += timedelta(days=(7 - day))
                    weekday = bday_this_year.strftime("%A")
                    congratulations.setdefault(weekday, []).append(record.name.value)

        return congratulations

# Обробка помилок
def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (IndexError, ValueError, TypeError) as e:
            return f"Помилка: {str(e)}"
        except KeyError:
            return "Контакт не знайдено."
    return wrapper

def parse_input(user_input):
    cmd, *args = user_input.strip().split()
    return cmd.lower(), args

@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def change_contact(args, book):
    name, old_phone, new_phone = args
    record = book.find(name)
    if not record:
        return "Контакт не знайдено."
    if record.edit_phone(old_phone, new_phone):
        return "Номер телефону оновлено."
    return "Старий номер не знайдено."

@input_error
def show_phone(args, book):
    name, *_ = args
    record = book.find(name)
    if not record:
        return "Контакт не знайдено."
    return f"{name}: {', '.join(p.value for p in record.phones)}"

@input_error
def show_all(book):
    if not book.data:
        return "Адресна книга порожня."
    return "\n".join(str(record) for record in book.data.values())

@input_error
def add_birthday(args, book):
    name, bday_str, *_ = args
    record = book.find(name)
    if not record:
        return "Контакт не знайдено."
    record.birthday = Birthday(bday_str)
    return f"День народження для {name} додано."

@input_error
def show_birthday(args, book):
    name, *_ = args
    record = book.find(name)
    if not record:
        return "Контакт не знайдено."
    if not record.birthday:
        return f"У контакту {name} не вказано день народження."
    return f"{name}: {record.birthday.value}"

@input_error
def birthdays(args, book):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "Немає днів народження на цьому тижні."
    result = []
    for day, names in upcoming.items():
        result.append(f"{day}: {', '.join(names)}")
    return "\n".join(result)

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(args, book))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()