import curses
import time
import random


def text_generator():
    text = [
        "La velocidad es crucial.",
        "Escribe rapido y con precision.",
        "10 palabras solamente para aprender a escribir y analizar ok.",
    ]
    return random.choice(text)


def main(stdscr):
    exit = ""
    while exit != "q":
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_CYAN, -1)
        curses.init_pair(2, curses.COLOR_RED, -1)
        curses.init_pair(3, curses.COLOR_BLACK, -1)
        curses.init_pair(4, curses.COLOR_WHITE, -1)

        def get_x(text: str, i: int = -1, full_text: str = ""):
            if i != -1:
                x = ((width - len(full_text)) // 2) + i
            else:
                x = (width - len(text)) // 2
            return [
                x,
                text,
            ]

        text = text_generator()
        words = len(text.split(" "))
        counter = 0
        current_word = 0
        y = height // 2 - 2
        stdscr.addstr(y, *get_x(f"{counter}/{words}"))
        stdscr.addstr(y + 1, *get_x(text.replace(" ", "•")))
        stdscr.refresh()

        begin = time.time()
        input = ""
        while True:
            if len(input) == len(text):
                break

            c = stdscr.getch()
            if c == ord("\n"):
                break
            elif c == ord("\b") or c == 263:
                input = input[:-1]
            else:
                input += chr(c)
            # Verificar si se completó una palabra
            words_input = input.split(" ")
            words_target = text.split(" ")

            if len(words_input) > len(words_target):
                words_input = words_target

            # Aumentar contador solo si la palabra está completa y coincide
            if input == " ".join(words_target[: current_word + 1]):
                if current_word < len(words_target):
                    current_word += 1
                    counter = current_word
                    stdscr.addstr(y, *get_x(f"{counter}/{words}"))
                stdscr.addstr(y, *get_x(f"{counter}/{words}"))

            stdscr.addstr(y, *get_x(f"{counter}/{words}"))
            for i, char in enumerate(text):
                color = curses.color_pair(3)
                inp = list(input)
                for j, char_input in enumerate(inp):
                    if j == i:
                        if char_input == char:
                            color = curses.color_pair(1)
                        else:
                            color = curses.color_pair(2)
                        break
                    else:
                        color = curses.color_pair(4)
                if char == " ":
                    char = "•"

                stdscr.addstr(y + 1, *get_x(char, i, text), color)
                stdscr.refresh()

        finish = time.time()
        times = finish - begin

        if input == text:
            speed = len(text.split(" ")) / times * 60
            stdscr.addstr(
                y + 3,
                *get_x(f"velocidad: {speed:.2f} wpm"),
            )
        else:
            stdscr.addstr(y + 3, *get_x("Texto incorrecto."))

        exit = chr(stdscr.getch())


curses.wrapper(main)
