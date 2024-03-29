# 2023/10/25

Following Danny Saba's instructions for mounting the nfs share from sdsc rds osdf origin server. Start by checking OS version again, then installing NFS client (and tools) on the nsgosg host.

```
[mkandes@nsgosg ~]$ cat /etc/os-release 
NAME="Rocky Linux"
VERSION="8.8 (Green Obsidian)"
ID="rocky"
ID_LIKE="rhel centos fedora"
VERSION_ID="8.8"
PLATFORM_ID="platform:el8"
PRETTY_NAME="Rocky Linux 8.8 (Green Obsidian)"
ANSI_COLOR="0;32"
LOGO="fedora-logo-icon"
CPE_NAME="cpe:/o:rocky:rocky:8:GA"
HOME_URL="https://rockylinux.org/"
BUG_REPORT_URL="https://bugs.rockylinux.org/"
SUPPORT_END="2029-05-31"
ROCKY_SUPPORT_PRODUCT="Rocky-Linux-8"
ROCKY_SUPPORT_PRODUCT_VERSION="8.8"
REDHAT_SUPPORT_PRODUCT="Rocky Linux"
REDHAT_SUPPORT_PRODUCT_VERSION="8.8"
[mkandes@nsgosg ~]$ sudo dnf install nfs-utils
[sudo] password for mkandes: 
Duo two-factor login for mkandes

Enter a passcode or select one of the following options:

 1. Duo Push to XXX-XXX-7242
 2. SMS passcodes to XXX-XXX-7242

Passcode or option (1-2): 1

Please open Duo Mobile and check for Duo Push requests manually.
Success. Logging you in...
Last metadata expiration check: 0:50:09 ago on Wed 25 Oct 2023 02:33:07 PM PDT.
Package nfs-utils-1:2.3.3-59.el8.x86_64 is already installed.
Dependencies resolved.
Nothing to do.
Complete!
[mkandes@nsgosg ~]$
```

Creating mount point, and mounting filesystem.

```
[mkandes@nsgosg ~]$ ls -lahtr /mnt/
total 0
drwxr-xr-x.  2 root root   6 Oct 10  2021 .
dr-xr-xr-x. 20 root root 288 Dec 21  2021 ..
[mkandes@nsgosg ~]$ sudo mkdir /mnt/osdf
[mkandes@nsgosg ~]$ ls -lahtr /mnt/
total 0
dr-xr-xr-x. 20 root root 288 Dec 21  2021 ..
drwxr-xr-x.  2 root root   6 Oct 25 15:24 osdf
drwxr-xr-x.  3 root root  18 Oct 25 15:24 .
[mkandes@nsgosg ~]$ sudo vi /etc/fstab
[mkandes@nsgosg ~]$ cat /etc/fstab

#
# /etc/fstab
# Created by anaconda on Tue Feb  4 16:07:51 2020
#
# Accessible filesystems, by reference, are maintained under '/dev/disk/'.
# See man pages fstab(5), findfs(8), mount(8) and/or blkid(8) for more info.
#
# After editing this file, run 'systemctl daemon-reload' to update systemd
# units generated from this file.
#
/dev/mapper/cl-root     /                       xfs     defaults        0 0
UUID=7fe9ccef-56e7-40ac-8d95-49cd05e728ac /boot                   ext4    defaults        1 2
UUID=D237-8078          /boot/efi               vfat    umask=0077,shortname=winnt 0 2
/dev/mapper/cl-home     /home                   xfs     defaults        0 0
/dev/mapper/cl-swap     swap                    swap    defaults        0 0

cavern3.sdsc.edu:/users/u3/sivagnan /users/u3/sivagnan nfs rw,nfsvers=3,proto=tcp,bg,intr,nodev,nosuid,noacl 0 0
cavern3.sdsc.edu:/users/u4/kenneth /users/u4/kenneth nfs rw,nfsvers=3,proto=tcp,bg,intr,nodev,nosuid,noacl 0 0
cavern3.sdsc.edu:/users/u4/nsgdevuser /users/u4/nsgdevuser nfs rw,nfsvers=3,proto=tcp,bg,intr,nodev,nosuid,noacl 0 0
cavern3.sdsc.edu:/users/u4/nsgproduser /users/u4/nsgproduser nfs rw,nfsvers=3,proto=tcp,bg,intr,nodev,nosuid,noacl 0 0
cavern3.sdsc.edu:/users/u2/majumdar /users/u2/majumdar nfs rw,nfsvers=3,proto=tcp,bg,intr,nodev,nosuid,noacl 0 0
cavern3.sdsc.edu:/users/u3/mkandes /users/u3/mkandes nfs rw,nfsvers=3,proto=tcp,bg,intr,nodev,nosuid,noacl 0 0
qs-nsg:/nsg     /projects/ps-nsg        nfs rw,nfsvers=3,proto=tcp,bg,intr,nodev,nosuid,noacl 0 0

qs-nsg.sdsc.edu:/nsg-osdf   /mnt/osdf       nfs     hard,tcp,nosuid,nodev,auto,nofail   0      0
[mkandes@nsgosg ~]$ sudo mount /mnt/osdf
mount: (hint) your fstab has been modified, but systemd still uses
       the old version; use 'systemctl daemon-reload' to reload.
[mkandes@nsgosg ~]$ sudo systemctl daemon-reload
[mkandes@nsgosg ~]$ ls -lahtr /nsg-osdf
ls: cannot access '/nsg-osdf': No such file or directory
[mkandes@nsgosg ~]$ df -h
Filesystem                              Size  Used Avail Use% Mounted on
devtmpfs                                1.8G     0  1.8G   0% /dev
tmpfs                                   1.8G     0  1.8G   0% /dev/shm
tmpfs                                   1.8G  176M  1.7G  10% /run
tmpfs                                   1.8G     0  1.8G   0% /sys/fs/cgroup
/dev/mapper/cl-root                      50G  4.7G   46G  10% /
/dev/sda2                               974M  287M  621M  32% /boot
/dev/sda1                               599M  5.8M  594M   1% /boot/efi
/dev/mapper/cl-home                      47G  511M   46G   2% /home
cavern3.sdsc.edu:/users/u4/nsgdevuser   454G  430G   25G  95% /users/u4/nsgdevuser
cavern3.sdsc.edu:/users/u3/sivagnan     454G  430G   25G  95% /users/u3/sivagnan
qs-nsg:/nsg                              91T   47T   45T  51% /projects/ps-nsg
cavern3.sdsc.edu:/users/u3/mkandes      454G  430G   25G  95% /users/u3/mkandes
cavern3.sdsc.edu:/users/u4/kenneth      454G  430G   25G  95% /users/u4/kenneth
cavern3.sdsc.edu:/users/u4/nsgproduser  454G  430G   25G  95% /users/u4/nsgproduser
cavern3.sdsc.edu:/users/u2/majumdar     454G  430G   25G  95% /users/u2/majumdar
tmpfs                                   364M     0  364M   0% /run/user/28563
tmpfs                                   364M     0  364M   0% /run/user/501506
qs-nsg.sdsc.edu:/nsg-osdf                91T   47T   45T  51% /mnt/osdf
[mkandes@nsgosg ~]$
```

Okay! Looks good.

```
[mkandes@nsgosg ~]$ sudo ls -lahtr /mnt/osdf/NSG/PUBLIC
total 16K
drwxr-xr-x. 4 xrootd 986 1.0K Jun  9 11:37 ..
-rw-r--r--. 1 xrootd 986   39 Jun  9 11:41 test-file.txt
drwxr-xr-x. 2 xrootd 986 1.0K Jun  9 14:21 .
-rw-r--r--. 1 xrootd 986   39 Jun  9 14:21 test-file-nsg.txt
[mkandes@nsgosg ~]$
```

Let's try staging in the ILSVRC2012 dataset ...

# 2023/10/30

I was unable to stage in the data last week due to permissions issues on the newly mounted `/mnt/osdf/NSG/PUBLIC` directory from the origin. To get around this issue, I'll try and create a new group with GID 986 and then add myself to the group. Please note, however, for whatever reason, this GID 986 does not appear to be the default GID for xrootd.

```
[mkandes@nsgosg ~]$ cat /etc/passwd | grep xrootd
xrootd:x:990:296:XRootD runtime user:/var/spool/xrootd:/sbin/nologin
[mkandes@nsgosg ~]$
[mkandes@nsgosg ~]$ getent group | grep xrootd
xrootd:*:296:
xrootd:x:296:
[mkandes@nsgosg ~]$
```

Creating `nsgosdf` group.

```
[mkandes@nsgosg ~]$ getent group | grep 986
[mkandes@nsgosg ~]$ sudo groupadd -g 986 nsgosdf
[mkandes@nsgosg ~]$ getent group | grep 986
nsgosdf:x:986:
[mkandes@nsgosg ~]$
```

Adding my user to the group ...

```
[mkandes@nsgosg ~]$ sudo usermod --append --groups nsgosdf mkandes
Sorry, user mkandes is not allowed to execute '/sbin/usermod --append --groups nsgosdf mkandes' as root on nsgosg.sdsc.edu.
[mkandes@nsgosg ~]$
```

Blocked! Ask RDS to modify group affiliation?
