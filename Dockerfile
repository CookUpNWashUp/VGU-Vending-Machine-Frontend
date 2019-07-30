FROM arm32v7/python:3.5.7-stretch
RUN mkdir /www
WORKDIR /www
#Install apt requirements
RUN apt update
#RUN apt install -y python3.5 python3.5-dev libmariadbclient-dev
RUN apt install -y libmariadbclient-dev
#Maybe mysql-server is not needed because an instance is included in the stock raspbian. I will try though
RUN apt install -y gcc cmake
RUN apt install -y libusb-dev libpcsclite-dev i2c-tools
#RUN apt install -y rpi.gpio
ENV PYTHONUNBUFFERED 1
#Install python modules and configure defaults
#RUN wget https://bootstrap.pypa.io/get-pip.py
#RUN python3 get-pip.py
COPY requirements.txt /www/
RUN pip3 install -r requirements.txt
#Install nfclib and configure
RUN wget http://dl.bintray.com/nfc-tools/sources/libnfc-1.7.1.tar.bz2
RUN tar -xf libnfc-1.7.1.tar.bz2
WORKDIR /www/libnfc-1.7.1
#RUN cp /www/NFC/nfc-mfultralight.c utils/
COPY NFC/nfc-mfultralight.c utils
RUN ./configure --prefix=/usr --sysconfdir=/www/Frontend
RUN make
RUN make install
#Run the server
WORKDIR /www
COPY . /www
#RUN ["python","manage.py","runserver","0:8000"]
