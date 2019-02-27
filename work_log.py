import datetime
import os
import sys

from peewee import *


db = SqliteDatabase('work_log.db')


class Entry(Model):
    timestamp = DateTimeField(default=datetime.datetime.today()
                              .strftime('%m/%d/%Y'))
    employee_name = TextField()
    task_title = TextField()
    time_spent = IntegerField()
    task_notes = TextField()

    class Meta:
        database = db


def initialize():
    """Create the database and the table if they don't exist"""
    db.connect()
    db.create_tables([Entry], safe=True)


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def work_log():
    menu = """WORK LOG
What would you like to do?
a) Add new entry
b) Search in existing entries
c) Quit program"""
    while True:
        print(menu)
        menu_select = None
        while not menu_select:
            menu_select = input("> ")
            if menu_select == "a":
                new_entry()
            elif menu_select == "b":
                search_entries()
            elif menu_select == "c":
                sys.exit(0)
            else:
                pass


def new_entry():
    clear_screen()
    while True:
        name = input('Employee name: ').strip()
        if validate_name_input(name):
            break
    while True:
        title = input('Task title: ').strip()
        if validate_title_input(title):
            break
    while True:
        duration = input('Time spent (in minutes): ').strip()
        if validate_duration_input(duration):
            break
    notes = input('Notes (optional): ').strip()
    validate_notes_input(notes)
    add_entry(name, title, duration, notes)


def validate_name_input(name):
    if all(letter.isalpha() or letter.isspace()
           for letter in name) and len(name) != 0:
        clear_screen()
        return True

    else:
        clear_screen()
        print('Please enter a name of consisting of letters and spaces')
        return False


def validate_title_input(title):
    if len(title) != 0:
        clear_screen()
        return True

    else:
        clear_screen()
        print('Please enter a task title')
        return False


def validate_duration_input(duration):
    if duration.isdigit():
        duration = int(duration)
        clear_screen()
        return duration

    else:
        clear_screen()
        print('Time spent on task (nearest whole minute)')
        return False


def validate_notes_input(notes):
    if len(notes) == 0:
        notes = 'None'
    clear_screen()
    return notes


def add_entry(name, title, duration, notes):
    clear_screen()
    print('Entry added to work log!')
    return Entry.create(
        employee_name=name,
        task_title=title,
        time_spent=duration,
        task_notes=notes
    )


def search_entries():
    clear_screen()
    menu = """How would you like to search?
a) Employee
b) Date
c) Duration
d) Term (Task Name or Notes)
e) Return to Main Menu"""

    print(menu)
    menu_select = None
    while not menu_select:
        menu_select = input("> ")
        if menu_select == "a":
            employee_search()
        elif menu_select == "b":
            date_search()
        elif menu_select == "c":
            duration_search()
        elif menu_select == "d":
            term_search()
        elif menu_select == "e":
            work_log()


def display_results(search_results):
    clear_screen()
    if search_results:
        print("---- Matched Task(s) ----")
        for task in search_results:
            print("""
Employee: {}
Date: {}
Title: {}
Time Spent (mins): {}
Notes: {}
"""
                  .format(task.employee_name, task.timestamp, task.task_title, task.time_spent, task.task_notes))
        input("Please press enter to return to the menu.")
        clear_screen()


def employee_search():
    search_results = []
    unique_names = get_unique_employees()
    while True:
        if len(unique_names) > 1:
            print('Entries found by {} and {}.'.format(
                ', '.join(unique_names[:-1]),
                unique_names[-1]))
        elif len(unique_names) == 1:
            print('Entries written by {}.'.format(unique_names[0]))

        search_query = input('Search for entries written by: ')
        if validate_employee_search_format(search_query):
            break
        print('Enter a name consisting only of letter and spaces')
    search_results.append(Entry.select().where(Entry.employee_name == search_query))
    for result in search_results:
        #        for thing in result:
        display_results(result)


def get_unique_employees():
    unique_names = []

    for entry in Entry.select():
        if entry.employee_name not in unique_names:
            unique_names.append(entry.employee_name)

    clear_screen()
    return unique_names


def validate_employee_search_format(search_query):
    if (all(letter.isalpha() or letter.isspace() for letter in
            search_query) and len(search_query) != 0):
        clear_screen()
        return True

    else:
        clear_screen()
        return False


def date_search():
    search_results = []
    unique_dates = get_unique_dates()
    while True:
        if unique_dates:
            print('Entries found for {} and {}.'.format(
                ', '.join(unique_dates[:-1]),
                unique_dates[-1]))
        elif len(unique_dates) == 1:
            print('Entries found for {}.'.format(unique_dates[0]))

        search_query = input('Show entries for (MM/DD/YYYY): ')
        if validate_date_search_format(search_query):
            break
        print('Please enter date in format MM/DD/YYYY')
    search_results.append(Entry.select().where(Entry.timestamp == search_query))
    for result in search_results:
        display_results(result)


def get_unique_dates():
    unique_dates = []

    for entry in Entry.select():
        if entry.timestamp not in unique_dates:
            unique_dates.append(entry.timestamp)

    clear_screen()
    return unique_dates


def validate_date_search_format(search_query):
    try:
        datetime.datetime.strptime(search_query, '%m/%d/%Y')
        clear_screen()
        return search_query

    except ValueError:
        clear_screen()
        return False


def duration_search():
    search_results = []
    while True:
        search_query = input('Time spent (in minutes): ')
        if validate_duration_search_format(search_query):
            break
        print('Please enter positive integer')
    search_results.append(Entry.select().where(Entry.time_spent == search_query))
    for result in search_results:
        display_results(result)


def validate_duration_search_format(search_query):
    if search_query.isdigit():
        clear_screen()
        return int(search_query)

    else:
        clear_screen()
        return False


def term_search():
    search_results = []
    while True:
        search_query = input('Show entries containing: ')
        if validate_term_search_format(search_query):
            break
        print('Enter search term')
    search_results.append(Entry.select().where(Entry.employee_name.contains(search_query)) |
                          Entry.select().where(Entry.task_notes.contains(search_query)))
    for result in search_results:
        display_results(result)


def validate_term_search_format(search_query):
    if len(search_query) != 0:
        clear_screen()
        return True

    else:
        clear_screen()
        return False


if __name__ == "__main__":
    initialize()
    work_log()
