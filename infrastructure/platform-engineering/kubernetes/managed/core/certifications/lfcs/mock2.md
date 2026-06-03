sudo -i
======================================
Question 1:
Configure the system to use the following NTP pools:

0.europe.pool.ntp.org
1.europe.pool.ntp.org
Next, change the timezone of this system to Europe, Bucharest.

vi /etc/systemd/timesyncd.conf
[Time]
NTP=0.europe.pool.ntp.org 1.europe.pool.ntp.org

systemctl list-units --type=service --all
systemctl show systemd-timesyncd

systemctl restart systemd-timesyncd
timedatectl set-timezone Europe/Bucharest
timedatectl status

==================================================================================
Question 2:
Add a cron job for the user called john. Don't use the system-wide crontable, but rather add it to the personal crontable of the user called john.

Make sure that this cron job runs every Wednesday at 4AM. The command it should execute is find /home/john/ -type d -empty -delete.

Switch back to the bob user once the task is done.

sudo crontab -u john -e
0 4 * * 3 find /home/john/ -type d -empty -delete

==================================================================================
Question 3:
There is a network interface on this system which has the IP address 10.5.5.2 associated with it. What is the name of this network interface? Create a file in /opt/interface.txt and add a single line to it containing the exact name of that interface.

ip a | grep 10.5.5.2 | awk '{print $5}' > /opt/interface.txt
or
ip -o -4 addr list | grep '10.5.5.2' | awk '{print $2}' | sudo  tee /opt/interface.txt

==================================================================================
Question 4:
An administrator added a new user called jane to this system. But a few mistakes were made. Fix the following problems:

1. The administrator wanted to allow jane to run sudo commands. But instead of adding "jane" to the secondary/supplemental "sudo" group, the administrator changed the primary group to sudo. Fix this by doing the following: Set the primary/login group back to the group called jane. And add the user to the secondary/supplemental group called sudo. In essence the primary group for the user called "jane" should be "jane". And the secondary group should be "sudo".

id jane
usermod -g jane jane
usermod -aG sudo jane
id jane

2. Currently, the home directory path for the jane user is set correctly. But the directory itself is missing. Fix this by creating the /home/jane/ directory. Make sure that the directory is owned by the jane user and jane group.

cat /etc/passwd | grep jane
mkdir -p /home/jane
chown jane:jane /home/jane

3. The default shell for the user called jane is set to /bin/sh. Change the default shell to /bin/bash.

usermod -s /bin/bash jane
cat /etc/passwd | grep jane

4. Finally, set the password for jane to 1234.

echo 'jane:1234' | chpasswd

su - jane
1234
exit

==================================================================================
Question 5:
Perform the following tasks:

1. Set up a port redirection rule that does the following: it redirects any IPv4 packet from the 10.5.5.0/24 CIDR range incoming on port 81 to another machine with the IP address 192.168.5.2 on port 80. To simplify this task, you are not required to specify input or output network interfaces.

iptables -t nat -A PREROUTING -p tcp -s 10.5.5.0/24 --dport 81 -j DNAT --to-destination 192.168.5.2:80

2. Don't forget to add the proper masquerading rule so that packets redirected from 10.5.5.0/24 have a way of getting back to that sender, by our machine sitting in the middle and acting as an ad-hoc router between those two networks.

iptables -t nat -A POSTROUTING -s 10.5.5.0/24 -j MASQUERADE
iptables -t nat -L -n

3. Make sure that after you add the rules you make them persistent (so that when the machine is rebooted these changes are not lost).

apt install iptables-persistent
netfilter-persistent save ou
  iptables-persistent save ou
  iptables-save > /etc/iptables/rules.v4

==================================================================================
Question 6:
In /home/bob/certs/ directory you will find 4 files. That's because we generated two self-signed TLS certificates for you. Delete the 2 files containing the private keys. But preserve the certificate files.

At this point you're left with 2 files containing 2 separate certificates. They both use the RSA algorithm. But one is using 2048 bits for its cryptography purposes, while the other is using 4096. Delete the certificate that is using 2048 bits.

cd /home/bob/certs/
ls -la
cat file*
rm file2 file3

openssl x509 -in file1 -noout -text | grep "Public-Key"
openssl x509 -in file4 -noout -text | grep "Public-Key"
rm file1

==================================================================================
Question 7:
There is a file at /opt/aclfile. Currently no one has permissions to read, write, or execute this file, not even root. But instead of working with regular permissions, use ACL for this task. Add the following to the access control list:

The user called janet should be able to read and write to /opt/aclfile. Just read and write, no execute permission for this ACL entry.

getfacl /opt/aclfile
setfacl -m u:janet:rw /opt/aclfile
getfacl /opt/aclfile

==================================================================================
Question 8:
Add two security limits to the configuration of this system:

1. The user called janet should have a hard`` limit so that she can't open more than100processes.

2. The group called mail should have a soft limit so users in the group not be able to create files larger than 8192 kilobytes.

vi /etc/security/limits.conf
janet hard nproc 100
@mail soft fsize 8192

==================================================================================
Question 9:
In your home directory you will find a subdirectory called project. Navigate to it and then do the following:

1. Add file1 to the staging area to prepare it for a future commit.

cd /home/bob/project
touch file1

2. Commit this file with the exact following message: Created first required file.

git commit -m "Created first required file"

3. Now upload your changes to the remote repository already associated with your local repository. Everything is already set up for you. Use the remote repository aliased as origin and upload the master branch and password to push the code is C0ntr0lplan3Pa$$wd.

git push origin master

==================================================================================
Question 10:
Perform the following tasks related to SELinux on node01:
1. First, check if SELinux is running in enforcing, permissive, or disabled mode. Create the file /opt/selinuxmode.txt. And write your answer to that file. Just one line where you write a single word: enforcing, permissive, or disabled, according to the status you found.

ssh bob@node01
getenforce > /opt/selinuxmode.txt
cat /opt/selinuxmode.txt

2. There is a file that has the wrong SELinux type label. Please correct that and restore the default SELinux label for the file at /usr/bin/less.

restorecon -v /usr/bin/less
exit

==================================================================================
Question 11:
Nginx is installed but it's not running on caleston-lp10. Make the necessary changes so that:

1. Nginx is started immediately.

systemctl status nginx
systemctl start nginx
systemctl status nginx

2. And also, Nginx will start up automatically every time the system boots up.

systemctl enable nginx

3. After starting Nginx, it has spawned at least 3 processes. We are not interested in the master process, only the worker processes. Under what username are these worker processes running? Create a new file at /opt/nginxuser.txt and add a single line to it with that username, other than bob.

ps -ef | grep nginx
echo "www-data" > /opt/nginxuser.txt
echo "root" >> /opt/nginxuser.txt
cat /opt/nginxuser.txt

==================================================================================
Question 12:
A basic LVM structure exists on the node01. Make some changes to it:
1. The volume group called volume1 currently only includes /dev/vdb. Add /dev/vdc to volume1.

ssh bob@node01
vgextend volume1 /dev/vdc
vgdisplay -v volume1

2. We have a logical volume called lv1. Resize this logical volume to 2GB.

lvresize --size 2G /dev/volume1/lv1

==================================================================================
Question 13:
Perform the following tasks on node01:

1. Install Git.

ssh bob@node01
apt install -y git

2. In your home directory, download the entire repository from https://github.com/htop-dev/htop. By default, this action should create a new subdirectory called htop where all the project's files are located.

cd /home/bob
git clone https://github.com/htop-dev/htop
cd htop

3. Switch to the htop subdirectory. Follow the project's instructions to build (compile) the htop application.

cat README.md | grep 'apt install'
apt update
apt install -y libncursesw5-dev autotools-dev autoconf automake build-essential

4. Install the newly built htop application. By default, the application should be installed in /usr/local, in the bin subdirectory

  ./autogen.sh
  ./configure
  make
  make install

==================================================================================
Question 14:
Create a virtual machine with the following parameters on caleston-lp10:

1. For the operating system information parameter use the ubuntu22.04.
2. Name the virtual machine mockexam2.
3. Assign 1024 MB of RAM to this machine.
4. Assign it one virtual CPU.
5. Import the disk image /var/lib/libvirt/images/ubuntu.img to this virtual machine.
6. At the end of your command, you can add the parameter --noautoconsole to avoid waiting for this virtual machine to boot up, and not get stuck in the virtual console after it initializes.

After you create this virtual machine, run a separate command to make mockexam2 automatically start up every time the system boots up.

sudo qemu-img create -f qcow2 /var/lib/libvirt/images/ubuntu.img 10G

virt-install \
--name mockexam2 \
--ram 1024 \
--vcpus=1 \
--os-variant=ubuntu22.04 \
--import \
--disk path=/var/lib/libvirt/images/ubuntu.img \
--noautoconsole

virsh autostart mockexam2

==================================================================================
Question 15:
Create a network bridge between these network interfaces: [ "eth1", and "eth2"] on node01. Call the bridge bridge1. Turn DHCP off for IPv4 for both interfaces. However, for the bridge itself, turn DHCP on for IPv4.

ssh bob@node01
cd /etc/netplan
ls -la
cp 01-netcfg.yaml 99-bridge.yaml
vi /etc/netplan/99-bridge.yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    eth1:
      dhcp4: no
    eth2:
      dhcp4: no
  bridges:
    bridge1:
      dhcp4: yes
      interfaces:
        - eth1
        - eth2

netplan apply

==================================================================================
Question 16:
Perform the following tasks on node01:
1. Remove the Docker image called nginx.

ssh bob@node01
docker rm nginx_container
docker rmi nginx

2. Start a container based on the httpd image. Name it apache_container. Instruct Docker to redirect connections coming to port 80 on the host to port 80 of this container. Also instruct Docker to restart this container only on failure, with a maximum number of retries set to 3 (you will have to look through the correct manual to find the parameter you need).

docker run -d -p 80:80 --name=apache_container --restart=on-failure:3 httpd

==================================================================================
Question 17:
The node01 was configured to use LDAP entries from a certain server. However, some configuration options are wrong. Edit the correct configuration files and fix the following mistakes:

1. Our name service local daemon is configured to look for an LDAP server at the wrong IP address (currently 10.9.9.8). Fix this and configure the correct IP to find it run ip -4 addr show eth0 ignoring /24 . Make sure your changes become active after you edit the configuration file.

ssh bob@node01
vi /etc/nslcd.conf
'''
# The user and group nslcd should run as.
uid nslcd
gid nslcd

# The location at which the LDAP server(s) should be reachable.
uri ldap://192.168.121.167/ # updated it with the output of ``ip -4 addr show eth0`

# The search base that will be used for all queries.
base dc=example,dc=org

# The LDAP protocol version to use.
#ldap_version 3

# The DN to bind with for normal lookups.
#binddn cn=annonymous,dc=example,dc=net
#bindpw secret
'''

2. Our system is currently configured to get group data and password data from the LDAP server but not user data. Configure it to get user data as well.

vi /etc/nsswitch.conf
'''
# /etc/nsswitch.conf
#
# Example configuration of GNU Name Service Switch functionality.
# If you have the `glibc-doc-reference' and `info' packages installed, try:
# `info libc "Name Service Switch"' for information about this file.

passwd:         files systemd ldap #updated
group:          files systemd ldap
shadow:         files ldap
gshadow:        files
'''

systemctl restart nslcd