#!/usr/bin/env bash

echo "========== Setup Wireless Scale Display =========="
sudo apt-get update

# Setup WiFi AP
cur_dir="$( cd "$(dirname "$0")" ; pwd -P )"
cd ${cur_dir}/scripts
sudo bash rpi3_ap_setup.sh

echo "Install Kivy now..."
sudo apt-get install -y python libpython-dev python-pip
sudo apt-get install -y libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev pkg-config libgl1-mesa-dev
sudo apt-get install -y libgles2-mesa-dev python-setuptools libgstreamer1.0-dev git-core gstreamer1.0-plugins-bad
sudo apt-get install -y gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-ugly gstreamer1.0-omx
sudo apt-get install -y gstreamer1.0-alsa python-dev libmtdev-dev xclip

sudo pip install -U pip
sudo pip install Cython==0.25.2

sudo pip install git+https://github.com/kivy/kivy.git@master

# install Adafruit
git clone https://github.com/adafruit/Adafruit_Python_ADS1x15.git
cd Adafruit_Python_ADS1x15
sudo python setup.py install

sudo apt-get install -y python-smbus i2c-tools
sudo pip install adafruit-ads1x15
sudo i2cdetect -y 1

# Install mosquitto MQTT broker.
sudo pip install paho-mqtt
sudo apt-get install -y mosquitto mosquitto-clients python-scipy python-numpy

sudo pip install pymongo xlsxwriter

# Enable SSH
sudo touch /boot/ssh

cd /tmp
git clone https://github.com/doceme/py-spidev
cd py-spidev
sudo python setup.py install

cd ${cur_dir}
echo "Configuring the 7inch touchscreen from Waveshare..."
echo "max_usb_current=1" | sudo tee -a /boot/config.txt
echo "hdmi_group=2" | sudo tee -a /boot/config.txt
echo "hdmi_mode=87" | sudo tee -a /boot/config.txt
echo "hdmi_cvt 1024 600 60 6 0 0 0" | sudo tee -a /boot/config.txt
echo "hdmi_drive=1" | sudo tee -a /boot/config.txt
cd /tmp
wget https://www.waveshare.com/w/upload/3/34/LCD-show-180331.tar.gz
tar zxvf LCD-show-180331.tar.gz
cd LCD-show
sudo rm -r rpi-fbcp/build
mkdir rpi-fbcp/build
sed -i -- "s/sudo cp -rf .\/etc\/rc.local/# sudo cp -rf .\/etc\/rc.local/" LCD7-1024x600-show
sed -i -- "s/sudo reboot/# sudo reboot/" LCD7-1024x600-show
sed -i -- "s/sudo apt-get install xserver-xorg-input-evdev/sudo apt-get install -y xserver-xorg-input-evdev/" LCD7-1024x600-show
chmod +x LCD7-1024x600-show
./LCD7-1024x600-show

# Increase GPU memory size
echo "gpu_mem=512" | sudo tee -a /boot/config.txt

# Enable SPI interface
echo "dtparam=spi=on" | sudo tee -a /boot/config.txt

echo "Disabling the booting logo..."
echo "disable_splash=1" | sudo tee -a /boot/config.txt
sudo sed -i -- "s/$/ logo.nologo quiet loglevel=3 vt.global_cursor_default=0 systemd.show_status=0 plymouth.ignore-serial-consoles plymouth.enable=0/" /boot/cmdline.txt
sudo sed -i -- "s/console=tty1/console=tty3/" /boot/cmdline.txt

bash ${cur_dir}/scripts/install_custom_splash_screen.sh
sudo bash ${cur_dir}/scripts/install_mongodb.sh

# Disable the blinking cursor
sudo sed -i -- "s/^exit 0/TERM=linux setterm -foreground black >\/dev\/tty0\\nexit 0/g" /etc/rc.local
sudo sed -i -- "s/^exit 0/TERM=linux setterm -clear all >\/dev\/tty0\\nexit 0/g" /etc/rc.local

# Disable some servics to reduce booting time
sudo systemctl disable hciuart
sudo mkdir /etc/systemd/system/networking.service.d
sudo touch /etc/systemd/system/networking.service.d/reduce-timeout.conf
echo "[Service]" | sudo tee -a /etc/systemd/system/networking.service.d/reduce-timeout.conf
echo "TimeoutStartSec=1" | sudo tee -a /etc/systemd/system/networking.service.d/reduce-timeout.conf
sudo rm /etc/systemd/system/dhcpcd.service.d/wait.conf

# Enable auto start
sudo apt-get install screen

sudo sed -i -- "s/^exit 0/screen -mS h -d\\nexit 0/g" /etc/rc.local
sudo sed -i -- "s/^exit 0/screen -S h -X stuff \"hostapd \/etc\/hostapd\/hostapd.conf\\\\r\"\\nexit 0/g" /etc/rc.local

sudo sed -i -- "s/^exit 0/screen -mS wsd -d\\nexit 0/g" /etc/rc.local
sudo sed -i -- "s/^exit 0/screen -S wsd -X stuff \"cd \/home\/pi\/WirelessScaleDisplay\/display\\\\r\"\\nexit 0/g" /etc/rc.local
sudo sed -i -- "s/^exit 0/screen -S wsd -X stuff \"python main.py\\\\r\"\\nexit 0/g" /etc/rc.local

echo "===== Cythoning Now ====="
cd ${cur_dir}
python compile.py build_ext --inplace

echo "========== Finished Installation, now rebooting... =========="
sudo reboot
