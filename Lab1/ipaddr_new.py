#!/usr/bin/python
# =============================================================================
#        File : ipaddr_new.py
# Description : Displays IP addr on the Raspberry Pi SenseHat 8x8 LED display
#               e.g. '10.193.72.242'
#      Author : Santhosh shetty
#        Date : 4/2/2017
# =============================================================================

# To use on bootup of :
# sudo nano /etc/rc.local add line: python /home/pi/ipaddr.py &
#

from sense_hat import SenseHat
sense = SenseHat()
sense.set_rotation(180)
sense.show_letter('P')

# give time to get on the Wi-Fi network
# import time
# time.sleep(10)

# get our local IP address. Requires internet access (to talk to gmail.com).
# import socket
# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s.connect(("gmail.com",80))
# addr = s.getsockname()[0]
# s.close()

# ------------------------Without Python packages--------------------------
import socket
import fcntl
import struct

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915, #SIOCGIFADDR
        struct.pack('256s',ifname[:15])
    )[20:24])

ip_addr = get_ip_address('wlan0')
sense.show_message("My IP:")
print ip_addr

#---------------------------------------------------------------------------


# display that address on the sense had
sense.show_message(str(ip_addr))
