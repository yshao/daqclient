import telnetlib
import time
from common.env import Env
from daqmanager.client.ftpfunc import upload_time, ftp_delete

cfg=Env().getConfig()

# ftp_delete(cfg['encoder_ip'],cfg['praco_username'],cfg['praco_password'])
# ftp_delete(cfg['archival_ip'],cfg['praco_username'],cfg['praco_password'])


t2=telnetlib.Telnet("192.168.38.31",port=23)
newline = "\n"
print t2.read_until("login:")
t2.write("admin"+newline)
print t2.read_until("Password:",3)
t2.write("BEST"+newline)
print t2.read_until(">")
t2.write("cd FlashDisk/Best"+newline)
print t2.read_until("Best")

t3=telnetlib.Telnet("192.168.38.46",port=23)
newline = "\n"
print t3.read_until("login:")
t3.write("admin"+newline)
print t3.read_until("Password:",3)
t3.write("BEST"+newline)
print t3.read_until(">")
t3.write("cd FlashDisk/Best"+newline)
print t3.read_until("Best")

### start motor ###
t2.write("stop_motor"+newline)
print t2.read_until(">",3)

t2.write("stop_motor"+newline)
print t2.read_until(">",3)

t2.write("encoder_home"+newline)
print t2.read_until(">",5)
# time.sleep(10)

t2.write("stop_motor"+newline)
print t2.read_until(">",3)
time.sleep(2)

t2.write("encoder_forward"+newline)
print t2.read_until(">",3)
time.sleep(20)


# t2.write("DAQArchImuS1"+newline)
# print t2.read_until(">",3)
# t3.write("DAQenc_new"+newline)
# print t3.read_until(">",3)


# upload_time(cfg['archival_ip'])
# upload_time(cfg['encoder_ip'])
#
