import grp
import os
import pwd
import sys
import termios
import time
import tty
import uinput

def drop_privileges(uid_name='nobody', gid_name='nogroup'):
    if os.getuid() != 0:
        return

    running_uid = pwd.getpwnam(uid_name).pw_uid
    running_gid = grp.getgrnam(gid_name).gr_gid

    os.setgroups([])
    os.setgid(running_gid)
    os.setuid(running_uid)
    os.umask(0o77)

# Key mapping and events
key_mapping = {
    'a': uinput.KEY_A,
    'b': uinput.KEY_B,
    'c': uinput.KEY_C,
    'd': uinput.KEY_D,
    'e': uinput.KEY_E,
    'f': uinput.KEY_F,
    'g': uinput.KEY_G,
    'h': uinput.KEY_H,
    'i': uinput.KEY_I,
    'j': uinput.KEY_J,
    'k': uinput.KEY_K,
    'l': uinput.KEY_L,
    'm': uinput.KEY_M,
    'n': uinput.KEY_N,
    'o': uinput.KEY_O,
    'p': uinput.KEY_P,
    'q': uinput.KEY_Q,
    'r': uinput.KEY_R,
    's': uinput.KEY_S,
    't': uinput.KEY_T,
    'u': uinput.KEY_U,
    'v': uinput.KEY_V,
    'w': uinput.KEY_W,
    'x': uinput.KEY_X,
    'y': uinput.KEY_Y,
    'z': uinput.KEY_Z,
    '\n': uinput.KEY_ENTER, # maybe this should be ctrl+j?
    '\r': uinput.KEY_ENTER,
    ' ': uinput.KEY_SPACE,
    '\x7f': uinput.KEY_BACKSPACE,
    '0': uinput.KEY_0,
    '1': uinput.KEY_1,
    '2': uinput.KEY_2,
    '3': uinput.KEY_3,
    '4': uinput.KEY_4,
    '5': uinput.KEY_5,
    '6': uinput.KEY_6,
    '7': uinput.KEY_7,
    '8': uinput.KEY_8,
    '9': uinput.KEY_9,
    '$': uinput.KEY_DOLLAR,
    ';': uinput.KEY_SEMICOLON,
    '.': uinput.KEY_DOT,
    '[': uinput.KEY_LEFTBRACE,
    ']': uinput.KEY_RIGHTBRACE,
    '(': uinput.KEY_KPLEFTPAREN,
    ')': uinput.KEY_KPRIGHTPAREN,
    'LSHIFT': uinput.KEY_LEFTSHIFT,
    '\t': uinput.KEY_TAB,
    '-': uinput.KEY_MINUS,
    '=': uinput.KEY_EQUAL,
    '\x1b': uinput.KEY_ESC,
    ',': uinput.KEY_COMMA,
    '/': uinput.KEY_SLASH,
    '\\': uinput.KEY_BACKSLASH,
    '\'': uinput.KEY_APOSTROPHE,
    '\x1b[A': uinput.KEY_UP,
    '\x1b[B': uinput.KEY_DOWN,
    '\x1b[C': uinput.KEY_RIGHT,
    '\x1b[D': uinput.KEY_LEFT,
    'KEY_LEFTALT': uinput.KEY_LEFTALT,
}

def get_key():
    """Get a single key press, including full ANSI escape sequences."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        if ch == '\x1b':
            ch += sys.stdin.read(1)
            if ch[1] == '[':
                while True:
                    ch += sys.stdin.read(1)
                    if ch[-1] in 'ABCD~':
                        break
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def remap(key, device):
    """Takes in an unknown event and tries to translate into known event and emit combo."""
    shiftmaps = {
        '!': '1',
        '@': '2',
        '#': '3',
        '$': '4',
        '%': '5',
        '^': '6',
        '&': '7',
        '*': '8',
        ',': '(',
        '.': ')',
        '{': '[',
        '}': ']',
        '_': '-',
        '<': ',',
        '>': '.',
        '?': '/',
        '|': '\\',
        '+': '=',
        '"': '\'',
        ':': ';',
    }

    if key.lower() in key_mapping:
        device.emit_combo([uinput.KEY_LEFTSHIFT, key_mapping[key.lower()]])
    elif key in shiftmaps:
        device.emit_combo([uinput.KEY_LEFTSHIFT, key_mapping[shiftmaps[key]]])
    elif key.startswith("\x1b[1;"):
        # determine if shift, alt, shift+alt, or ctrl+alt event
        SHIFT     = "2"
        ALT       = "3"
        SHIFT_ALT = "4"
        CTRL_ALT  = "7"
        no_prefix = key.split("\x1b[1;", 1)[1]
        command, rest_of_string = no_prefix[0], no_prefix[1:]
        reconstituted = "\x1b[" + rest_of_string

        if command == SHIFT:
            device.emit_combo([uinput.KEY_LEFTSHIFT, key_mapping[reconstituted]])
        elif command == ALT:
            print("ALT not supported yet")
        elif command == SHIFT_ALT:
            print("SHIFT_ALT not supported yet")
        elif command == CTRL_ALT:
            print("CTRL_ALT not supported yet")
        else:
            # device.emit_combo([uinput.KEY_LEFTALT, key_mapping[reconstituted]])
            print("TODO:", command, "rest", rest_of_string)
    else:
        print("WELP", repr(key))

def main():
    print("BEGIN")
    uinput_fd = uinput.fdopen()
    drop_privileges()
    print("DROPPED PRIVILEGES")


    with uinput.Device(key_mapping.values(), fd=uinput_fd) as device:
        time.sleep(1)  # Gives time for the device to fully register
        print("READY!")
        try:
            while True:
                key = get_key()
                if key == '\x03':  # Ctrl+C
                    break
                if key in key_mapping:
                    print(f"Sending key: {repr(key)}, {repr(key_mapping[key])}")  # Debugging output
                    device.emit_click(key_mapping[key])
                else:
                    remap(key, device)
        except KeyboardInterrupt:
            print("Exiting...")

if __name__ == "__main__":
    main()
