
"""
This script will drop and create tables from the table_names list.
Take care not to reuse this outside of a trusted environment as it
is vulnerable to SQL injection.
"""

import sqlite3

drop_statement = "DROP TABLE IF EXISTS"
table_names = ["UNUSED_JAM_IDEAS", "USED_JAM_IDEAS"]
success_statment = "created successfully!"

conn = sqlite3.connect('codejam.db')
cursor = conn.cursor()


for name in table_names:
    #Drop all tables in the list
    cursor.execute(f"{drop_statement} {name}")

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS {} (
        NAME VARCHAR(200) NOT NULL,
        DESCRIPTION TEXT,
        UNIQUE(NAME, DESCRIPTION)
        )'''.format(name))

    print(name, success_statment)


conn.commit()
conn.close()
