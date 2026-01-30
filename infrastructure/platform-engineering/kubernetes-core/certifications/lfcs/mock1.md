sudo -i
======================================
Question 1:
In the /opt/findme/ directory you will find 10,000 files. You need to filter out specific files

1. Find all files that have the executable permission bit enabled for the user that owns them. Redirect the output of the find command to the /opt/foundthem.txt file.

find /opt/findme/ -type f -perm -u=x > /opt/foundthem.txt
or
find /opt/findme/ -type f -perm /u=x  | tee /opt/foundthem.txt

2. Find all files that have the SETUID permission enabled and delete them.

find /opt/findme/ -type f -perm -4000 -exec rm -f {} +
or
find /opt/findme/ -type f -perm -4000 | xargs rm -f
or
find /opt/findme/ -type f -perm /u=s -exec rm {} \;
or
find /opt/findme/ -perm /4000 -exec rm -f {} \;
or
find /opt/findme/ -perm /4000 -exec rm -f {} +

3. Find any file that is larger than 1KB and copy it to the /opt/ directory

find /opt/findme/ -type f -size +1k -exec cp {} /opt/ \;
or
find /opt/findme/ -type f -size +1k | xargs cp -t /opt/

==================================================================================
Question 2:
Perform the following two tasks:

1. Create a bash script that recursively copies the /var/www/ directory into the /opt/www-backup/ directory
Save your script at /opt/script.sh. Remember, the script file you create also has to be executable.

vi /opt/script.sh
'''
#!/bin/bash
mkdir -p /opt/www-backup/
cp -a /var/www/. /opt/www-backup/
'''
mkdir (-p, --parents no error if existing, make parent directories as needed)
cp (-a, --archive, more complete than -r, --recursive, -a preserve all caracteristics)

chmod +x /opt/script.sh

2. Make sure that your script /opt/script.sh automatically runs every day at 4AM. More specifically, create a cron job that runs that script every day at 4AM. Put this in the system-wide cron table (not root's local cron table) and make sure the script executes under the root user.

crontab -e -> current user crontab
/etc/crontab -> system-wide crontab

vi /etc/crontab
0 4 * * * root /opt/script.sh

==================================================================================
Question 3:
Enforce some limits on two users:

1. Set a limit on the user called john so that he can open no more than 30 processes. This should be a hard limit.
2. For the user called jane make sure she can create files not larger than 1024 kilobytes. Make this a soft limit.

vi /etc/security/limits.conf
john hard nproc 30
jane soft fsize 1024

grep '^john:' /etc/passwd -> nologin so we can not change user with command su - john to test with ulimit -a
sudo -u john bash -c "ulimit -a | grep processes"
sudo -u jane bash -c "ulimit -a | grep 'file size'"
ou 
su - john -c "ulimit -a"

==================================================================================
Question 4:
Create a new user on this system called mary

Set her password to 1234.
Leave the full name and other personal details empty.
Set her default shell to /bin/dash.
Make sure she can execute sudo commands by adding her to the secondary group called sudo.
At this point Mary's primary group is mary. And her secondary group is sudo. Change her primary group to developers. Without affecting her secondary group.

useradd -m -s /bin/dash mary
echo "mary:1234" | sudo chpasswd

usermod -aG sudo mary
usermod -g developers mary
id mary
groups mary

==================================================================================
Question 5:
Modify the following kernel runtime parameter:

vm.swappiness set it to a value of 10. This should be a persistent change, added to a file so that vm.swappiness is set to 10 every time the system boots up. However, after you create the proper file, also set this runtime parameter to 10 for this session as well. Otherwise said, the file will set the parameter to 10 the next time the system boots up, but we want to set it to 10 even for this current, active session, instead of waiting until the next boot until that takes effect.

sysctl -a
sysctl vm.swappiness=10
echo "vm.swappiness=10" >> /etc/sysctl.d/99-swappiness.conf
or
echo "vm.swappiness=10" | sudo tee /etc/sysctl.d/99-swappiness.conf

==================================================================================
Question 6:
You have an xfs filesystem on /dev/vdb1. Also, there's an ext4 filesystem on /dev/vdb2.

1. Edit the correct file in /etc/ so that /dev/vdb1 is automatically mounted into the /backups directory every time the system boots up. Default mount options should be used.

lsblk
vi /etc/fstab
/dev/vdb1    /backups    xfs    defaults    0    2

2. /dev/vdb2 is already mounted in /mnt/. But there is a problem. Sensitive data exists on this ext4 filesystem and you want to make sure that it's not accidentally modified. To solve this problem, remount /dev/vdb2 into the /mnt directory, but this time, with the read-only mount option. It does not matter what the other mount options are. Just make sure this mount point is read-only so that users cannot change contents on this filesystem.

mount -o remount,ro /dev/vdb2 /mnt

==================================================================================
Question 7:
Use the Logical Volume Manager to perform the following tasks:

1. Add /dev/vdc and /dev/vdd as Physical Volumes to LVM.

pvcreate /dev/vdc /dev/vdd
pvs

2. Create a Volume Group on these two physical volumes. Call the volume volume1.

vgcreate volume1 /dev/vdc /dev/vdd
vgs

3. On the Volume Group called volume1 create a new Logical Volume. Call this Logical Volume website_files. Set the size of the Logical Volume to 3GB.

lvcreate -n website_files -L 3G volume1
lvs

==================================================================================
Question 8:
In your home directory you will find a subdirectory called kode. Git tools are pre-installed. Switch to the kode subdirectory and perform the following tasks:

1. Initialize this subdirectory as an empty Git repository.

cd /home/bob/kode
git init

2. Associate this local Git repository with the remote repository found at https://github.com/kodekloudhub/git-for-beginners-course.git. Add this as a remote repository and call it (alias it as) origin.

git remote add origin https://github.com/kodekloudhub/git-for-beginners-course.git

3. Download all the latest changes from the master branch from that remote repository into your local repository.

git pull origin master

==================================================================================
Question 9:
A Docker container is running on node01.
Perform the following tasks:

1. Stop and remove the container that is currently running, since it's not configured correctly.

ssh bob@node01
docker ps -a
docker stop webserver1
docker rm webserver1
docker ps -a

2. In your home directory you will find a subdirectory called kode_web. It contains all the necessary build instructions for Docker. Use that directory to build a new Docker image. Call this image kodekloudwebserv.

cd /home/bob/kode_web
docker build -t kodekloudwebserv .

3. Finally, launch a container based on the kodekloudwebserv image. In your command, make sure that all connections incoming to port 8081 on the host are redirected to port 80 of the container. Call this container webserver2.

docker run -d -p 8081:80 --name webserver2 kodekloudwebserv
docker ps -a
exit

==================================================================================
Question 10:
NFS server and client tools are installed on caleston-lp10 system. Instruct the NFS server to share the /home directory in read-only mode with IP addresses in the 10.0.0.0/24 CIDR range.

vi /etc/exports
/home 10.0.0.0/24(ro)

exportfs -ra

==================================================================================
Question 11:
Find the application that is accepting incoming connections on port 80. Make note of the exact name of that application. You will need it later on.

As you investigated what application is accepting incoming connections to port 80, you might have noticed that two or more PIDs are associated with that. Basically, the application has forked multiple processes to do its job. Figure out which PID is associated with the master process.

With both of these things noted, create the following file: /opt/process.txt.

On the first line add the name of the application associated with port 80, in all lowercase letters.
On the second line add the PID number associated with the master process.

lsof -i :80
echo "nginx" > /opt/process.txt
pgrep -a nginx
echo "8240" >> /opt/process.txt
cat /opt/process.txt

==================================================================================
Question 12:
Explore your network settings and perform the following tasks:

1. There is currently one network interface which does not have any IPv4 address associated with it. Temporarily assign it the following IPv4 address: 10.5.0.1/24. This should not be a permanent change (no need to edit configuration files).

ip addr
ip addr add 10.5.0.1/24 dev eth1
ip addr

2. What is the default route for this system? Create a file, and add a single line where you save the IP address for the gateway used by this default route (i.e., requests are routed to what IP address?). Save the address in this file: /opt/gateway.txt.

ip route show default | awk '{print $3}' | tee /opt/gateway.txt
cat /opt/gateway.txt

3. For the final task, find out what is the IP address of the main DNS resolver configured for this system. Create the file /opt/dns.txt and add a single line to it with that IP address.

grep ^nameserver /etc/resolv.conf | awk '{print $2}' > /opt/dns.txt

==================================================================================
Question 13:
There is a another virtual machine with name node01 is available for you. Perform this task on node01. You can access the node by ssh

You can identify the disk because it is currently unpartitioned, not mounted anywhere, and is 2 GB in size.
Disk /dev/vdb is unpartitioned, not mounted anywhere, and is 2 GB in size.

1. Create two partitions of equal size on this disk: 500M each. Ignore about remaining 1GB partition.

ssh bob@node01

lsblk

sudo fdisk /dev/vdb
n - new
p - primary
enter - default
enter - default
+500M
n - new
p - primary
enter - default
enter - default
+500M
w - write

lsblk

2. Create an ext4 filesystem on the first partition.
Create an xfs filesystem on the second partition.

sudo mkfs.ext4 /dev/vdb1
sudo mkfs.xfs /dev/vdb2
lsblk -f

3. Create two directories: /part1 and /part2.
Manually mount the ext4 filesystem in the /part1 directory. Manually mount the xfs filesystem in the /part2 directory.

sudo mkdir /part1
sudo mkdir /part2
sudo mount /dev/vdb1 /part1
sudo mount /dev/vdb2 /part2
df -h

4. Also, configure the system to automatically mount these the same way, every time the operating system boots up.
sudo vi /etc/fstab
/dev/vdb1    /part1    ext4    defaults    0    2
/dev/vdb2    /part2    xfs    defaults    0    2

sudo umount /part1 /part2
df -h
sudo mount -a
df -h
exit

==================================================================================
Question 14:
Configure the system to use /swfile as a swap file on node01.

1. First, create /swfile. Make the size of this file exactly 1024 MB.

ssh bob@node01
sudo fallocate -l 1024M /swfile

2. Then take all the necessary steps to temporarily mount this as swap. (So that it's immediately used as swap for this current boot session).

chmod 600 /swfile
mkswap /swfile
swapon /swfile
swapon --show
free -h

3. But also make sure to configure the system to also use this as swap every time it will boot up in the future.

vi /etc/fstab
/swfile none swap sw 0 0

==================================================================================
Question 15:
On node01 two processes are overusing our storage device. One is executing a lot of I/O operations per second (small data transfers, but a very large number of such transfers). Otherwise said, the process has a high tps/IOPS. The other process is reading very large volumes of data.

1. Identify the process with the high tps. What partition is it using? Create the file /opt/devname.txt and write the device name of that partition inside that file. For example, if it's using /dev/vde5, you would simply write /dev/vde5 on a single line in that file. Note that there might be some abstractions behind this, and we're not interested in device mapper names, but rather, the real device the mapper is using.

ssh bob@node01
sudo -i
dstat --top-io --top-bio
pgrep python3
lsof -p 10057
lsof -p 10057 | awk '{print $9}' | while read file; do df $file; done
echo "/dev/vda1" > /opt/devname.txt

2. Identify the process with the high read transfer rate/second. Create the file /opt/highread.pid and write the PID number of that process in that file. For example, if the PID is 3886 you just write 3886 in that file (only the number, on a single line).

sudo pidstat -d 1
echo "10479" > /opt/highread.pid

==================================================================================
Question 16:
On node01 list all filesystems to check out how much free space they have remaining. You'll find one which is almost full (should be around 98% full). To confirm it is the correct filesystem, see where it is mounted, and you should find many directories on it in the form of numbers from 1 to 999. Find the directory which has the largest file and delete that file (only that file, nothing else).

ssh bob@node01
df -h
ls -la /data

find /data -type f -exec du -h {} + | sort | tail -1
rm -rf /data/683/lf
or
find /data -type f -exec du -h {} + | sort | tail -1 | awk '{print $2}' | xargs rm
exit 

==================================================================================
Question 17:
On caleston-lp10 change the configuration for the SSH daemon. Disable X11 forwarding globally. Then, make an exception for just one user called bob. For that user alone enable X11 forwarding.

Do not restart the SSH service after making the changes.

vi /etc/ssh/sshd_config
/X11
X11Forwarding no

Match User bob
        X11Forwarding yes