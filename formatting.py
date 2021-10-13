
from textwrap import TextWrapper


class Formatting():

    def simple_text_wrap(wrap_length: int, text_to_wrap: str) -> None:

        wrapped_text = TextWrapper(width=wrap_length).wrap(text_to_wrap)

        for line in wrapped_text:
            print(line)

    @classmethod
    def display(cls,
                wrap_length: int,
                app_name: str,
                title: str,
                body: str,
                pad_char: str = "=") -> None:

        top_padding = pad_char * ((wrap_length - len(app_name) - 2) // 2)
        middle = wrap_length - (len(app_name) * 2 + 10)

        print("\n\n" + top_padding, app_name, top_padding, "\n")
        print(title.center(wrap_length), "\n")
        cls.simple_text_wrap(wrap_length, body)
        print("\n" + pad_char * 3,
              app_name, pad_char * middle, app_name,
              pad_char * 3 + "\n")


def main():
    pass


if __name__ == "__main__":
    main()
