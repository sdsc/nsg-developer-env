2023/10/25

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
