import os
import telnetlib
import time
from common.env import Env
from common.utils import get_timestamp
from daqmanager.client.ftpfunc import upload_time, ftp_delete, touch
import shutil



### clear data folder ###
try:
    shutil.rmtree('data')
except:
    pass


cfg=Env().getConfig()

ftp_delete(cfg['encoder_ip'],cfg['praco_username'],cfg['praco_password'])
ftp_delete(cfg['archival_ip'],cfg['praco_username'],cfg['praco_password'])


t2=telnetlib.Telnet(cfg['archival_ip'],port=23)
newline = "\n"
print t2.read_until("login:")
t2.write("admin"+newline)
print t2.read_until("Password:",3)
t2.write("BEST"+newline)
print t2.read_until(">")
t2.write("cd FlashDisk/Best"+newline)
print t2.read_until("Best")

t3=telnetlib.Telnet(cfg['encoder_ip'],port=23)
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

t2.write("stop_motor"+newline)
print t2.read_until(">",3)
time.sleep(2)

t2.write("encoder_forward"+newline)
print t2.read_until(">",3)
# time.sleep(20)


t2.write("DAQArchImuS1"+newline)
print t2.read_until(">",3)
t3.write("DAQenc_new"+newline)
print t3.read_until(">",3)


tm=get_timestamp()
tm=tm.replace('-','_')
touch(tm)
upload_time(cfg['archival_ip'],tm)
upload_time(cfg['encoder_ip'],tm)
time.sleep(5)
os.move(tm,temp)

