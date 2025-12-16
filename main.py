import ntgbtminer
from pynput import keyboard, mouse
import data_in
from time import sleep
from config import config
import os
import dotenv
import time

dotenv.load_dotenv()


def player_death_reset():
    kbd = keyboard.Controller()
    mousie = keyboard.Controller()
    kbd.tap(keyboard.Key.tab)
    time.sleep(0.5)
    kbd.tap(keyboard.Key.enter)
    time.sleep(3)
    mousie.click(mouse.Button.right) # Open the book


def start_mining():

    test = config['use_test_header']
    
    if not test:
        block_template = ntgbtminer.get_block_template(config['coinbase_message'], config['address'])
    while config['loop_attempts']:
        if test:
            header = bytes.fromhex(config['test_header'])
        else:
            header = ntgbtminer.block_make_header(block_template)

        
        # Pad the header according to the SHA-256 spec:
        #   0x80 at the start, and the length of the message at the end
        header += b'\x80' + b'\x00' * 45 + bytes.fromhex('0280')
        
        # Send the first chunk
        print('Sending the first chunk...')
        data_in.send_to_book(header[:64], milliseconds=220) 
        

        # Wait for the first chunk to be done
        print(f'Waiting for the first chunk to finish hashing ({config['seconds_between_chunks']} seconds)...')
        sleep(config['seconds_between_chunks'])

        # Send the second chunk
        print('Sending the second chunk...')
        data_in.send_to_book(header[64:], milliseconds=220) # Second chunk

        print('All the data is in the game. Checking for death message...')
        message = poll_log()

        if message.find(config['dog_name']) >= 0:
            print('Success!')
            if not test:
                # Send off the block to the network
                submission = ntgbtminer.block_make_submit(block_template)
                ntgbtminer.rpc_submitblock(submission)
        else:
            print('Better luck next time!')
            
        if test:
            return
        else:
            block_template['nonce'] += 1


def on_press(key: keyboard.KeyCode): 
    if key == keyboard.KeyCode.from_char(config['start_key']):
        return False


def check_death_message(file_path: str):

    # Only check the file if it was updated in the last 5 seconds
    if time.time() - os.path.getmtime(file_path) > 5:
        return ''
    with open(file_path, 'rb') as file:
        line = None
        
        # Read backwards until we find a newline character
        file.seek(0, 2)
        while file.tell() > 0:
            file.seek(-2, 1)
            if file.read(1) == b'\n':
                line = file.readline().decode()
                break
        
        # In case the file only contains one line
        if line is None:
            line = file.readline().decode()
        
        if line.find('died') >= 0:
            return line


def poll_log():
    while True:
        if message := check_death_message(os.environ.get('LOG_PATH')):
            return message
        time.sleep(config['log_poll_interval'])


def main():
    print(f'Press {config['start_key']} to start the miner...')
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
    start_mining()
    
if __name__ == '__main__':
    main()