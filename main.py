
import os
import sys

from filemanager import FileManager
from formatting import Formatting
from inputhandler import InputHandler
from sqlitewrapper import SQLiteWrapper


#================================================================#
# Jamdomizer (tm) Jarrod Burns | ta747839@gmail.com | 10/14/2021 #
# Revision 2.0.1 - Update before commit                          #
#================================================================#


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
UNUSED_IDEAS = "UPCOMING_JAMS"
USED_IDEAS = "JAM_HISTORY"
ERROR_SQL_UNIQUE = "ERROR: All name entries must be unique."
SQL_SUCCESS = "Record created successfully!"

JSON_FILE_NAME = "data.json"

ERROR_INVALID_NAME = "ERROR: You must enter at least one character."
QUIT_MESSAGE = "Shutting down."
INVALID_INPUT = "Invalid input, try again."
MENU_OR_QUIT = 'Type "menu" to return or "quit" to exit.\nYour input: '
MENU_RETURN_MSG = "Returning to the main menu...\n"

MENU_MSG = """
    Menu
    1. Randomly select a new jam from the data set
    2. Add new jams to your list
    3. List all upcoming jams
    4. List all completed jams
    5. Back up all jam data
    6. Restore jam data from backup (Requires Conformation)
    7. Reset your data completely (Requires Conformation)
    8. Import/Export JSON data
    9. Quit
    """
print(welcome_message)
print("""
Select your destination by typing the appropriate number and pressing enter.
Return to this menu at any time by typing "menu"
Quit this application at any time by typing "quit" """)
print(MENU_MSG)

if not os.path.exists(DB_NAME):
    SQLiteWrapper(DB_NAME).create_table(UNUSED_IDEAS, False)
    SQLiteWrapper(DB_NAME).create_table(USED_IDEAS, False)

while True:

    menu_input = input("Your input: ")
    first_roll = True

    while menu_input == "1":                            # Roll new jam

        if SQLiteWrapper(DB_NAME).empty_table(UNUSED_IDEAS):
            print("You haven't created any jams yet. "
                  "Go and add some ideas first!")
            break

        if first_roll:
            jam_idea = SQLiteWrapper(DB_NAME).random_row(UNUSED_IDEAS)
            Formatting.display(88, "Jamdomizer", jam_idea[1], jam_idea[2])

            first_roll = False

        roll_input = input('\nType "YES" to use this idea, '
                           'NO to re-roll, or "menu" to return.\n'
                           "Your input: ")

        if InputHandler.yes(roll_input):
            SQLiteWrapper(DB_NAME).insert_row(USED_IDEAS, (jam_idea[1], jam_idea[2]))
            SQLiteWrapper(DB_NAME).delete_row_byid(UNUSED_IDEAS, str(jam_idea[0]))
            print(MENU_RETURN_MSG, MENU_MSG)
            break

        if InputHandler.no(roll_input):
            print("Randomizing jam ideas...")
            jam_idea = SQLiteWrapper(DB_NAME).random_row(UNUSED_IDEAS)
            Formatting.display(88, "Jamdomizer", jam_idea[1], jam_idea[2])
            first_roll = False
            continue

        if InputHandler.menu(roll_input):
            print(MENU_MSG)
            break

        if InputHandler.quit(roll_input, ["quit", "q"], False):
            print("No jam selected. Shutting down...")
            sys.exit()

        else:
            print(INVALID_INPUT)
            continue

    while menu_input == "2":                            # Add more jams

        if first_roll:
            user_jam_name = input("\nEnter the name of your Jam idea: ")

        if InputHandler.menu(user_jam_name):
            print(MENU_MSG)
            break

        if InputHandler.quit(user_jam_name):
            sys.exit()

        if not len(user_jam_name):
            print(ERROR_INVALID_NAME)
            continue

        if first_roll:
            user_jam_description = input("Enter a description for your idea: ")

        if InputHandler.menu(user_jam_description):
            print(MENU_MSG)
            break

        if InputHandler.quit(user_jam_description):
            sys.exit()

        if first_roll:
            SQLiteWrapper(DB_NAME).insert_row(
                UNUSED_IDEAS,
                (user_jam_name, user_jam_description)
            )

            first_roll = False

        continue_input = input("\nWould you like to enter another idea? (Y/N)\n"
                               "Your input: ")

        if InputHandler.yes(continue_input):
            first_roll = True
            continue

        if InputHandler.no(continue_input) or InputHandler.menu(continue_input):
            print(MENU_RETURN_MSG, MENU_MSG)
            break

        if InputHandler.quit(continue_input):
            sys.exit()

        else:
            print(INVALID_INPUT)

    while menu_input == "3":                            # List upcoming jams

        if SQLiteWrapper(DB_NAME).empty_table(UNUSED_IDEAS):
            print("There doesn't seem to be anything here. "
                  "Go to the menu and add some jams to get started!")
            break

        if first_roll:
            print("Showing all unselected jam ideas...")

            for idea in SQLiteWrapper(DB_NAME).all_table_rows(UNUSED_IDEAS):
                Formatting.display(88, "Jamdomizer", idea[0], idea[1])

            first_roll = False

        upcoming_jam_input = input(MENU_OR_QUIT)

        if InputHandler.menu(upcoming_jam_input):
            print(MENU_MSG)
            break

        if InputHandler.quit(upcoming_jam_input):
            sys.exit()

        else:
            print(INVALID_INPUT)

    while menu_input == "4":                            # List past jams

        if SQLiteWrapper(DB_NAME).empty_table(USED_IDEAS):
            print("You haven't completed any jams yet. "
                  "Go select and idea and start coding!")
            break

        if first_roll:
            print("Showing all previously selected jam ideas...\n")

            for idea in SQLiteWrapper(DB_NAME).all_table_rows(USED_IDEAS):
                Formatting.display(88, "Jamdomizer", idea[0], idea[1])

            first_roll = False

        old_jam_input = input(MENU_OR_QUIT)

        if InputHandler.menu(old_jam_input):
            print(MENU_MSG)
            break

        if InputHandler.quit(old_jam_input):
            sys.exit()

        else:
            print(INVALID_INPUT)

    while menu_input == "5":                            # Backup the DB

        if FileManager.backup_db(DB_NAME, "db_backup"):
            print(MENU_RETURN_MSG, MENU_MSG)
            break

        else:
            # Error message printing is thrown by backup_db so in the else case
            # this logic will return the user back to the main menu.
            print(MENU_RETURN_MSG, MENU_MSG)
            break

    while menu_input == "6":                            # Restore from backup

        restore_input = input(
            "\nSelecting a file will overwrite your current one.\n"
            "This could potentially result in a loss of data.\n"
            "It is recommended to back up your current file before proceeding.\n"
            'Type "YES" to continue, "menu" to return, or "quit" to exit.\n\n'
            'Your Input: '
        )

        if InputHandler.strict_yes(restore_input):
            if FileManager.restore_db(DB_NAME):
                print(MENU_RETURN_MSG, MENU_MSG)
                break

        if InputHandler.no(restore_input) or InputHandler.menu(restore_input):
            print(MENU_MSG)
            break

        if InputHandler.quit(restore_input):
            sys.exit()

        else:
            if not InputHandler.yes(restore_input):
                print(INVALID_INPUT)

    while menu_input == "7":                            # Reset everything

        reset_input = input("\nThis will completely reset ALL of your data. "
                            "Are you sure? (YES/NO)\nYour input: ")

        if InputHandler.strict_yes(reset_input):
            SQLiteWrapper(DB_NAME).drop_table(UNUSED_IDEAS)
            SQLiteWrapper(DB_NAME).drop_table(USED_IDEAS)
            SQLiteWrapper(DB_NAME).create_table(UNUSED_IDEAS)
            SQLiteWrapper(DB_NAME).create_table(USED_IDEAS)
            print(MENU_MSG)
            break

        if InputHandler.no(reset_input) or InputHandler.menu(reset_input):
            print("\nNo action taken.")
            print(MENU_RETURN_MSG, MENU_MSG)
            break

        if InputHandler.quit(reset_input):
            sys.exit()

        else:
            if not InputHandler.yes(reset_input):
                print(INVALID_INPUT)

    while menu_input == "8":                            # JSON I/O

        json_input = input(
            "\nSelect your destination by typing the "
            "appropriate number and pressing enter.\n\n"
            "    1. Export your database file to JSON format. "
            f'(File will be saved in:\n       {os.getcwd()} as "{JSON_FILE_NAME}")\n\n'
            "    2. Import a JSON file into the database."
            " (Expected format is:\n       {name: description, ...})\n\n"
            'You may type "menu" to return or "quit" to exit the application.\n\n'
            "Your Input: "
        )

        if json_input == "1":                       # JSON Out

            if SQLiteWrapper(DB_NAME).empty_table(UNUSED_IDEAS):
                print("\nYou don't have any data to export yet. "
                      "Go add some jams to your list first!\n")

                print(MENU_RETURN_MSG, MENU_MSG)
                break

            table_to_json = SQLiteWrapper(DB_NAME).all_table_rows(UNUSED_IDEAS)
            FileManager.dump_json(table_to_json, JSON_FILE_NAME)
            print(MENU_RETURN_MSG, MENU_MSG)
            break

        if json_input == "2":                       # JSON In

            json_data = FileManager.load_json()

            if json_data:
                for count, (k, v) in enumerate(json_data.items()):
                    print(f"\n------ Operation {count + 1} of {len(json_data)}:\n")
                    SQLiteWrapper(DB_NAME).insert_row(UNUSED_IDEAS, (k, v))

                print(MENU_MSG)
                break

        if InputHandler.menu(json_input):
            print(MENU_MSG)
            break

        if InputHandler.quit(json_input):
            sys.exit()

        else:
            print(INVALID_INPUT)

    if InputHandler.quit(menu_input, ["9", "quit", "exit", "q"]):   # Terminate app
        sys.exit()

    if menu_input.lower() not in ["1", "2", "3", "4", "5",
                                  "6", "7", "8", "9",
                                  "quit", "q", "exit"]:
        print(INVALID_INPUT)
