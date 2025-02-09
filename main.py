import ntgbtminer
from pynput import keyboard
import data_in
from time import sleep

TEST_HEADER = bytes.fromhex('02000000b6ff0b1b1680a2862a30ca44d346d9e8910d334beb48ca0c00000000000000009d10aa52ee949386ca9385695f04ede270dda20810decd12bc9b048aaab3147124d95a5430c31b18fe9f0864')
REAL_TEST_HEADER = bytes.fromhex('0100000081cd02ab7e569e8bcd9317e2fe99f2de44d49ab2b8851ba4a308000000000000e320b6c2fffc8d750423db8b1eb942ae710e951ed797f7affc8892b0f1fc122bc7f5d74df2b9441a42a14695')


def start_mining():
    # coinbase_message = "This task's a gruelling one. Hope to find some diamonds tonight-night-night. Diamonds tonight!"
    # header = ntgbtminer.get_header_bytes(coinbase_message, 'bc1q27geatqpasc3rdjdnmwgxyyzvyykdae867npjt')


    # Pad the header according to the SHA-256 spec:
    #   0x80 at the start, and the length of the message at the end
    header = TEST_HEADER

    header += b'\x80' + b'\x00' * 45 + bytes.fromhex('0280')
    
    # Send the first chunk
    data_in.send_to_book(header[:64], milliseconds=220) 
    

    # Wait for the first chunk to be done
    sleep(10)

    # Send the second chunk\
    data_in.send_to_book(header[64:], milliseconds=220) # Second chunk


def on_press(key: keyboard.KeyCode):    
    if key == keyboard.KeyCode.from_char('`'):
        start_mining()


if __name__ == '__main__':
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()