nohup python3 manage.py runserver 0:8000 > /dev/null &
nohup python3 NFC/readNFC.py > /dev/null &
echo "Server running..."
while true; do
	sleep 3
	echo "Doing it.."
done
