from pynput import keyboard, mouse
from win_precise_time import sleep
from config import config

def bytes_to_nibbles(bytes: bytes):
    """
    Generate the high and low nibbles of each byte 
    """
    for byte in bytes:
        yield byte >> 4
        yield byte & 0x0f


kbd = keyboard.Controller()
mousie = mouse.Controller()

def move_page(current_page: int, target_page: int, milliseconds=250):
    """
    Move to a particular page in the book.
    """
    # The page down key moves one page forwards, and the page up key moves one page backwards.

    offset = target_page - current_page
    if offset == 0:
        # We're already on the right page, so we just need to update the write signal by flicking the page.
        if (target_page == 15):
            kbd.tap(keyboard.Key.page_up)
            kbd.tap(keyboard.Key.page_down)
        else:
            kbd.tap(keyboard.Key.page_down)
            kbd.tap(keyboard.Key.page_up)
    elif offset > 0:
        # The target page is further along in the book.
        for _ in range(offset):
            kbd.tap(keyboard.Key.page_down)
    else:
        # The page offset is negative, so we go backwards.
        for _ in range(abs(offset)):
            kbd.tap(keyboard.Key.page_up)
    
    sleep(milliseconds / 1000) # The jankest part of all. This lines the inputs up with redstone ticks.
    return target_page


def send_to_book(data: bytes, current_page=1, subtract_mode=True, milliseconds=250, replace_book=True) -> tuple[int]:
    """
    Convert a list of bytes into a page sequence, and execute that page sequence in Minecraft.
    """
    for nibble in bytes_to_nibbles(data):
        if subtract_mode and nibble > 13:
            current_page = move_page(current_page, 15, milliseconds=milliseconds)
            subtract_mode = False
        elif not subtract_mode and nibble < 2:
            current_page = move_page(current_page, 1, milliseconds=milliseconds)
            subtract_mode = True
        if subtract_mode:
            nibble += 1
        current_page = move_page(current_page, nibble, milliseconds=milliseconds)
    
    # Replace the book
    if replace_book:
        kbd.tap(keyboard.Key.enter) # Take the book off the lectern
        sleep(0.2)
        mousie.click(mouse.Button.right) # Place the book back on the lectern
        sleep(0.2)
        mousie.click(mouse.Button.right) # Open the book
        sleep(0.2)

        # Select the "take book" button
        kbd.tap(keyboard.Key.tab)
        kbd.tap(keyboard.Key.tab)
        sleep(0.2)
    
    return (current_page, subtract_mode)


