
import os
import sqlite3
import sys
import tkinter as tk
from datetime import datetime
from os.path import exists
from shutil import copyfile, SameFileError
from textwrap import TextWrapper
from tkinter import filedialog


# TODO:

# Write helper note to explain random logic
# Display Used and Unused Jams are basically the same, combine to reduce code
# Add way to delete bad jam inputs
# JSON dump
# JSON to db slurper
# Clean up function documentation
# Investigate SQL Uniqueness
# Consider sub menu for file management options
# Menu option -- Restore DB from backup -- DONE
# Menu option -- Create DB backup -- DONE
# Menu option -- full jam list -- DONE

# --------------------------- INPUT HANDLERS -------------------------- #


def quit_check(user_input: str,
               valid_input: list[str, ...] = ["quit"],
               default_message_on: bool = True) -> bool:
    """
    pass
    """
    if user_input.lower() in valid_input:
        if default_message_on:
            print("Shutting Down...")
        return True


def menu_check(user_input: str,
               valid_input: list[str, ...] = ["menu"],
               default_message_on: bool = True) -> bool:
    """
    pass
    """
    if user_input.lower() in valid_input:
        if default_message_on:
            print("Returning to the main menu...")
        return True


def no_check(user_input: str,
             valid_input: list[str, ...] = ["no", "n"]) -> bool:
    """
    pass
    """
    if user_input.lower() in valid_input:
        return True


def yes_check(user_input: str,
              valid_input: list[str, ...] = ["yes", "y"]) -> bool:
    """
    pass
    """
    if user_input.lower() in valid_input:
        return True


def strict_yes_check(user_input: str,
                     valid_input: list[str, ...] = ["YES"],
                     default_message_on: bool = True) -> bool:
    """
    pass
    """
    if user_input in valid_input:
        if default_message_on:
            print("Input accepted, erasing all data...\n")
        return True

    if yes_check(user_input):
        if default_message_on:
            for phrase in valid_input:
                print(f'Reset command must be entered exactly: "{phrase}"')
        return False


# -------------------------------- SQL ------------------------------- #


def sql_insert(db_name: str,
               table_name: str,
               row_name: str,
               row_description: str) -> None:
    """
    pass
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    insert_statment = """INSERT INTO {}
                         (NAME, DESCRIPTION)
                         VALUES (?, ?)""".format(table_name)

    insert_values = (row_name, row_description)
    cursor.execute(insert_statment, insert_values)
    conn.commit()
    conn.close()


def sql_delete(db_name: str,
               table_name: str,
               row_id: int) -> None:
    """
    pass
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("""DELETE from {}
                      WHERE ROWID={}""".format(table_name, row_id))

    conn.commit()
    conn.close()


def all_table_rows(db_name: str, table_name: str) -> list[tuple[str, ...], ...]:
    """
    pass
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM USED_JAM_IDEAS")
    all_rows = cursor.fetchall()
    conn.close()
    return all_rows


def random_table_row(db_name: str, table_name: str) -> tuple[int, str, str]:
    """
    Selects a random row from the specified table.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("""SELECT ROWID, * from {}
                      ORDER BY RANDOM()
                      LIMIT 1""".format(table_name))

    selected_row = cursor.fetchone()
    conn.close()
    return selected_row


def empty_table(db_name: str, table_name: str) -> bool:
    """
    pass
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("""SELECT count(*) FROM {}""".format(table_name))
    row_count = cursor.fetchone()
    conn.close()

    if not row_count[0]:
        return True
    return False


def table_maker(db_name: str,
                table_names: list[str, ...],
                print_creation_message: bool = True) -> None:
    """
    pass
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    for name in table_names:
        cursor.execute("""DROP TABLE IF EXISTS {}""".format(name))

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS {} (
            NAME VARCHAR(200) NOT NULL,
            DESCRIPTION TEXT,
            UNIQUE(NAME, DESCRIPTION)
            )""".format(name))

        if print_creation_message:
            print(name.lower().title().replace("_", " "),
                  "deleted successfully!")

    conn.commit()
    conn.close()


# ----------------------------- FORMATTING ---------------------------- #


def simple_text_wrap(wrap_length: int, text_to_wrap: str) -> None:
    """
    pass
    """
    wrapped_text = TextWrapper(width=wrap_length).wrap(text_to_wrap)

    for line in wrapped_text:
        print(line)


def fancy_text_display(wrap_length: int,
                       app_name: str,
                       title: str,
                       body: str,
                       pad_char: str = "=") -> None:
    """
    Formats text for display.
    """
    top_padding = pad_char * ((wrap_length - len(app_name) - 2) // 2)
    middle = wrap_length - (len(app_name) * 2 + 10)

    print(top_padding, app_name, top_padding, "\n")
    print(title.center(wrap_length), "\n")
    simple_text_wrap(wrap_length, body)
    print("\n" + pad_char * 3,
          app_name, pad_char * middle, app_name,
          pad_char * 3 + "\n")


# -------------------------- FILE MANAGEMENT -------------------------- #


def file_backup(file_name: str, dst_folder_name: str) -> bool:
    """
    Backup your file to the specified folder name
    in the current working directory.
    """
    timestamp = (datetime.now().strftime("%b-%d-%y_%H%M%S").upper())
    cwd = os.getcwd()
    os.makedirs(f"{cwd}/{dst_folder_name}/", exist_ok=True)
    src = f"{cwd}/{file_name}"
    dst = f"{cwd}/{dst_folder_name}/{timestamp}_{file_name}"

    try:
        copyfile(src, dst)
        return True
    except FileNotFoundError:
        print(f'ERROR: Operation could not be completed '
              f'because "{file_name}" does not exist!')
        return False


def restore_db_from_backup(file_name: str) -> bool:
    """
    pass
    """
    tk.Tk().withdraw()
    cwd = os.getcwd()
    file = filedialog.askopenfilename(initialdir=cwd, filetypes=[
        ("SQLite Database files", ".db"),
        ("SQLite Database files", ".sqlite"),
        ("SQLite Database files", ".sqlite3"),
        ("SQLite Database files", ".db3"),
    ])
    try:
        copyfile(file, f"{cwd}/{file_name}")
        return True
    except FileNotFoundError:
        print("ERROR: Operation could not be completed because the "
              "file does not exist or a file was not selected!")
        return False
    except SameFileError:
        print("You can not restore a backup from the current active file.")
        return False


# -------------------------------- MAIN ------------------------------- #


welcome_message = """
db   d8b   db d88888b db       .o88b.  .d88b.  .88b  d88. d88888b     d888888b  .d88b.
88   I8I   88 88'     88      d8P  Y8 .8P  Y8. 88'YbdP`88 88'         `~~88~~' .8P  Y8.
88   I8I   88 88ooooo 88      8P      88    88 88  88  88 88ooooo        88    88    88
Y8   I8I   88 88~~~~~ 88      8b      88    88 88  88  88 88~~~~~        88    88    88
`8b d8'8b d8' 88.     88booo. Y8b  d8 `8b  d8' 88  88  88 88.            88    `8b  d8'
 `8b8' `8d8'  Y88888P Y88888P  `Y88P'  `Y88P'  YP  YP  YP Y88888P        YP     `Y88P'


   d88b  .d8b.  .88b  d88. d8888b.  .d88b.  .88b  d88. d888888b d88888D d88888b d8888b.
   `8P' d8' `8b 88'YbdP`88 88  `8D .8P  Y8. 88'YbdP`88   `88'   YP  d8' 88'     88  `8D
    88  88ooo88 88  88  88 88   88 88    88 88  88  88    88       d8'  88ooooo 88oobY'
    88  88~~~88 88  88  88 88   88 88    88 88  88  88    88      d8'   88~~~~~ 88`8b
db. 88  88   88 88  88  88 88  .8D `8b  d8' 88  88  88   .88.    d8' db 88.     88 `88.
Y8888P  YP   YP YP  YP  YP Y8888D'  `Y88P'  YP  YP  YP Y888888P d88888P Y88888P 88   YD
......::..:::..:..::..::..:.......::......::..::..::..:........:.......:.......:..:::..:
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
========================================================================================
"""

DB_NAME = "codejam.db"
TABLE_NAMES = ["UNUSED_JAM_IDEAS", "USED_JAM_IDEAS"]
ERROR_INVALID_NAME = "ERROR: You must enter at least one character."
ERROR_SQL_UNIQUE = "ERROR: All name entries must be unique."
SQL_SUCCESS = "Record created successfully!"
QUIT_MESSAGE = "Shutting down."
UNUSED_IDEAS = "UNUSED_JAM_IDEAS"
USED_IDEAS = "USED_JAM_IDEAS"
INVALID_INPUT = "Invalid input, try again."

MENU_MESSAGE = """
    Menu
    1. Randomly select a new jam from the data set
    2. Add new jams to your list
    3. List all upcoming used jams
    4. List all completed jams
    5. Back up all jam data
    6. Restore jam data from backup. (Requires Conformation)
    7. Reset your data completely. (Requires Conformation)
    8. Quit
    """
print(welcome_message)
print("""
Select your destination by typing the appropriate number and pressing enter.
Return to this menu at any time by typing "menu"
Quit this application at any time by typing "quit" """)
print(MENU_MESSAGE)

if not exists(DB_NAME):
    table_maker(DB_NAME, TABLE_NAMES, False)


while True:

    menu_input = input("Your input: ")

    while menu_input == "1":                            # Roll new jam

        first_roll = True

        if empty_table(DB_NAME, UNUSED_IDEAS):
            print("You haven't created any jams yet. "
                  "Go and add some ideas first!")
            break

        if first_roll:
            jam_idea = random_table_row(DB_NAME, UNUSED_IDEAS)
            fancy_text_display(88, "Jamdomizer", jam_idea[1], jam_idea[2])

        roll_input = input("\nSelect YES to use this idea, "
                           "NO to re-roll, or QUIT to exit. (Y/N/Q)?")

        if yes_check(roll_input):
            sql_insert(DB_NAME, USED_IDEAS, jam_idea[1], jam_idea[2])
            sql_delete(DB_NAME, UNUSED_IDEAS, jam_idea[0])

            print("Selection approved. Returning to main menu.\n")
            print(MENU_MESSAGE)
            break

        if no_check(roll_input):
            print("Re-randomizing jam_ideas...\n")
            jam_idea = random_table_row(DB_NAME, UNUSED_IDEAS)
            fancy_text_display(88, "Jamdomizer", jam_idea[1], jam_idea[2])
            first_roll = False
            continue

        if menu_check(roll_input):
            print(MENU_MESSAGE)
            break

        if quit_check(roll_input, ["quit", "q"], False):
            print("\nNo jam selected. Shutting down...\n")
            sys.exit()

        else:
            print(INVALID_INPUT)
            continue

    while menu_input == "2":                            # Add more jams

        user_jam_name = input("Enter the name of your Jam idea: ")

        if menu_check(user_jam_name):
            print(MENU_MESSAGE)
            break

        if quit_check(user_jam_name):
            sys.exit()

        if not len(user_jam_name):
            print(ERROR_INVALID_NAME)
            continue

        user_jam_description = input("Enter a description for your idea: ")

        if menu_check(user_jam_description):
            print(MENU_MESSAGE)
            break

        if quit_check(user_jam_description):
            sys.exit()

        try:
            # Name row doesn't seem to care about uniquness anymore, check this.
            sql_insert(DB_NAME, UNUSED_IDEAS, user_jam_name, user_jam_description)
            print(SQL_SUCCESS)

        except sqlite3.IntegrityError:
            print(ERROR_SQL_UNIQUE)

        continue_input = input("Whould you like to enter another idea? (Y/N) ")

        if yes_check(continue_input):
            continue

        if no_check(continue_input) or menu_check(continue_input):
            print(MENU_MESSAGE)
            break

        if quit_check(continue_input):
            sys.exit()

    while menu_input == "3":                            # List upcoming jams

        print("Showing all unselected jam ideas...\n")

        if empty_table(DB_NAME, UNUSED_IDEAS):
            print("There doesn't seem to be anything here. "
                  "Go to the menu and add some jams to get started!")
            break

        for idea in all_table_rows(DB_NAME, UNUSED_IDEAS):
            fancy_text_display(88, "Jamdomizer", idea[0], idea[1])

        upcoming_jam_input = input("Type menu to return or quit to exit."
                                   "\nYour input: ")

        if menu_check(upcoming_jam_input):
            print(MENU_MESSAGE)
            break

        if quit_check(upcoming_jam_input):
            sys.exit()

        else:
            print(INVALID_INPUT)

    while menu_input == "4":                            # List past jams

        print("Showing all previously selected jam ideas...\n")

        if empty_table(DB_NAME, USED_IDEAS):
            print("You haven't completed any jams yet. "
                  "Go select and idea and start coding!")
            break

        for idea in all_table_rows(DB_NAME, USED_IDEAS):
            fancy_text_display(88, "Jamdomizer", idea[0], idea[1])

        old_jam_input = input("Type menu to return or quit to exit.\nYour input: ")

        if menu_check(old_jam_input):
            print(MENU_MESSAGE)
            break

        if quit_check(old_jam_input):
            sys.exit()

        else:
            print(INVALID_INPUT)

    while menu_input == "5":                            # Backup the DB

        if file_backup(DB_NAME, "db_backup"):
            print("File back up successful! "
                  "Returning to the main menu...")
            print(MENU_MESSAGE)
            break

        else:
            print("\nReturning to the main menu...")
            break

    while menu_input == "6":                            # Restore from backup
        restore_input = input("\nSelecting a file will overwrite your current one.\n"
                              "This could potentially result in a loss of data.\n"
                              "It is recommended to back up your current file before proceeding.\n"
                              'Type "YES" to continue, menu to return, or quit to exit.\n\n'
                              'Your Input: ')

        if strict_yes_check(restore_input, default_message_on=False):
            if restore_db_from_backup(DB_NAME):
                print("File restoration successful! "
                      "Returning to the main menu...")
                print(MENU_MESSAGE)
                break

        if no_check(restore_input) or menu_check(restore_input):
            print(MENU_MESSAGE)
            break

        if quit_check(restore_input):
            sys.exit()

        else:
            if not yes_check(restore_input):
                print(INVALID_INPUT)

    while menu_input == "7":                            # Reset everything

        reset_input = input("\nThis will completely reset ALL of your data. "
                            "Are you sure? (YES/NO)")

        if strict_yes_check(reset_input):
            table_maker(DB_NAME, TABLE_NAMES)
            print(MENU_MESSAGE)
            break

        if no_check(reset_input) or menu_check(reset_input):
            print(MENU_MESSAGE)
            break

        if quit_check(reset_input):
            sys.exit()

        else:
            if not yes_check(reset_input):
                print(INVALID_INPUT)

    if quit_check(menu_input, ["8", "quit", "exit", "q"]):   # Terminate app
        sys.exit()

    if menu_input.lower() not in ["1", "2", "3", "4",
                                  "5", "6", "7", "8",
                                  "quit", "exit"]:
        print(INVALID_INPUT)
