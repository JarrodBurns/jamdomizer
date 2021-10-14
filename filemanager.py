
import json
import os
import shutil
import tkinter
import tkinter as tk
from datetime import datetime
from tkinter import filedialog


class FileManager:

    def backup_db(file_to_backup: str, dst_folder_name: str) -> bool:
        """
        Backup your file to the specified folder name
        in the current working directory.
        """
        timestamp = (datetime.now().strftime("%b-%d-%y_%H%M%S").upper())
        cwd = os.getcwd()
        os.makedirs(f"{cwd}\\{dst_folder_name}\\", exist_ok=True)
        src = f"{cwd}\\{file_to_backup}"
        dst = f"{cwd}\\{dst_folder_name}\\{timestamp}_{file_to_backup}"

        try:
            shutil.copyfile(src, dst)
            print(f'Database back up created successfully. Your file is saved in:\n{dst}')
            return True
        except FileNotFoundError:
            print(f'ERROR: Operation could not be completed.\n'
                  f'       "{file_to_backup}" does not exist.')
            return False

    def restore_db(save_file_as: str) -> bool:

        window = tk.Tk()
        window.attributes("-topmost", True)     # Always on top for Windows
        window.lift()                           # Always on top for Linux/Mac
        window.withdraw()
        cwd = os.getcwd()
        file = filedialog.askopenfilename(
            initialdir=cwd,
            title="Select a File",
            filetypes=[
                ("SQLite Database files", ".db"),
                ("SQLite Database files", ".sqlite"),
                ("SQLite Database files", ".sqlite3"),
                ("SQLite Database files", ".db3"),
            ])
        try:
            shutil.copyfile(file, f"{cwd}/{save_file_as}")
            print("Restoration from back up executed successfully.")
            return True
        except FileNotFoundError:
            print("ERROR: Operation could not be completed.\n"
                  "       File does not exist or was not selected.")
            return False
        except shutil.SameFileError:
            print("ERROR: File in use by this application.\n"
                  '       By default back ups are stored in the folder "db_backup"')
            return False

    def dump_json(data_to_write: list[tuple[str, str], ...],
                  json_file_name: str,
                  default_message_on: bool = True) -> None:

        json_data = {name: desc for name, desc in data_to_write}
        with open(json_file_name, "w") as file_handle:
            json.dump(json_data, file_handle, indent=2)

        if default_message_on:
            print(f'{len(json_data)} object(s) '
                  f'written to "{json_file_name}" successfully.')

    def load_json() -> dict[str, str, ...] or None:

        window = tk.Tk()
        window.attributes("-topmost", True)     # Always on top for Windows
        window.lift()                           # Always on top for Linux/Mac
        window.withdraw()
        cwd = os.getcwd()
        file = tk.filedialog.askopenfilename(
            initialdir=cwd,
            title="Select a File",
            filetypes=[
                ("JSON Files", ".json")
            ])
        try:
            with open(file, "r") as file_handle:
                return json.load(file_handle)
        except FileNotFoundError:
            print("ERROR: Operation could not be completed.\n"
                  "       No file was selected.")


def main():
    pass


if __name__ == "__main__":
    main()
