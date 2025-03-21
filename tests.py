from datetime import datetime, timedelta
from bot import AddressBook, Record, Name, Phone, Birthday

def test_address_book_functionality():
    print("\n=== Створення адресної книги ===")
    book = AddressBook()
    print("Адресну книгу успішно створено")

    print("\n=== Створення та додавання контактів ===")
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    print(f"Створено запис для John: {john_record}")

    book.add_record(john_record)
    print("Запис John додано до адресної книги")

    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    print(f"Створено запис для Jane: {jane_record}")
    
    book.add_record(jane_record)
    print("Запис Jane додано до адресної книги")

    print("\n=== Пошук контактів ===")
    found_john = book.find("John")
    print(f"Знайдено запис John: {found_john}")

    try:
        book.find("NonExistent")
        print("Помилка: Неіснуючий контакт не повинен бути знайдений")
    except KeyError as e:
        print(f"Коректна обробка пошуку неіснуючого контакту: {e}")

    print("\n=== Керування телефонами ===")
    print("Редагування телефонів для John...")
    john_record.edit_phone("1234567890", "1112223333")
    print(f"Після редагування: {john_record}")

    found_phone = john_record.find_phone("5555555555")
    print(f"Знайдено телефон: {found_phone}")

    try:
        john_record.add_phone("123")
        print("Помилка: Некоректний телефон не повинен бути доданий")
    except ValueError as e:
        print(f"Коректна обробка некоректного телефону: {e}")

    print("\n=== Керування днями народження ===")
    try:
        john_record.add_birthday("01.01.1990")
        print(f"Додано день народження для John: {john_record}")
    except ValueError as e:
        print(f"Помилка додавання дня народження: {e}")

    try:
        jane_record.add_birthday("35.13.2022")
        print("Помилка: Некоректна дата не повинна бути додана")
    except ValueError as e:
        print(f"Коректна обробка некоректної дати: {e}")

    print("\n=== Перевірка найближчих днів народження ===")
    today = datetime.today()
    upcoming_date = (today + timedelta(days=5)).strftime("%d.%m.1995")
    try:
        jane_record.add_birthday(upcoming_date)
        print(f"Додано найближчий день народження для Jane: {jane_record}")
        
        upcoming_birthdays = book.get_upcoming_birthdays()
        if upcoming_birthdays:
            print("Знайдено найближчі дні народження:")
            for birthday in upcoming_birthdays:
                print(f"Ім'я: {birthday['name']}, Дата привітання: {birthday['congratulation_date']}")
        else:
            print("Найближчих днів народження не знайдено")
    except ValueError as e:
        print(f"Помилка встановлення дня народження: {e}")

    print("\n=== Видалення контактів ===")
    book.delete("Jane")
    print("Запис Jane видалено")

    try:
        book.find("Jane")
        print("Помилка: Видалений контакт не повинен бути знайдений")
    except KeyError as e:
        print(f"Коректна обробка пошуку видаленого контакту: {e}")

    print("\n=== Фінальний стан адресної книги ===")
    for name, record in book.data.items():
        print(f"Контакт: {record}")

if __name__ == "__main__":
    test_address_book_functionality()
