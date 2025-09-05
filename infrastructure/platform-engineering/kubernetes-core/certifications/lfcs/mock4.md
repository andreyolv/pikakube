sudo -i
======================================
Question 1:
A process mockexam.sh is running under the user account called bob. Find and terminate that process.

ps -u bob
ps aux | grep mockexam
kill -9 2618
or
pgrep -u bob
or
pkill -u bob -f mockexam.sh

==================================================================================
Question 2:
Nginx is installed and a configuration file is available to make it work as a load balancer. However, some steps are still required:

1. Edit the provided configuration file and add another server for load balancing.

vi /etc/nginx/sites-available/loadbalancer.conf
    
2. The server's IP is 10.9.0.3. Assign it a weight equal to 3 so that requests are sent to this server more often.

upstream backend {
    server 10.9.0.3 weight=3;
}

3. Take the rest of the steps necessary to make this new configuration active for Nginx.

nginx -t
sudo ln -s /etc/nginx/sites-available/loadbalancer.conf /etc/nginx/sites-enabled/loadbalancer.conf
sudo systemctl reload nginx

==================================================================================
Question 3:
A user called jane exists on this system. Make the following changes:

1. Change the default shell of this user to /bin/bash.

usermod -s /bin/bash jane
or
chsh -s /bin/bash jane

2. Add the user to an additional secondary group called sudo. Make sure to preserve the secondary groups jane is already part of.

sudo usermod -aG sudo jane

==================================================================================
Question 4:
Add a cron job to the crontable of the user called john (not the system-wide crontable).

1. This cron job should be executed every Monday and Saturday at 3 AM (03:00).
2. The command executed by this cron job should be:
tar acf /home/john/www-snapshot.tgz /var/nginx
Important note: The crontable entry should be specified on a single line (not one line for Monday and a separate one for Friday).

crontab -e -u john
0 3 * * 1,6 tar acf /home/john/www-snapshot.tgz /var/nginx

==================================================================================
Question 5:
We've created a configuration file that defines a network bond between two interfaces. But we haven't activated it yet.

1. Change that configuration file to make eth3 the primary interface of this network bond.

vi /etc/netplan/99-bond.yaml
primary: eth3

2. Activate the new network settings defined in that file, so that the network bond gets created accordingly.

netplan apply

==================================================================================
Question 6:
Perform the following tasks:

1. Set up a port redirection rule. All connections coming from the 10.9.9.0/24 IP range, on port 8080 should be redirected to 10.100.0.8 on port 80.

sudo iptables -t nat -A PREROUTING -s 10.9.9.0/24 -p tcp --dport 8080 -j DNAT --to-destination 10.100.0.8:80

2. Make sure to also set up masquerading so that traffic can also be returned to the sender (10.9.9.0/24).

sudo iptables -t nat -A POSTROUTING -s 10.9.9.0/24 -j MASQUERADE

==================================================================================
Question 7:
The systemd-timesyncd package is already installed. However, automatically setting up the correct time by using NTP servers is currently disabled.

1. Enable NTP time synchronization on this machine.

sudo timedatectl set-ntp true

2. Then set the timezone to Asia, Singapore.

sudo timedatectl set-timezone Asia/Singapore

3. Finally, Determine the name of the fallback NTP pool currently configured for this system. Extract only the name of the pool (e.g., "example.ubuntu.com") and create the file /opt/pool.txt containing that name on a single line.

sudo timedatectl show-timesync | grep FallbackNTP > /opt/pool.txt

==================================================================================
Question 8:
In your home directory, you will find a subdirectory called project1. Inside, a local Git repository was already set up, initialised, and associated with a remote repository aliased as "origin".

1. Stage and commit all files in the project1 repository.

cd ~/project1
git add *

2. Use the commit message: Initial commit of project1.

git commit -m "Initial commit of project1"

3. Push your changes to the master branch of the remote repository.

git push origin master

==================================================================================
Question 9:
In your /home/bob/certs directory, you will find six files. Three private keys and three TLS certificates that are associated with those keys. However, two certificates have incorrect data.

1. Look for the certificate generated for kodekloud.com. Keep that certificate and its associated key.

cd /home/bob/certs
openssl x509 -in third.crt -text -noout | grep kodekloud.com

2. Delete the two certificates that aren't associated with kodekloud.com. Also, delete their corresponding keys.

sudo rm first.key first.crt second.key second.crt

3. At the end of this task, you should be left with two files: the certificate for "kodekloud.com" and its associated key.

==================================================================================
Question 10:
The Logical Volume Manager was used to create the following structure:

A volume group called VG1.
A logical volume called LV1.
On this logical volume we have an ext4 filesystem of approximately 2GB.
Expand the logical volume called LV1 to use 100% of the free space available on the VG1 volume group.

sudo lvresize --extents 100%VG VG1/LV1

==================================================================================
Question 11:
We have a Docker container on this system(node01) that is currently stopped. Find that container and delete it.

ssh bob@node01
docker ps --all
docker rm container1

==================================================================================
Question 12:
Create an ext4 filesystem on /dev/vdc. Then configure the system to automatically mount this new filesystem in the /home/bob/share directory every time it boots up.

ssh bob@node01
mkfs.ext4 /dev/vdc
vim /etc/fstab
/dev/vdc /home/bob/share ext4 defaults 0 2
mount -a

==================================================================================
Question 13:
Configure the system to automatically adjust the value of a certain kernel parameter every time it boots up.
net.ipv6.conf.all.forwarding should be set to 1 at each boot.

ssh bob@node01
vim /etc/sysctl.conf
net.ipv6.conf.all.forwarding = 1
sysctl --system

==================================================================================
Question 14:
The /var/www/ directory and all of its content is currently labeled like this under SELinux:
unconfined_u:object_r:var_t:s0
Change the label on the /var/www/ directory itself, its subdirectories, and all the files it contains.
More specifically, change the SELinux type on these objects to httpd_sys_content_t.
At the end of this task, everything in /var/www/ (and the directory itself) should end up with the following label:
unconfined_u:object_r:httpd_sys_content_t:s0

chcon -R -t httpd_sys_content_t /var/www
ls -Z /var/www

extra:
Show all user label of SELinux:
# seinfo -u
Role label:
# seinfo -r
Type label:
# seinfo -t

Change SELinux context for a certain files, ex: to httpd_sys_content_t
Change Type:
# chcon -t [typename] [file]
Change User:
# chcon -u [username] [file]
Change Role:
# chcon -r [role] file]
Ex:
# chcon -t httpd_sys_content_t [file]
==================================================================================
Question 15:
In the /opt/archive/ directory there is a single file with the permission to be executed by its user. Find the user's executable file and delete it.

find /opt/archive/ -type f -perm /u=x
rm /opt/archive/file43492

==================================================================================
Question 16:
Find the filesystem that is almost full (100% of available space is used, or very close to 100%). Free up some space by deleting the largest file from that filesystem.

df -h
find /mnt -type f -exec ls -s {} + | sort -n -r | head -1 | awk '{print $2}' | xargs sudo rm -f

==================================================================================
Question 17:
Swap is currently used on this system. Disable (turn off) only swap with name additionalspace.

swapoff /additionalspace
