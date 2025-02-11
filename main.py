import ntgbtminer
from pynput import keyboard
import data_in
from time import sleep
from config import config
import asyncio
import watchfiles
import os
import dotenv
import time



TEST_HEADER = bytes.fromhex('02000000b6ff0b1b1680a2862a30ca44d346d9e8910d334beb48ca0c00000000000000009d10aa52ee949386ca9385695f04ede270dda20810decd12bc9b048aaab3147124d95a5430c31b18fe9f0864')
REAL_TEST_HEADER = bytes.fromhex('0100000081cd02ab7e569e8bcd9317e2fe99f2de44d49ab2b8851ba4a308000000000000e320b6c2fffc8d750423db8b1eb942ae710e951ed797f7affc8892b0f1fc122bc7f5d74df2b9441a42a14695')
dotenv.load_dotenv()

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
    sleep(config['seconds_between_chunks'])

    # Send the second chunk\
    data_in.send_to_book(header[64:], milliseconds=220) # Second chunk


def on_press(key: keyboard.KeyCode):    
    if key == keyboard.KeyCode.from_char(config['start_key']):
        start_mining()

def check_dog_death(file_path):
    if time.time() - os.path.getmtime(file_path) > 5:
        return False
    with open(file_path, 'rb') as file:
        # Move the pointer to the end of the file
        file.seek(0, 2)
        line = None
        # Read backwards until we find a newline character
        while file.tell() > 0:
            file.seek(-2, 1)
            if file.read(1) == b'\n':
                line = file.readline().decode()
                break
        # In case the file only contains one line
        if line is None:
            line = file.readline().decode()
        print(line)
        return line.find('Kevin') >= 0

async def poll_log():
    while True:
        if check_dog_death(os.environ.get('LOG_PATH')):
            print('mined!')
            break
        await asyncio.sleep(config['log_poll_interval'])


async def main():
    # print(f'Press {config['start_key']} to start the miner...')
    # with keyboard.Listener(on_press=on_press) as listener:
    #     listener.join()

    
        
    await poll_log()
    
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('stopped via KeyboardInterrupt')