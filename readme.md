# The Jamdomizer

Files should be executed in the folowing order:

1. jamdomizer_table_creation.py
2. jamdomizer_idea_inserter.py
3. jamdomizer.py

## DISCLAMER
Some of the methods employed here are **NOT** suitable for use outside of a trusted environment as they are vulnerable to **SQL injection**. You have been warned.

## Purpose
These scripts are intended to preform C.R.U.D functionality for a database of code jam ideas. 

## jamdomizer_table_creation.py
Quickly creates SQLite tables. 

**WARNING** This script intentionally drops all tables with the specified name before creating them again. As such it will **PERMANENTLY** delete your information if ran after storing your data. Execute with extreme care and always back up your tables before working on them.

## jamdomizer_idea_inserter.py
When executed, with your terminal of choice, this script will allow you to easily insert information into your created tables.

## jamdomizer.py
Selects a random row from previously created tables and prompts the user with that information. If approved, the data will be dropped from the selection table, to prevent it from being reused, and then written to a separate table for posterity.

## Version Control
The Jamdomizer and all related files are dependent on the following:

- [python](https://docs.python.org/3/) 3.9.6

## Conclusion
Thank you for taking the time to review the readme, if you have any questions feel free to message my twitter bot, @BotJarrod or my gmail at ta747839@gmail.com