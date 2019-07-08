#!/bin/bash

#I run this in my virtualenv. As such the PATH to python here is not absolute
export DISPLAY=:0
sed -i 's/"exited_cleanly":false/"exited_cleanly":true/' /home/$USER/.config/chromium/Default/Preferences
sed -i 's/"exit_type":"Crashed"/"exit_type":"Normal"/' /home/$USER/.config/chromium/Default/Preferences
# Start the websocket server responsible for the NFC connection
nohup python3 NFC/readNFC.py > /dev/null &
# Start thw webserver
nohup python3 manage.py runserver > /dev/null &
#Start chromium in kiosk mode
/usr/bin/chromium-browser --kiosk http://127.0.0.1:8000/Vendor
