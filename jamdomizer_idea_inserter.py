
import sqlite3

conn = sqlite3.connect('codejam.db')
cursor = conn.cursor()

error_invalid_name = "ERROR: You must enter at least one character."
error_sql_unique = "ERROR: All name entries must be unique."
sql_success = "Record created successfully!"

print('You may type "Quit" at any time to close this application.')


while True:
    user_jam_name = input("Enter the name of your Jam idea: ")

    # Not DRY, Rewrite as function & try except later.
    if user_jam_name.lower() == "quit":
        print("Shutting down.")
        conn.close()
        break

    if len(user_jam_name) < 1:
        print(error_invalid_name)
        continue

    user_jam_description = input("Enter a description for your idea: ")

    # Not DRY, Rewrite as function & try except later.
    if user_jam_description.lower() == "quit":
        print("Shutting down.")
        conn.close()
        break

    try:
        cursor.execute('''INSERT INTO UNUSED_JAM_IDEAS(
            NAME, DESCRIPTION) VALUES
            ('{}', '{}')'''.format(user_jam_name, user_jam_description))
        conn.commit()
        print(sql_success)

    except sqlite3.IntegrityError:
        print(error_sql_unique)

# Close the DB connection if the user breaks out of the loop somehow.
conn.close()
