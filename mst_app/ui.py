import os


COLORS = {
    "reset": "\033[0m",
    "resetcolor": "\033[0m",
    "bold": "\033[1m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
    "bg_black": "\033[40m",
    "bg_red": "\033[41m",
    "bg_green": "\033[42m",
    "bg_yellow": "\033[43m",
    "bg_blue": "\033[44m",
    "bg_magenta": "\033[45m",
    "bg_cyan": "\033[46m",
    "bg_white": "\033[47m",
    "bg_bright_black": "\033[100m",
    "bg_bright_red": "\033[101m",
    "bg_bright_green": "\033[102m",
    "bg_bright_yellow": "\033[103m",
    "bg_bright_blue": "\033[104m",
    "bg_bright_magenta": "\033[105m",
    "bg_bright_cyan": "\033[106m",
    "bg_bright_white": "\033[107m",
}


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def print_error(title, usage=None, examples=None):
    print(f"{COLORS['red']}{title}{COLORS['reset']}")
    if usage:
        print(f"\n{COLORS['bold']}Usage:{COLORS['reset']}\n")
        print(usage)
    if examples:
        print(f"\n{COLORS['bold']}Examples:{COLORS['reset']}\n")
        print(examples)


def print_success(message):
    print(f"{COLORS['green']}{message}{COLORS['reset']}")


def print_warning(message):
    print(f"{COLORS['yellow']}{message}{COLORS['reset']}")


def print_info(message):
    print(f"{COLORS['cyan']}{message}{COLORS['reset']}")


def confirm(prompt_lines, default_yes=False):
    color = COLORS["cyan"] if default_yes else COLORS["yellow"]
    suffix = "[Y/n]" if default_yes else "[y/N]"
    for line in prompt_lines:
        print(line)
    answer = input(f"{color}{suffix}{COLORS['reset']}: ").strip().lower()
    if not answer:
        return default_yes
    return answer in ("y", "yes")

