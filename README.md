
# Components

* bar.py, running on the Raspberry PI; bar.py opens a TCP port
  (configured in net.ini)
* connect.py, connecting to the port opened by bar.py. connect.py tries
  to ensure that a connection to bar.py is always established.

# Setting up the Raspberry PI

* mount the /boot partition of the SD card and create the empty file
  "ssh" in order to enable sshd
* $ sudo aptitude install python3 python3-pip python3-rpi.gpio git
* $ sudo pip3 install rpi\_ws281x
* $ git clone CLONE\_URL $HOME/akk\_status; cd akk\_status # code is
  expected in /home/pi/akk\_status
* $ cp systemd/bar\_panel.service /etc/systemd/system/
* $ cp example\_net.ini net.ini
* Modify net.ini if necessary
* $ sudo systemctl enable bar\_panel.service
* $ sudo reboot

After rebooting, everything should be up and running. The daemon should
be listening in TCP socket 9999.

Tested on Raspbian, version 2017-03-02-raspbian-jessie-lite
