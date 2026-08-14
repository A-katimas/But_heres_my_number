import os
import sys
import tty
import termios
import select


def cursor(pos: tuple[int, int], text: str) -> str:
    """
    Move the cursor to a specific position and return the formatted string.

    Args:
        pos: A tuple (row, column) representing the cursor position.
        text: The text to display at the given position.

    Returns:
        A string containing ANSI escape codes to position the cursor and
        print the text.
    """
    return f"\033[{pos[0]};{pos[1]}H{text}"


def cursor_hide() -> None:
    """
    Hide the terminal cursor.

    Sends an ANSI escape sequence to make the cursor invisible.
    """
    print("\33[?251", end="")


def cursor_shaw() -> None:
    """
    Show the terminal cursor.

    Sends an ANSI escape sequence to make the cursor visible.
    """
    print("\33[?25h", end="")


def move_cursor_to_bottom() -> None:
    """
    Move the cursor to the bottom line of the terminal.

    Uses the current terminal height to position the cursor on the last row.
    """
    rows = os.get_terminal_size().lines
    print(f"\033[{rows};0H", end="")


def cursor_more_line(pos: tuple[int, int], lines: list[str]) -> str:
    """
    Render multiple lines starting from a given cursor position.

    Each line is printed on a new row, incrementing the vertical position.

    Args:
        pos: Starting position (row, column).
        lines: List of strings to display.

    Returns:
        A single string containing all formatted lines with cursor positioning.
    """
    result = ""
    for i, line in enumerate(lines):
        result += cursor((pos[0] + i, pos[1]), line)
    return result


def clear() -> None:
    """
    Clear the terminal screen and reset the cursor position.

    Sends ANSI escape sequences to clear the screen and move the cursor to
    (0, 0).
    """
    print("\033[2J")
    print("\033[H")


def get_key() -> str:
    """
    Read a single key press from standard input (raw mode).

    Supports special keys such as arrow keys, which emit multi-character
    sequences.

    Returns:
        The key pressed as a string. Special keys may return multiple
        characters.
    """

    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)

    try:
        tty.setraw(fd)
        if not select.select([fd], [], [], 0)[0]:
            return ""
        key = os.read(fd, 1)
        # Special keys (like arrows) send multiple characters
        if key == b"\x1b":
            key += os.read(fd, 2)
        return key.decode()
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
