
import sqlite3


conn = sqlite3.connect('codejam.db')
cursor = conn.cursor()
table_to_read = "UNUSED_JAM_IDEAS"
table_to_write = "USED_JAM_IDEAS"


def random_table_row(table_to_read: str) -> tuple:
    """
    Selects a random row from the specified table.
    """
    cursor.execute('''SELECT ROWID, * from {}
        ORDER BY RANDOM() LIMIT 1'''.format(table_to_read))
    selected_row = cursor.fetchone()
    return selected_row


def simple_text_wrap(text_to_wrap: str, wrap_length: int):
    """
    Python already has a way to do this, but it requires an
    import and is assuredly less fun.

    Splits input text at the specified length.
    Returns a generator expression.
    """
    return (
        text_to_wrap[:wrap_length]
        if line_number == 0
        else text_to_wrap[
            line_number * wrap_length:(line_number + 1) * wrap_length
        ]
        for line_number in range(len(text_to_wrap) // wrap_length + 1)
    )


def final_text_display(jam_idea: tuple) -> str:
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

    return "".join(t)


jam_idea = random_table_row(table_to_read)
print(final_text_display(jam_idea))


while True:

    user_input = input(
        "\nSelect YES to use this idea, NO to re-roll, or QUIT to exit.\n(Y/N/Q)?"
    )

    if user_input.lower() in ["y", "yes"]:
        cursor.execute('''INSERT INTO {}(
            NAME, DESCRIPTION) VALUES
            ('{}', '{}')'''.format(table_to_write, jam_idea[1], jam_idea[2]))

        cursor.execute('''DELETE from {}
            WHERE ROWID={}'''.format(table_to_read, jam_idea[0]))

        print("Selection approved. Shutting down.\n")
        conn.commit()
        conn.close()
        break

    elif user_input.lower() in ["n", "no"]:
        print("Re-randomizing jam_ideas...\n")

        jam_idea = random_table_row(table_to_read)
        print(final_text_display(jam_idea))
        continue

    elif user_input.lower() in ["q", "quit"]:
        print("\nNo jam selected. Shutting down.\n")
        conn.close()
        break

    else:
        print("Invalid input, try again.\n")
        continue

# Close the DB connection if the user breaks out of the loop somehow.
conn.close()
