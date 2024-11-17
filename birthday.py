import datetime

def input_error(func):
    def wrapper(args, book):
        try:
            return func(args, book)
        except ValueError as e:
            return str(e)
        except IndexError:
            return "Invalid number of arguments."
        except Exception as e:
            return str(e)
    return wrapper

class Birthday:
    def __init__(self, value):
        try:
            
            self.value = datetime.datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Field:
    def __init__(self, value):
        self.value = value

class Name(Field):
    pass

class Phone(Field):
    pass

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

class AddressBook:
    def __init__(self):
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def find(self, name):
        for record in self.records:
            if record.name.value == name:
                return record
        return None

    def get_upcoming_birthdays(self):
        upcoming_birthdays = []
        today = datetime.date.today()
        for record in self.records:
            if record.birthday:
                delta = record.birthday.value - today
                if 0 <= delta.days <= 7:
                    birthday_date = record.birthday.value
                    if birthday_date.weekday() == 5:  
                        birthday_date = birthday_date + datetime.timedelta(days=2)
                    elif birthday_date.weekday() == 6:  
                        birthday_date = birthday_date + datetime.timedelta(days=1)
                    upcoming_birthdays.append({
                        "name": record.name.value,
                        "birthday": birthday_date.strftime("%d.%m.%Y")
                    })
        return upcoming_birthdays

@input_error
def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)
    if not record:
        return f"Contact {name} not found."
    record.add_birthday(birthday)
    return f"Birthday for {name} added."

@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if not record or not record.birthday:
        return f"Birthday for {name} not found."
    return f"{name}'s birthday is {record.birthday.value.strftime('%d.%m.%Y')}."

@input_error
def birthdays(args, book):
    upcoming_birthdays = book.get_upcoming_birthdays()
    if not upcoming_birthdays:
        return "No upcoming birthdays in the next 7 days."
    return "\n".join([f"{entry['name']} - {entry['birthday']}" for entry in upcoming_birthdays])

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = user_input.split()

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
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