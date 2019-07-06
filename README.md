# Vending Machine Frontend

Code run on the Raspberry Pi, run on a Django + MariaDB stack. The idea is to run the application on Chromium kiosk mode. Thus this will be a pleb web applicaion

## Installation
1. Install virtualenv and set up a new environment. Google how.
1. ```pip3 install django RPi.GPIO gpiozero mysqlserver websockets```
1. Start a new project. The project name I chose is called Frontend. 
1. ```git clone https://github.com/CookUpNWashUp/VGU-Vending-Machine-Frontend.git```
1. Install and install libnfc. This website relies on the ```nfc-mfultralight```tool, look it up on Google.
1. Setup your PN352 with any configuration on the Rasp Pi. I used the SPI config.
1. Run the websocket server in the NFC dir. I tested the page on a remote host instead of local so there might be potential problems. Switch up the settings.py if you have to.
1. Add things, break things, have fun

## Changelog
- [x] Client side DB structure
- [x] Server side dummy API
- [x] One single view rules all
- [x] GPIO control added
- [x] Javascript keyboard
- [x] Add css + js. Split up view if necessary
- [x] NFC websocket server
- [x] Websocket dialog box for 2FA token
- [ ] Add backend - frontend database replication
- [ ] Adjust admin rights
- [ ] Add startup shell script
- [ ] Add install script
- [ ] Clean up code
