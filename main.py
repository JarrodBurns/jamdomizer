
import sqlite3
import sys
from os.path import exists


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
            print(f'Reset command must be entered exactly: "{valid_input}"')
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


def simple_text_wrap(text_to_wrap: str, wrap_length: int):
    """
    Python already has a way to do this, but it requires an
    import and is assuredly less fun.

    Splits input text at the specified length.
    Returns a generator expression.
    """
    return (
        text_to_wrap[:wrap_length]
        if not line_number
        else text_to_wrap[line_number * wrap_length:(line_number + 1) * wrap_length]
        for line_number in range(len(text_to_wrap) // wrap_length + 1)
    )


def final_text_display(jam_idea: tuple[int, str, str]) -> str:
    """
    Formats text for display.
    """
    t = []
    top_text_border = ("=" * 10, " Code Jam ", "=" * 10, "\n")
    bottom_text_border = ("=" * 30)

    for i in top_text_border:
        t.append(i)

    t.append("\n")
    t.append(jam_idea[1].center(28))
    t.append("\n\n")

    for i in simple_text_wrap(jam_idea[2], 30):
        t.append(i)
        t.append("\n")

    t.append(bottom_text_border)
    t.append("\n")

    return "".join(t)


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
......::..:::..:..::..::..:.......::......::..::..::..:........:.......:.......:..:::..
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
=======================================================================================
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
    1. Randomly select a new jam from the dataset
    2. Add new jams to your list
    3. See the used jams
    4. Reset your data completely. (Requires Conformation)
    5. Quit
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
            print(final_text_display(jam_idea))

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
            print(final_text_display(jam_idea))
            first_roll = False
            continue

        if menu_check(roll_input):
            print(MENU_MESSAGE)
            break

        if quit_check(roll_input, ["quit", "q"]):
            print("\nNo jam selected. Shutting down.\n")
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

    while menu_input == "3":                            # See past jams

        print("Showing all previously selected jam ideas...\n")

        if empty_table(DB_NAME, USED_IDEAS):
            print("You haven't completed any jams yet. "
                  "Go select and idea and start coding!")
            break

        for pos, idea in enumerate(all_table_rows(DB_NAME, USED_IDEAS)):
            print("=" * 30)
            print(f"Jam #{pos + 1}:  {idea[0]}\n")
            print(*simple_text_wrap(f"Description:  {idea[1]}", 30), sep="\n")
            print("=" * 30, "\n")

        old_jam_input = input("Type menu to return or quit to exit.\nYour input: ")

        if menu_check(old_jam_input):
            print(MENU_MESSAGE)
            break

        if quit_check(old_jam_input):
            sys.exit()

        else:
            print(INVALID_INPUT)

    while menu_input == "4":                            # Reset everything

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

    if quit_check(menu_input, ["5", "quit", "exit"]):   # Terminate app
        sys.exit()

    if menu_input.lower() not in ["1", "2", "3", "4", "5", "quit", "exit"]:
        print(INVALID_INPUT)
