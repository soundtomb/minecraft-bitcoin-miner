def gen_nibbles(b: bytes):
    for byte in b:
        yield byte >> 4
        yield byte & 0x0f

data = bytes.fromhex('aab3147124d95a5430c31b18fe9f0864800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000280')
page_sequence = ''
subtract_mode = True
for nibble in gen_nibbles(data):
    if subtract_mode and nibble > 13:
        page_sequence += 'f'
        subtract_mode = False
    elif not subtract_mode and nibble < 2:
        page_sequence += '1'
        subtract_mode = True
    if subtract_mode:
        nibble += 1
    page_sequence += '{:x}'.format(nibble)

with open(r'C:\Users\rhysl\Documents\Code\minecraft_bitcoin\minecraft_bitcoin_miner\data_in\page_sequence.txt', 'w') as f:
    f.write(page_sequence)