# Minecraft Bitcoin Miner

## Script Install

* Install Python

* Clone or download this repository, and open a shell in the downloaded folder

```powershell
git clone https://github.com/soundtomb/minecraft-bitcoin-miner.git
cd minecraft-bitcoin-miner
```

* Install the libraries. I recommend that you [create a virtual environment](https://docs.python.org/3/library/venv.html) first, so that there are no conflicts. You can install everything you need by running this command

```powershell
pip install -r requirements.txt
```

* Create a file named `.env`. Configure your credentials in `.env`. This should contain these secrets:
  * `RPC_URL` The URL of your bitcoin node server
  * `RPC_USER` The bitcoin node server's username
  * `RPC_PASS` The bitcoin node server's password
  * `SCREENSHOTS_PATH` The path to your minecraft screenshots folder
  * `LOG_PATH` The path to your world's chat logs
  
```sh
RPC_URL=http://localhost:8332
RPC_USER=your_username
RPC_PASS=your_password
SCREENSHOTS_PATH=/Path/To/Minecraft/Screenshots/Folder
SCREENSHOTS_PATH=/Path/To/Minecraft/logs/latest.log
```

* Run the script with

```sh
python main.py
```

## Configuration

This is done from `config.json`.

## License

ntgbtminer is MIT licensed. See the provided [`LICENSE`](LICENSE) file.
