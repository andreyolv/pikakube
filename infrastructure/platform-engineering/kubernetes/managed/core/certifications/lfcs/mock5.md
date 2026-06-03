Q1:
1. Get the kernel name of linux

uname -s

2. Get the value of kernel parameter ip_forward

sysctl net.ipv4.ip_forward

3. Get the system timezone

cat /etc/timezone
or
timedatectl | grep "Time zone"

==================================================================================
Q2:
migrate a cronjob belongs to user 'user1' in /etc/crontab to user1's crontab that we can list it by cmd 'crontab -l'
create a new cronjob to exec file clean.sh by 'user1' every Monday and Thurday at 11:15 am

cat /etc/crontab
crontab -e -u user1

==================================================================================
Q3:
Config the NTP servers to 0.pool.ntp.org and 1.pool.ntp.org
Config the fallback NTP servers to ntp.ubuntu.com and 0.debian.pool.ntp.org
Set maxium pool interval to 1000s and connection retry to 20s

vi /etc/systemd/timesyncd.conf
'''
[Time]
NTP=0.pool.ntp.org 1.pool.ntp.org
FallbackNTP=ntp.ubuntu.com 0.debian.pool.ntp.org
PollIntervalMaxSec=1000
PollIntervalMinSec=20
'''
systemctl restart systemd-timesyncd
timedatectl status

==================================================================================
Q4:
1. add new variable VAR1=random-string into the .bashrc file

echo 'export VAR1=random-string' >> ~/.bashrc
source ~/.bashrc

2. create a new script script.sh with following vars:
VAR2 contains 'v2'
VAR3 contains VAR1-extended, which is available in the script and all sub-processes
print VAR3

vi script.sh
'''
#!/bin/bash

VAR2="v2"
export VAR3="${VAR1}-extended"

echo "$VAR3"
'''
chmod +x script.sh

==================================================================================
Q5:
There is a file import01.tar.bz2, we have to create a new compress gz file named as import01.tar.gz
write all file names and sort all files inside to 2 coresponding files 'import01.tar.bz2_list' and 'import01.tar.gz_list'


==================================================================================
Q6:
1. change group of user1 to dev and change home dir to /home/user1

sudo usermod -g dev -d /home/user1 -m user1

2. add user2 with group 'dev' and 'op', home dir to /home/user2 and default terminal is /bin/bash

sudo useradd -m -d /home/user2 -s /bin/bash -G dev,op user2

3. configure to allow user2 can run file 'dangerous.sh' without entering root password

sudo visudo
user2 ALL=(ALL) NOPASSWD: /usr/local/bin/dangerous.sh

==================================================================================
Q7:
1. Close port 5000

sudo iptables -A INPUT -p tcp --dport 5000 -j DROP

2. Redirect all traffic from port 6000 to 6001

sudo iptables -t nat -A PREROUTING -p tcp --dport 6000 -j REDIRECT --to-port 6001

3. Only allow IP 192.168.1.1 to access the port 6002

# Primeiro, permitir o IP desejado
sudo iptables -A INPUT -p tcp -s 192.168.1.1 --dport 6002 -j ACCEPT
# Depois, bloquear todos os outros
sudo iptables -A INPUT -p tcp --dport 6002 -j DROP

4. Block all traffic to 192.168.1.2

sudo iptables -A OUTPUT -d 192.168.1.2 -j DROP
sudo iptables -A INPUT -s 192.168.1.2 -j DROP

apt install iptables-persistent
netfilter-persistent save

==================================================================================
Q8:
Format the /dev/vdb to ext4, mount to /mnt/backup
Find the fullest of disk /dev/vdc and /dev/vdd, and remove all files inside the .trash folder
between 2 processes 'matter1' and 'mater2', find the one is consumming more RAM, then unmount the disk where it's excuting

==================================================================================
Q9:
At dir /opt/
Delete all files created before 01-09-2024
Move all files smaller than 3kb to /opt/3kb/
Move all files larger than 10kb to /opt/10kb/
Move all files have permission 777 to /opt/777/
A:
Backup the dir /opt/

==================================================================================
Q10:
Mount dir /data-export from server1 to /opt/server1/data-export in server 'master' by using SSHFS with format 'read-only' and enable option 'allow_other'
Mount the NFS dir /nfs/share in server 'master' to /opt/nfs/ dir in 'server1'


==================================================================================
Q11:
Stop container 'fe_v1'
Collect and write all info about 'fe_v1' to /opt/info:
- assigned ip address
- volume mount destination dir
Start a new container with name 'fe_v3' from image 'nginx:alpine' with limited ram is 30m and expose to port 1234 from port 80 inside the container

==================================================================================
Q12:
Clone a repo /repository/project1 to /home/user1/project1
Check file 'config.yaml' inside 3 branchs 'dev1' 'dev2' 'dev3', which one does contain 'user_level' inside? Then merge the branch to 'main'
Create new dir 'logs' and 'logs/.keep' file into the 'main' branch, then commit all things with msg 'added new log dir'

==================================================================================
Q13:
There are 3 processes named 'process1' 'process2' and 'process3'. Currently the server has an system security alert. Let find where the alert came from in these 3 processes and stop it by using cmd 'kill'. 
Notice: use 'strace -p PID' 

==================================================================================
Q14:
run the file /opt/generate.sh many times with following below requirements:
- redirect stdout to /var/1.out
- redirect stderr to /var/2.out
- redirect both stdout and stderr to /var/3.out
- write the exit code number to /var/4.out

==================================================================================
Q15:
install the terminal browser from source located in /opt/links2/, with configuring the location to /usr/bin/links2, turn off the ipv6 support

==================================================================================
Q16:
server1 has 2 apps, which are opening 2 port 1111 and 2222 and using nginx as webservers.
Try to create a LoadBalanacer on that server which:
- Listens on port 8001 and forward/redirect traffics to server1:2222/special
- Listens on port 8000 and balances traffic between server1:1111 and server1:2222 by using Random or Round Robin

==================================================================================
Q17:
Disable the X11Forwarding of OpenSSH in server1
Disable PasswordAuthentication for everyone except user1
Enable Banner with file /etc/ssh/sshd-banner for user user1 and user2

==================================================================================
Q18:
Remove the disk /dev/vdh from vg vol1
Create a new vg vol2 from disk /dev/vdh
Create 50M lv named pv1 for vg vol2
format the pv1 with ext4

==================================================================================
Q19:
Find all log lines in /var/nginx/nginx.log where URLs start with /app/user and were accessed by browser identity 'bot/1.2', write all them into /opt/log-collection.extracted
Find and replace all lines starting with 'container.web', end with '24h' and have word 'Running' anywhere in-between with 'SENSITIVE LINE REMOVE' in file /var/ngin/server.log

==================================================================================
Q20:
Find the soft limit we added for user 'jackier' for number of processes need to be run in .bashrc file, then set it as a hard limit 
Enforce the group 'operations' can only ever log in once at the same time

vi /etc/security/limits.conf
'''
jackier   soft    nproc   4096
jackier   hard    nproc   4096
@operations   hard   maxlogins   1
'''
