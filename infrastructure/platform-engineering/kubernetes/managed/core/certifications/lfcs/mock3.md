sudo -i
======================================
Question 1:
Nginx is installed and a configuration file for running Nginx as a reverse proxy is already available. Perform the following tasks:

1. Disable the default Nginx website configuration.

cd /etc/nginx
ls -la
ls -la sites-enabled
rm /etc/nginx/sites-enabled/default

2. Find the correct file where the reverse proxy configuration for Nginx is defined. Edit this file and make it redirect requests to "google.com".

vi /etc/nginx/sites-available/proxy.conf
'''
server {
    listen 80;
    location / {
        proxy_pass http://google.com;
        include proxy_params;
    }
}
'''

3. Make Nginx use this configuration file so that it starts working as a reverse proxy.

ln -s /etc/nginx/sites-available/proxy.conf /etc/nginx/sites-enabled/proxy.conf
ls -la sites-enabled
systemctl reload nginx
systemctl status nginx

==================================================================================
Question 2:
Add a cron job to the system-wide cron table. This cron job should run as a user called Mary, on the 15th day of every month, at 4 AM*. The command that the cron job should execute is: find /home/mary/ -type d -empty -delete.

vi /etc/crontab
0 4 15 * * mary find /home/mary/ -type d -empty -delete

==================================================================================
Question 3:
Make some changes to the network configuration settings of the interface called enp0s10 using netplan.
1. First, make a persistent change to the correct configuration file. There are two routes defined for our network interface. Remove the route that sends network packets to 192.168.1.0/24 through the server at 10.198.0.2. Make sure that your changes are applied.

cd /etc/netplan
cat *.yaml

vi /etc/netplan/extrainterface.yaml 
'''
network:
  version: 2
  ethernets:
    enp0s10:
      dhcp4: false
      dhcp6: false
      addresses:
        - 10.198.0.5/24
      routes:
        - to: 192.168.0.0/24
          via: 10.198.0.1
'''

netplan apply
ip route show

2. Next, add a temporary IP address to our interface. Assign it the following IP: 10.5.0.9/24. No configuration files should be edited for this second task.

ip addr add 10.5.0.9/24 dev enp0s10

==================================================================================
Question 4:
Change the following kernel parameters:

1. Set vm.swappiness to 30. Make this a non-persistent change that will be lost at the next reboot.
sysctl -a | grep swappiness
sysctl vm.swappiness=30
sysctl -a | grep swappiness

2. Set vm.dirty_ratio to 15. Make this a persistent change so that it survives across reboots.

vi /etc/sysctl.conf
vm.dirty_ratio = 15

==================================================================================
Question 5:
Perform the following tasks:

1. Add a group called developers.

groupadd developers

2. Add a user called jane. When creating the account, go with the system defaults. That is, the user's home directory should be set to /home/jane, and the default shell should be /bin/bash. You can pick any password you want for this user.

useradd jane -m -s /bin/bash
echo 'jane:1234' | chpasswd

3. After the user jane was created, perform the following changes. Set her primary/login group to developers. And set her secondary groups to jane and 

usermod -g developers jane
usermod -aG jane,jane
id jane

==================================================================================
Question 6:
Edit the configuration of the SSH daemon. Disable password logins globally (for all users). But make an exception for a single user. The user called "john" should be allowed to log in with a password.

Don't apply changes now.

Note: There's also a setting related to "Keyboard Interactive Authentication" that can in some cases affect password authentication settings. But you can ignore that setting for the purposes of this task.

vi /etc/ssh/sshd_config
PasswordAuthentication no
Match User john
    PasswordAuthentication yes

==================================================================================
Question 7:
A large file in the /usr directory is no longer required. Find the file larger than 1 GB and delete it.

find /usr -type f -size +1G -exec rm {} \;

==================================================================================
Question 8:
We've provided two storage devices that can be accessed at /dev/vdb and /dev/vdc. 

1. Add these as physical volumes to LVM, then set up a volume group that includes both devices. Call this volume group VG1 (uppercase letters).

pvcreate /dev/vdb /dev/vdc
pvs
vgcreate VG1 /dev/vdb /dev/vdc
vgdisplay -v VG1

2. On this volume group, add a logical volume of exactly 6 GB. Call this logical volume LV1 (uppercase letters).

lvcreate -L 6G -n LV1 VG1
lvs

==================================================================================
Question 9:
Set up iptables rules that will redirect all incoming network connections from "10.11.12.0/24" to "10.9.9.1". Remember the matching masquerade rule (so traffic can be returned to 10.11.12.0/24).

iptables -t nat -A PREROUTING -s 10.11.12.0/24 -p tcp -j DNAT --to-destination 10.9.9.1
iptables -t nat -A POSTROUTING -s 10.11.12.0/24 -j MASQUERADE
iptables -t nat -L -n

==================================================================================
Question 10:
Use the kode_web directory to build a Docker image. Fix any errors if necessary. Call your image kodekloud/nginx_kodekloud:1.0. Run a Docker container based on this image, call the container kodekloud_webserv and redirect any connections incoming to port 81 on the host to port 80 of the container.

ssh bob@node01
cd kode_web
vi Dockerfile (fix COPi do COPY)
docker build --tag kodekloud/nginx_kodekloud:1.0 /home/bob/kode_web
docker run -d -p 81:80 --name kodekloud_webserv kodekloud/nginx_kodekloud:1.0
exit

==================================================================================
Question 11:
You will find a subdirectory called kode. This is a local Git repository. And it's already configured with a remote repository aliased as origin. Perform the following tasks:

1. Pull in the latest commits from this origin remote repository, from the master branch.

cd ~/kode
git pull origin master

2. You should now see a file called file1. Edit this file and add another line to it. Write this text on the second line: "line2". Save the file.

vi file1
# Add "line2" on the second line, save, and exit.

3. Stage and commit your latest changes to file1. Add the following message to this commit: "Added line2 to our project".

git add file1
git commit -m "Added line2 to our project"

4. Push your local Git repository to the remote repository aliased as "origin", into the "master" branch.

git push origin master

==================================================================================
Question 12:
Format /dev/vdd with the ext4 filesystem. Then set up the system to automatically mount /dev/vdd into the /home/bob/backups directory every time it boots up.

mkfs.ext4 /dev/vdd
lsblk -f

vi /etc/fstab
/dev/vdd /home/bob/backups ext4 defaults 0 2
mount -a
mkdir /home/bob/backups
mount -a
lsblk

==================================================================================
Question 13:
A process (mockexam.sh) is overusing system resources on node01. Identify the process consuming the most system resources.

1. Kill the process

ssh bob@node01
ps aux | grep mockexam
kill -9 9757
ps aux | grep mockexam

2. Delete the script which is the source for that process.

rm /home/bob/test/mockexam.sh
exit

==================================================================================
Question 14:
Find all files in the /opt/files/ directory that are larger than 500 megabytes and delete them.

find /opt/files -type f -size +500M -exec rm -f {} +

==================================================================================
Question 15:
A process is overusing CPU resources. Find the most CPU-intensive process and close it.

ps aux
kill -9 10709

==================================================================================
Question 16:
This system currently has no way of synchronizing its time with NTP servers. Install the timesyncd utility belonging to the systemd suite of software. Then configure it to synchronize with the following NTP pools:

0.asia.pool.ntp.org
1.asia.pool.ntp.org
2.asia.pool.ntp.org
3.asia.pool.ntp.org

Make sure these settings are applied.

apt install systemd-timesyncd

vi /etc/systemd/timesyncd.conf
NTP=0.asia.pool.ntp.org 1.asia.pool.ntp.org 2.asia.pool.ntp.org 3.asia.pool.ntp.org

systemctl restart systemd-timesyncd
timedatectl status

==================================================================================
Question 17:
We have a Network Block Device (NBD) server running at the IP address 127.0.0.1. Perform the following tasks:

1. A network block device is already attached to this system and mounted to a certain directory. Unmount the network block device from that directory. Then disconnect the network block device from the system.

ssh bob@node01
lsblk
umount /share
nbd-client -d /dev/nbd0

2. List the exports available on the NBD server at 127.0.0.1. Attach the second export to this system, and then mount it to the /mnt directory.

nbd-client -l 127.0.0.1
nbd-client 127.0.0.1 -N disk2
mount /dev/nbd0 /mnt
