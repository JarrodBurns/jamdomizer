
class InputHandler:

    def quit(user_input: str,
             valid_input: list[str, ...] = ["quit"],
             default_message_on: bool = True) -> bool:

        if user_input.lower() in valid_input:
            if default_message_on:
                print("Shutting Down...")
            return True

    def menu(user_input: str,
             valid_input: list[str, ...] = ["menu"],
             default_message_on: bool = True) -> bool:

        if user_input.lower() in valid_input:
            if default_message_on:
                print("Returning to the main menu...")
            return True

    def no(user_input: str,
           valid_input: list[str, ...] = ["no", "n"]) -> bool:

        if user_input.lower() in valid_input:
            return True

    def yes(user_input: str,
            valid_input: list[str, ...] = ["yes", "y"]) -> bool:

        if user_input.lower() in valid_input:
            return True

    @classmethod
    def strict_yes(cls,
                   user_input: str,
                   valid_input: list[str, ...] = ["YES"],
                   default_message_on: bool = True) -> bool:
        """
        pass
        """
        if user_input in valid_input:
            if default_message_on:
                print("Input accepted, preforming operation...\n")
            return True

        if cls.yes(user_input):
            if default_message_on:
                for phrase in valid_input:
                    print(f'Command must be entered exactly: "{phrase}"')
            return False


def main():
    pass


if __name__ == "__main__":
    main()
