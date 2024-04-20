from pynput import keyboard
from time import sleep
import ntgbtminer


def bytes_to_nibbles(bytes):
    for byte in bytes:
        yield byte >> 4
        yield byte & 0x0f


controller = keyboard.Controller()


def move_page(current_page, target_page, milliseconds=250):
    # The page down key moves one page forwards, and the page up key moves one page backwards.

    offset = target_page - current_page
    if offset == 0:
        # We're already on the right page, so we just need to update the write signal by flicking the page.
        if (target_page == 15):
            controller.tap(keyboard.Key.page_up)
            controller.tap(keyboard.Key.page_down)
        else:
            controller.tap(keyboard.Key.page_down)
            controller.tap(keyboard.Key.page_up)
    elif offset > 0:
        # The target page is further along in the book.
        for i in range(offset):
            controller.tap(keyboard.Key.page_down)
    else:
        # The page offset is negative, so we go backwards.
        for i in range(abs(offset)):
            controller.tap(keyboard.Key.page_up)
    
    sleep(milliseconds / 1000) # The jankest part of all. This lines the inputs up with redstone ticks.
    return target_page


def send_to_book(data: bytes, current_page=1, subtract_mode=True):
    for nibble in bytes_to_nibbles(data):
        if subtract_mode and nibble > 13:
            current_page = move_page(current_page, 15)
            subtract_mode = False
        elif not subtract_mode and nibble < 2:
            current_page = move_page(current_page, 1)
            subtract_mode = True
        if subtract_mode:
            nibble += 1
        current_page =move_page(current_page, nibble)
    return (current_page, subtract_mode)


