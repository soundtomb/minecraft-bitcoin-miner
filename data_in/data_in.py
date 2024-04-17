from pyautogui import press, click, keyDown, keyUp
from time import sleep
from keyboard import wait, add_hotkey


HOTKEY = '`'

chunk = b'\x49\xc1\x80\xfa'
nibbles = []


def bytes_to_nibbles(bytes):
    for byte in bytes:
        yield byte >> 4
        yield byte & 0x0f

def string_to_nibbles(hex_string):
    for char in hex_string:
        yield int(char, base=16)

page_number = 1
def write_nibble(value):
    global page_number

    # If we want to write a 0, we have to take the book of the lectern
    if value == 0:
        # Move the page to update the write signal
        if page_number == 15:
            press('pageup')
        else:
            press('pagedown')
        
        # Take the book off the lectern
        press('enter')
        sleep(0.1)

        # Place the book back on the lectern and edit the book
        click(2, button='right')
        sleep(0.1)

        # Navigate to the "Take Book" button
        press('tab', presses=2)
        page_number = 1

        # Extra sleep for precision
        sleep(0.05)
        return
    
    offset = value - page_number
    page_number = value
    if offset == 0:
        # Already on the right page, so we just need to update the write signal
        # by flipping the page forward and backward (or backward and forward it it's page 15)
        if value == 15:
            press('pageup')
            press('pagedown')
        else:
            press('pagedown')
            press('pageup')
    
    # Navigate to the right page
    elif offset > 0:
        press('pagedown', presses=offset)
    else:
        press('pageup', presses=-offset)
    sleep(0.2)


def key_sequence():
    with open(r'C:\Users\rhysl\Documents\Code\minecraft_bitcoin\minecraft_bitcoin_miner\data_in\page_sequence.txt') as f:
        # for nibble in string_to_nibbles(f.read()):
        keyDown('alt')
        keyDown('pagedown')

add_hotkey(HOTKEY, key_sequence)
wait()