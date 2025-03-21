import pickle
from collections import UserDict
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Name cannot be empty")
        super().__init__(value)

class Phone(Field):
    def __init__(self, value):
        if not self.validate_phone(value):
            raise ValueError("Phone number must contain 10 digits")
        super().__init__(value)

    def validate_phone(self, phone):
        return phone.isdigit() and len(phone) == 10

class Birthday(Field):
    def __init__(self, value):
        try:
            self.date = datetime.strptime(value, "%d.%m.%Y")
            if self.date > datetime.now():
                raise ValueError("Birthday cannot be in the future")
            super().__init__(value)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))
        return f"Phone {phone} added to contact {self.name}"

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return f"Phone {phone} removed from contact {self.name}"
        raise ValueError(f"Phone {phone} not found")

    def edit_phone(self, old_phone, new_phone):
        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                try:
                    self.phones[i] = Phone(new_phone)
                    return f"Phone {old_phone} changed to {new_phone}"
                except ValueError:
                    raise ValueError("Invalid new phone number")
        raise ValueError(f"Phone {old_phone} not found")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)
        return f"Birthday added to contact {self.name}"

    def __str__(self):
        result = f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
        if self.birthday:
            result += f", birthday: {self.birthday.value}"
        return result

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
        return f"Contact {record.name} added to address book"

    def find(self, name):
        if name in self.data:
            return self.data[name]
        else:
            raise KeyError(f"Contact {name} not found")

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return f"Contact {name} deleted"
        else:
            raise KeyError(f"Contact {name} not found")

    def get_upcoming_birthdays(self):
        upcoming_birthdays = []
        today = datetime.today().date()

        for name, record in self.data.items():
            if record.birthday:
                birthday_date = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()

                birthday_this_year = datetime(
                    today.year,
                    birthday_date.month,
                    birthday_date.day
                ).date()

                if birthday_this_year < today:
                    birthday_this_year = datetime(
                        today.year + 1,
                        birthday_date.month,
                        birthday_date.day
                    ).date()

                days_until_birthday = (birthday_this_year - today).days

                if days_until_birthday <= 7:
                    congratulation_date = birthday_this_year

                    if congratulation_date.weekday() >= 5:
                        days_to_add = 7 - congratulation_date.weekday()
                        congratulation_date = congratulation_date + timedelta(days=days_to_add)

                    upcoming_birthdays.append({
                        "name": name,
                        "congratulation_date": congratulation_date.strftime("%d.%m.%Y")
                    })

        return upcoming_birthdays

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except KeyError as e:
            return str(e)
        except IndexError:
            return "Please provide all required arguments"
    return inner

def parse_input(user_input):
    cmd = user_input.strip().lower()
    cmd_parts = cmd.split()
    cmd_name = cmd_parts[0] if cmd_parts else ""
    return cmd_name, cmd_parts[1:]

@input_error
def add_contact(args, book):
    name, phone, *_ = args
    record = book.find(name) if name in book.data else None
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
    if len(args) != 3:
        raise ValueError("Please provide name, old phone, and new phone")
    name, old_phone, new_phone = args
    record = book.find(name)
    return record.edit_phone(old_phone, new_phone)

@input_error
def show_phone(args, book):
    if not args:
        raise ValueError("Please provide contact name")
    name = args[0]
    record = book.find(name)
    return '; '.join(p.value for p in record.phones)

@input_error
def show_all(args, book):
    if not book.data:
        return "No contacts saved"
    return '\n'.join(str(record) for record in book.data.values())

@input_error
def add_birthday(args, book):
    if len(args) != 2:
        raise ValueError("Please provide name and birthday (DD.MM.YYYY)")
    name, birthday = args
    record = book.find(name)
    return record.add_birthday(birthday)

@input_error
def show_birthday(args, book):
    if not args:
        raise ValueError("Please provide contact name")
    name = args[0]
    record = book.find(name)
    if not record.birthday:
        return f"No birthday set for contact {name}"
    return f"{name}'s birthday: {record.birthday.value}"

@input_error
def birthdays(args, book):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No birthdays next week"
    return "\n".join(
        f"{birthday['name']}: {birthday['congratulation_date']}"
        for birthday in upcoming
    )

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()

def main():
    book = load_data()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(book)
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
            print(show_all(args, book))
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
