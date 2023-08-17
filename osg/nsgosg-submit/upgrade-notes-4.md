2023/08/17

Continuing from `upgrade-notes-3.md`, we're again attempting to fix the authentication issue with nsgosg.sdsc.edu. In addition, RDS has created and NFS share for the `xrootd` user on their OSDF origin server, which we should now be able to use to export data to via this share. As such, we need to get it mounted as well. 

The following is the previous history that covered my last debugging session with Mats Rynge from OSG.

```
723  condor_config_val -summary > saved_condor_config_before_upgrade.20230502
  724  sudo yum-config-manager --enable powertools
  725  sudo systemctl stop condor
  726  sudo systemctl status condor
  727  sudo systemctl stop gratia-probes-cron
  728  sudo systemctl status gratia-probes-cron
  729  sudo yum update
  730  yum info condor
  731  [mkandes@nsgosg ~]$ yum info --enablerepo=osg-upcoming condor
  732  OSG Software for Enterprise Linux 8 - Upcoming  290 kB/s | 279 kB     00:00    
  733  Installed Packages
  734  Name         : condor
  735  Version      : 9.0.17
  736  Release      : 1.1.osg36.el8
  737  Architecture : x86_64
  738  Size         : 21 M
  739  Source       : condor-9.0.17-1.1.osg36.el8.src.rpm
  740  Repository   : @System
  741  From repo    : osg
  742  Summary      : HTCondor: High Throughput Computing
  743  URL          : http://www.cs.wisc.edu/condor/
  744  License      : ASL 2.0
  745  Description  : HTCondor is a specialized workload management system for
  746               : compute-intensive jobs. Like other full-featured batch systems,
  747               : HTCondor provides a job queueing mechanism, scheduling policy,
  748               : priority scheme, resource monitoring, and resource management.
  749               : Users submit their serial or parallel jobs to HTCondor, HTCondor
  750               : places them into a queue, chooses when and where to run the jobs
  751               : based upon a policy, carefully monitors their progress, and
  752               : ultimately informs the user upon completion.
  753  Available Packages
  754  Name         : condor
  755  Version      : 10.4.0
  756  Release      : 1.osg36up.el8
  757  Architecture : x86_64
  758  Size         : 8.3 M
  759  Source       : condor-10.4.0-1.osg36up.el8.src.rpm
  760  Repository   : osg-upcoming
  761  Summary      : HTCondor: High Throughput Computing
  762  URL          : https://www.cs.wisc.edu/htcondor/
  763  License      : ASL 2.0
  764  Description  : HTCondor is a specialized workload management system for
  765               : compute-intensive jobs. Like other full-featured batch systems,
  766               : HTCondor provides a job queueing mechanism, scheduling policy,
  767               : priority scheme, resource monitoring, and resource management.
  768               : Users submit their serial or parallel jobs to HTCondor, HTCondor
  769               : places them into a queue, chooses when and where to run the jobs
  770               : based upon a policy, carefully monitors their progress, and
  771               : ultimately informs the user upon completion.
  772  clear
  773  yum info --enablerepo=osg-upcoming condor
  774  yum --enablerepo=osg-upcoming,osg-testing --showduplicates list condor
  775  yum upgrade --enablerepo=osg-upcoming condor
  776  clear
  777  sudo yum upgrade --enablerepo=osg-upcoming condor
  778  sudo systemctl restart condor
  779  sudo systemctl status condor
  780  condor_q -version
  781  sudo systemctl status condor
  782  condor_q -version
  783  sudo systemctl restart gratia-probes-cron
  784  sudo systemctl status gratia-probes-cron
  785  clear
  786  condor_q
  787  host 132.249.20.215
  788  condor_q
  789  cd /var/log/
  790  ls
  791  cd condor/
  792  ls
  793  ls -lahtr
  794  less MasterLog
  795  condor_q
  796  less SchedLog
  797  sudo condor_q
  798  sudo -u condor condor_q
  799  cat /etc/condor/
  800  ls /etc/condor/
  801  ls -lahtr
  802  cd /etc/condor/
  803  ls -lahtr
  804  cd passwords.d/
  805  ls
  806  sudo ls passwords.d/
  807  sudo ls -lahtr passwords.d/
  808  sudo ls -lahtr condor_
  809  sudo ls -lahtr config.d/
  810  sudo less config.d/00-htcondor-9.0.config 
  811  condor
  812  ls /var/log/condor/
  813  sudo ls -lahtr config.d/
  814  [mkandes@nsgosg condor]$ sudo ls -lahtr config.d/
  815  total 24K
  816  -rw-r--r--. 1 root root   79 Dec 15  2020 95-nsg-submit-attrs.conf
  817  -rw-r--r--. 1 root root  118 Feb 23 12:15 81-osg-flock-version.conf
  818  -rw-r--r--. 1 root root 1.1K Feb 23 12:15 80-osg-flocking.conf
  819  -rw-r--r--. 1 root root  279 Feb 24 12:30 01-xcache-reporter-auth.conf
  820  -rw-r--r--. 1 root root  178 Mar  9 10:56 10-stash-plugin.conf
  821  -rw-r--r--. 1 root root 1004 Apr  6 08:59 00-htcondor-9.0.config
  822  drwxr-xr-x. 2 root root  193 May  2 11:51 .
  823  drwxr-xr-x. 6 root root  160 May  2 11:52 ..
  824  [mkandes@nsgosg condor]$
  825  clear
  826  ls
  827  ls -lahtr config.d/
  828  sudo cat config.d/00-htcondor-9.0.config 
  829  cd /
  830  cd ~/
  831  sudo dd if=/dev/urandom of=/etc/condor/password.d/POOL count=1 bs=1024
  832  sudo condor_store_cred -c add
  833  ls -lahtr /etc/condor/passwords.d/
  834  sudo ls -lahtr /etc/condor/passwords.d/
  835  sudo cat /etc/condor/passwords.d/POOL
  836  sudo condor_token_create -identity condor@nsgosg.sdsc.edu >/etc/condor/tokens.d/nsgosg.token
  837  sudo condor_token_create -identity condor@nsgosg.sdsc.edu > nsgosg.token
  838  less nsgosg.token 
  839  sudo cp nsgosg.token /etc/condor/tokens.d/
  840  sudo ls /etc/condor/tokens.d/
  841  sudo ls -lahtr /etc/condor/tokens.d/
  842  sudo chown condor:condor /etc/condor/tokens.d/nsgosg.token
  843  sudo chmod 600 /etc/condor/tokens.d/nsgosg.token
  844  sudo ls -lahtr /etc/condor/tokens.d/
  845  history | grep restart
  846  sudo systemctl restart condor
  847  sudo systemctl status condor
  848  condor_q
  849  ls
  850  cat /var/log/
  851  cat /var/log/condor/
  852  ls /var/log/condor/
  853  ls -lahtr /var/log/condor/
  854  less /var/log/condor/SchedLog
  855  cd /etc/condor/
  856  ls
  857  less condor_config 
  858  cd config.d/
  859  ls
  860  grep DAEMONS *
  861  less 01-xcache-reporter-auth.conf 
  862  less 10-stash-plugin.conf 
  863  less 80-osg-flocking.conf 
  864  less 81-osg-flock-version.conf 
  865  less 95-nsg-submit-attrs.conf 
  866  hostname -f
  867  localhost
  868  cat /var/log/condor/SchedLog
  869  cd ~?
  870  ls
  871  cd ~/
  872  ls
  873  condor_submit bash_pi.htcondor 
  874  cat /var/log/condor/SchedLog
  875  ls
  876  cd /etc/condor/
  877  ls
  878  cd config.d/
  879  ls -lahtr
  880  vi 00-htcondor-9.0.config 
  881  sudo vi 00-htcondor-9.0.config 
  882  sudo cat 00-htcondor-9.0.config 
  883  ls -lahtr
  884  ls -lahtr ../condor_config 
  885  less ../condor_config 
  886  cd ../
  887  cp condor_config ./
  888  cd ~/
  889  _CONDOR_ALL_DEBUG=D_ALL condor_q -debug
  890  cp /etc/condor/condor_config ./
  891  vi condor_config 
  892  sudo cp condor_config /etc/condor/
  893  history | grep restart
  894  sudo systemctl restart condor
  895  condor_q
  896  sudo systemctl status condor
  897  condor_submit bash_pi.htcondor 
  898  ls -lahtr /var/log/condor/
  899  cat /var/log/condor/AuditLog
  900  cat /var/log/condor/SchedLog
  901  _CONDOR_ALL_DEBUG=D_ALL condor_q -debug
  902  vi condor_config 
  903  sudo cp condor_config /etc/condor/
  904  ls -lahtr /etc/condor/
  905  vi 99-local.conf
  906  sudo cp 99-local.conf /etc/condor/config.d/
  907  ls -lahtr /etc/condor/config.d/
  908  history | grep restart
  909  sudo systemctl restart condor
  910  condor_q
  911  condor_status
  912  condor_q
  913  _CONDOR_ALL_DEBUG=D_ALL condor_q -debug | less
  914  _CONDOR_ALL_DEBUG=D_ALL condor_q -debug
  915  sudo reboot
  916  condor_q
  917  condor_config
  918  history | grep summary
  919  condor_config_val -summary
  920  condor_config_val -summary | less
  921  _CONDOR_ALL_DEBUG=D_ALL condor_q -debug
  922  ls -lahtr /etc/grid-security/xrd/xrdcert.pem
  923  condor_q
  924  _CONDOR_ALL_DEBUG=D_ALL condor_q -debug
  925  sudo _CONDOR_ALL_DEBUG=D_ALL condor_q -debug
  926  cat /etc/os-release 
  927  condor_status
  928  exit

```

Let's start by checking the current operating system version again. 

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
[mkandes@nsgosg ~]$
```

Then verify the central managers in our configuration are still active.

```
mkandes@hardtack:~$ nmap -Pn cm-1.ospool.osg-htc.org
Starting Nmap 7.80 ( https://nmap.org ) at 2023-08-17 09:42 PDT
Nmap scan report for cm-1.ospool.osg-htc.org (128.104.103.187)
Host is up (0.33s latency).
rDNS record for 128.104.103.187: psc-bridges2-ce2.svc.opensciencegrid.org
Not shown: 997 filtered ports
PORT     STATE SERVICE
80/tcp   open  http
8000/tcp open  http-alt
9618/tcp open  condor

Nmap done: 1 IP address (1 host up) scanned in 42.08 seconds
mkandes@hardtack:~$ nmap -Pn cm-2.ospool.osg-htc.org
Starting Nmap 7.80 ( https://nmap.org ) at 2023-08-17 09:43 PDT
Nmap scan report for cm-2.ospool.osg-htc.org (192.170.231.10)
Host is up (0.059s latency).
Not shown: 989 closed ports
PORT     STATE    SERVICE
22/tcp   open     ssh
80/tcp   open     http
111/tcp  open     rpcbind
179/tcp  open     bgp
646/tcp  filtered ldp
6839/tcp open     unknown
6881/tcp open     bittorrent-tracker
6901/tcp open     jetstream
8000/tcp open     http-alt
9100/tcp open     jetdirect
9618/tcp open     condor

Nmap done: 1 IP address (1 host up) scanned in 2.04 seconds
mkandes@hardtack:~$
```

The first issue at present is that `condor_q` command is unable to fetch job classads from the submit host itself.

```
[mkandes@nsgosg ~]$  condor_q

-- Failed to fetch ads from: <132.249.20.215:9618?addrs=132.249.20.215-9618&alias=nsgosg.sdsc.edu&noUDP&sock=schedd_1423_a35b> : nsgosg.sdsc.edu
AUTHENTICATE:1003:Failed to authenticate with any method
[mkandes@nsgosg ~]$
```

While at the same time, we can fetch machine classads from the central managers using the `condor_status` command. 

```
[mkandes@nsgosg ~]$ condor_status | head -n 10
Name                                                                  OpSys      Arch   State      Activity     LoadAv Mem     ActvtyTime

slot1@glidein_23644_561893560@C09.cm.cluster                          LINUX      X86_64 Unclaimed  Idle          0.000  37376  0+14:32:05
slot1_1@glidein_23644_561893560@C09.cm.cluster                        LINUX      X86_64 Claimed    Busy          1.000   4096  0+09:59:50
slot1_2@glidein_23644_561893560@C09.cm.cluster                        LINUX      X86_64 Claimed    Busy          1.000   2560  0+00:03:25
slot1_3@glidein_23644_561893560@C09.cm.cluster                        LINUX      X86_64 Claimed    Busy          1.000   4096  0+09:59:50
slot1_4@glidein_23644_561893560@C09.cm.cluster                        LINUX      X86_64 Claimed    Busy          1.000   2560  0+00:03:17
slot1_5@glidein_23644_561893560@C09.cm.cluster                        LINUX      X86_64 Claimed    Busy          1.000   4096  0+09:59:49
slot1_6@glidein_23644_561893560@C09.cm.cluster                        LINUX      X86_64 Claimed    Busy          1.000   4096  0+09:59:49
slot1_7@glidein_23644_561893560@C09.cm.cluster                        LINUX      X86_64 Claimed    Busy          1.000   2560  0+00:05:55
[mkandes@nsgosg ~]$
```
First change to attempt a fix is to include the pool password authentication method in the security configuration. Starting from ...
```
[mkandes@nsgosg ~]$ cd /etc/condor/config.d/
[mkandes@nsgosg config.d]$ grep -H SEC *
01-xcache-reporter-auth.conf:SEC_CLIENT_AUTHENTICATION_METHODS = SSL
80-osg-flocking.conf:SCHEDD.SEC_CLIENT_AUTHENTICATION = REQUIRED
80-osg-flocking.conf:SCHEDD.SEC_CLIENT_ENCRYPTION = REQUIRED
80-osg-flocking.conf:SCHEDD.SEC_DEFAULT_ENCRYPTION = REQUIRED
99-local.conf:SEC_DEFAULT_AUTHENTICATION_METHODS = FS, IDTOKENS
[mkandes@nsgosg config.d]$
```
... making change to ...
```
[mkandes@nsgosg config.d]$ grep -H SEC *
01-xcache-reporter-auth.conf:SEC_CLIENT_AUTHENTICATION_METHODS = SSL
80-osg-flocking.conf:SCHEDD.SEC_CLIENT_AUTHENTICATION = REQUIRED
80-osg-flocking.conf:SCHEDD.SEC_CLIENT_ENCRYPTION = REQUIRED
80-osg-flocking.conf:SCHEDD.SEC_DEFAULT_ENCRYPTION = REQUIRED
99-local.conf:SEC_DEFAULT_AUTHENTICATION_METHODS = FS, PASSWORD, IDTOKENS
[mkandes@nsgosg config.d]$
```
Authentication still failing.
```
[mkandes@nsgosg config.d]$ sudo systemctl restart condor
[mkandes@nsgosg config.d]$ sudo systemctl status condor
● condor.service - Condor Distributed High-Throughput-Computing
   Loaded: loaded (/usr/lib/systemd/system/condor.service; enabled; vendor preset: disabled)
  Drop-In: /usr/lib/systemd/system/condor.service.d
           └─osg-env.conf
   Active: active (running) since Thu 2023-08-17 10:01:30 PDT; 2s ago
 Main PID: 73762 (condor_master)
   Status: "All daemons are responding"
    Tasks: 4 (limit: 4194303)
   Memory: 8.7M
   CGroup: /system.slice/condor.service
           ├─73762 /usr/sbin/condor_master -f
           ├─73802 condor_procd -A /var/run/condor/procd_pipe -L /var/log/condor/ProcLog -R 1000000 -S 60 -C 992
           ├─73803 condor_shared_port
           └─73804 condor_schedd

Aug 17 10:01:30 nsgosg.sdsc.edu systemd[1]: Started Condor Distributed High-Throughput-Computing.
[mkandes@nsgosg config.d]$ condor_q

-- Failed to fetch ads from: <132.249.20.215:9618?addrs=132.249.20.215-9618&alias=nsgosg.sdsc.edu&noUDP&sock=schedd_73762_2cda> : nsgosg.sdsc.edu
AUTHENTICATE:1003:Failed to authenticate with any method
[mkandes@nsgosg config.d]$
```

Next, let's try reverting to the older default security model prior to HTCondor v9.x. See https://htcondor-wiki.cs.wisc.edu/index.cgi/wiki?p=UpgradingFromEightNineToNineZero. This may help us determine if the issue is the new securrity policies enforced by default after the last upgrade of HTCondor. Starting with ...
```
[mkandes@nsgosg config.d]$ grep ^use 00-htcondor-9.0.config 
use security:recommended_v9_0
[mkandes@nsgosg config.d]$
```
... and changing back to host-based authentication ...
```
[mkandes@nsgosg config.d]$ grep ^use 00-htcondor-9.0.config 
use security:host_based
```
Still failing authentication.

```
[mkandes@nsgosg config.d]$ sudo systemctl restart condor
[mkandes@nsgosg config.d]$ sudo systemctl status condor
● condor.service - Condor Distributed High-Throughput-Computing
   Loaded: loaded (/usr/lib/systemd/system/condor.service; enabled; vendor preset: disabled)
  Drop-In: /usr/lib/systemd/system/condor.service.d
           └─osg-env.conf
   Active: active (running) since Thu 2023-08-17 10:09:14 PDT; 5s ago
 Main PID: 73900 (condor_master)
   Status: "All daemons are responding"
    Tasks: 4 (limit: 4194303)
   Memory: 8.7M
   CGroup: /system.slice/condor.service
           ├─73900 /usr/sbin/condor_master -f
           ├─73940 condor_procd -A /var/run/condor/procd_pipe -L /var/log/condor/ProcLog -R 1000000 -S 60 -C 992
           ├─73941 condor_shared_port
           └─73942 condor_schedd

Aug 17 10:09:14 nsgosg.sdsc.edu systemd[1]: Started Condor Distributed High-Throughput-Computing.
[mkandes@nsgosg config.d]$ condor_q

-- Failed to fetch ads from: <132.249.20.215:9618?addrs=132.249.20.215-9618&alias=nsgosg.sdsc.edu&noUDP&sock=schedd_73900_d4ec> : nsgosg.sdsc.edu
AUTHENTICATE:1003:Failed to authenticate with any method
[mkandes@nsgosg config.d]$
```
Well, this might explain why the pool password authentication is not working.

```
[mkandes@nsgosg config.d]$ sudo condor_check_password
Key tests:
FAIL      /etc/condor/passwords.d/POOL: Key is too short: 11 bytes

There were 0 compatible keys and 1 keys with issues.

HTCondor recommends passwords be longer than 12 characters.
[mkandes@nsgosg config.d]$
```

Note, however, the tokens look okay.

```
[mkandes@nsgosg config.d]$ sudo condor_check_password /etc/condor/tokens.d/ospool.token
Key tests:
OK        /etc/condor/tokens.d/ospool.token

There were 1 compatible keys and 0 keys with issues.
[mkandes@nsgosg config.d]$ sudo condor_check_password /etc/condor/tokens.d/nsgosg.token
Key tests:
OK        /etc/condor/tokens.d/nsgosg.token

There were 1 compatible keys and 0 keys with issues.
[mkandes@nsgosg config.d]$
```

The following snippet from the SchedLog is representative of the typical log messages observed over the past month prior to starting up this debugging work again today.

```
08/16/23 20:53:14 condor_write(): Socket closed when trying to write 4112 bytes to collector cm-1.ospool.osg-htc.org, fd is 13
08/16/23 20:53:14 Buf::write(): condor_write() failed
08/16/23 20:53:14 condor_write(): Socket closed when trying to write 4112 bytes to collector cm-2.ospool.osg-htc.org, fd is 15
08/16/23 20:53:14 Buf::write(): condor_write() failed
08/16/23 20:54:23 Number of Active Workers 0
08/16/23 20:55:55 Number of Active Workers 0
08/16/23 20:55:55 Number of Active Workers 0
08/16/23 20:55:55 Number of Active Workers 0
08/16/23 21:00:42 condor_read(): Socket closed abnormally when trying to read 5 bytes from  in non-blocking mode, errno=104 Connection reset by peer
08/16/23 21:00:42 DaemonCore: Can't receive command request from  (perhaps a timeout?)
08/16/23 21:00:42 Received a superuser command
08/16/23 21:00:42 condor_read(): Socket closed abnormally when trying to read 5 bytes from <132.249.119.214:49074> in non-blocking mode, errno=104 Connection reset by peer
08/16/23 21:00:42 DaemonCore: Can't receive command request from 132.249.119.214 (perhaps a timeout?)
08/16/23 21:00:59 Received a superuser command
08/16/23 21:00:59 DaemonCore: Can't receive command request from 132.249.119.214 (perhaps a timeout?)
08/16/23 21:01:14 IO: Incoming packet header unrecognized : 47 45 54 20 2f
08/16/23 21:01:14 DaemonCore: Can't receive command request from 132.249.119.214 (perhaps a timeout?)
08/16/23 21:01:14 Received a superuser command
08/16/23 21:01:14 IO: Incoming packet header unrecognized : 47 45 54 20 2f
08/16/23 21:01:14 DaemonCore: Can't receive command request from 132.249.119.214 (perhaps a timeout?)
08/16/23 21:01:14 IO: Incoming packet header unrecognized : 49 00 00 00 66
08/16/23 21:01:14 DaemonCore: Can't receive command request from 132.249.119.214 (perhaps a timeout?)
08/16/23 21:01:15 Received a superuser command
08/16/23 21:01:15 IO: Incoming packet header unrecognized : 49 00 00 00 66
08/16/23 21:01:15 DaemonCore: Can't receive command request from 132.249.119.214 (perhaps a timeout?)
08/16/23 21:01:15 IO: Incoming packet header unrecognized : 48 45 4c 50 0d
08/16/23 21:01:15 DaemonCore: Can't receive command request from 132.249.119.214 (perhaps a timeout?)
08/16/23 21:01:15 Received a superuser command
08/16/23 21:01:15 IO: Incoming packet header unrecognized : 48 45 4c 50 0d
08/16/23 21:01:15 DaemonCore: Can't receive command request from 132.249.119.214 (perhaps a timeout?)
08/16/23 21:01:29 condor_read(): Socket closed abnormally when trying to read 16323 bytes from <132.249.119.214:46874> in non-blocking mode, errno=104 Connection reset by peer
08/16/23 21:01:29 Buf::read(): condor_read() failed
08/16/23 21:01:29 IO: Packet read failed: read -2 of 16323
08/16/23 21:01:29 DaemonCore: Can't receive command request from 132.249.119.214 (perhaps a timeout?)
08/16/23 21:01:29 IO: Incoming packet is larger than 1MB limit (requested size 17432576) : 03 01 0a 00 00
08/16/23 21:01:29 DaemonCore: Can't receive command request from 132.249.119.214 (perhaps a timeout?)
```
Hmmm.

```
[mkandes@nsgosg config.d]$ condor_check_config 
obsolete ALLOW_WRITE_COLLECTOR ALLOW_WRITE_STARTD :
    In 8.8 ALLOW_DAEMON_<name> would inherit from ALLOW_WRITE_<name>, but in 9.0 this no
    longer happens.  You should use
       condor_config_val -verbose -dump ALLOW_WRITE_
    To find obsolete uses of ALLOW_WRITE and either delete them, or change them to ALLOW_DAEMON

[mkandes@nsgosg config.d]$ condor_config_val -verbose -dump ALLOW_WRITE_
# Configuration from machine: nsgosg.sdsc.edu

# Parameters with names that match ALLOW_WRITE_:
ALLOW_WRITE_COLLECTOR = $(ALLOW_WRITE) $(FLOCK_FROM)
 # at: /etc/condor/config.d/00-htcondor-9.0.config, line 25, use SECURITY:HOST_BASED+6
 # expanded: nsgosg.sdsc.edu 132.249.20.215  
ALLOW_WRITE_STARTD = $(ALLOW_WRITE) $(FLOCK_FROM)
 # at: /etc/condor/config.d/00-htcondor-9.0.config, line 25, use SECURITY:HOST_BASED+7
 # expanded: nsgosg.sdsc.edu 132.249.20.215  
[mkandes@nsgosg config.d]$
```

Let's go ahead and restart condor with host-based security enabled and make a copy of the daemon logs. We'll then revert back to HTCondor v9.x security model and do the same.

`/var/log/condor/MasterLog`

```
08/17/23 11:02:43 ******************************************************
08/17/23 11:02:43 ** condor_master (CONDOR_MASTER) STARTING UP
08/17/23 11:02:43 ** /usr/sbin/condor_master
08/17/23 11:02:43 ** SubsystemInfo: name=MASTER type=MASTER(1) class=DAEMON(1)
08/17/23 11:02:43 ** Configuration: subsystem:MASTER local:<NONE> class:DAEMON
08/17/23 11:02:43 ** $CondorVersion: 10.4.0 2023-04-07 PackageID: 10.4.0-1 $
08/17/23 11:02:43 ** $CondorPlatform: X86_64-Rocky_8.7 $
08/17/23 11:02:43 ** PID = 74715
08/17/23 11:02:43 ** Log last touched 8/17 11:02:43
08/17/23 11:02:43 ******************************************************
08/17/23 11:02:43 Using config source: /etc/condor/condor_config
08/17/23 11:02:43 Using local config sources: 
08/17/23 11:02:43    /usr/share/condor/config.d/50-gratia-gwms.conf
08/17/23 11:02:43    /etc/condor/config.d/00-htcondor-9.0.config
08/17/23 11:02:43    /etc/condor/config.d/01-xcache-reporter-auth.conf
08/17/23 11:02:43    /etc/condor/config.d/10-stash-plugin.conf
08/17/23 11:02:43    /etc/condor/config.d/80-osg-flocking.conf
08/17/23 11:02:43    /etc/condor/config.d/81-osg-flock-version.conf
08/17/23 11:02:43    /etc/condor/config.d/95-nsg-submit-attrs.conf
08/17/23 11:02:43    /etc/condor/config.d/99-local.conf
08/17/23 11:02:43    /etc/condor/condor_config.local
08/17/23 11:02:43 config Macros = 90, Sorted = 90, StringBytes = 3306, TablesBytes = 3344
08/17/23 11:02:43 CLASSAD_CACHING is OFF
08/17/23 11:02:43 Daemon Log is logging: D_ALWAYS D_ERROR D_STATUS
08/17/23 11:02:44 SharedPortEndpoint: waiting for connections to named socket master_74715_da9c
08/17/23 11:02:44 SharedPortEndpoint: failed to open /var/lock/condor/shared_port_ad: No such file or directory
08/17/23 11:02:44 SharedPortEndpoint: did not successfully find SharedPortServer address. Will retry in 60s.
08/17/23 11:02:44 DaemonCore: private command socket at <132.249.20.215:0?alias=nsgosg.sdsc.edu&sock=master_74715_da9c>
08/17/23 11:02:45 Adding SHARED_PORT to DAEMON_LIST, because USE_SHARED_PORT=true (to disable this, set AUTO_INCLUDE_SHARED_PORT_IN_DAEMON_LIST=False)
08/17/23 11:02:45 Master restart (GRACEFUL) is watching /usr/sbin/condor_master (mtime:1680877544)
08/17/23 11:02:45 Starting shared port with port: 9618
08/17/23 11:02:45 Started DaemonCore process "/usr/libexec/condor/condor_shared_port", pid and pgroup = 74754
08/17/23 11:02:45 Waiting for /var/lock/condor/shared_port_ad to appear.
08/17/23 11:02:45 Found /var/lock/condor/shared_port_ad.
08/17/23 11:02:45 Started DaemonCore process "/usr/sbin/condor_schedd", pid and pgroup = 74755
08/17/23 11:02:45 Daemons::StartAllDaemons all daemons were started
08/17/23 11:12:50 condor_write(): Socket closed when trying to write 2232 bytes to collector cm-1.ospool.osg-htc.org, fd is 12
08/17/23 11:12:50 Buf::write(): condor_write() failed
08/17/23 11:12:50 condor_write(): Socket closed when trying to write 2232 bytes to collector cm-2.ospool.osg-htc.org, fd is 13
08/17/23 11:12:50 Buf::write(): condor_write() failed
```

`/var/log/condor/SchedLog`

```
08/17/23 11:02:45 ******************************************************
08/17/23 11:02:45 ** condor_schedd (CONDOR_SCHEDD) STARTING UP
08/17/23 11:02:45 ** /usr/sbin/condor_schedd
08/17/23 11:02:45 ** SubsystemInfo: name=SCHEDD type=SCHEDD(4) class=DAEMON(1)
08/17/23 11:02:45 ** Configuration: subsystem:SCHEDD local:<NONE> class:DAEMON
08/17/23 11:02:45 ** $CondorVersion: 10.4.0 2023-04-07 PackageID: 10.4.0-1 $
08/17/23 11:02:45 ** $CondorPlatform: X86_64-Rocky_8.7 $
08/17/23 11:02:45 ** PID = 74755
08/17/23 11:02:45 ** Log last touched 8/17 11:02:43
08/17/23 11:02:45 ******************************************************
08/17/23 11:02:45 Using config source: /etc/condor/condor_config
08/17/23 11:02:45 Using local config sources: 
08/17/23 11:02:45    /usr/share/condor/config.d/50-gratia-gwms.conf
08/17/23 11:02:45    /etc/condor/config.d/00-htcondor-9.0.config
08/17/23 11:02:45    /etc/condor/config.d/01-xcache-reporter-auth.conf
08/17/23 11:02:45    /etc/condor/config.d/10-stash-plugin.conf
08/17/23 11:02:45    /etc/condor/config.d/80-osg-flocking.conf
08/17/23 11:02:45    /etc/condor/config.d/81-osg-flock-version.conf
08/17/23 11:02:45    /etc/condor/config.d/95-nsg-submit-attrs.conf
08/17/23 11:02:45    /etc/condor/config.d/99-local.conf
08/17/23 11:02:45    /etc/condor/condor_config.local
08/17/23 11:02:45 config Macros = 91, Sorted = 91, StringBytes = 3353, TablesBytes = 3380
08/17/23 11:02:45 CLASSAD_CACHING is ENABLED
08/17/23 11:02:45 Daemon Log is logging: D_ALWAYS D_ERROR D_STATUS D_AUDIT
08/17/23 11:02:45 SharedPortEndpoint: waiting for connections to named socket schedd_74715_da9c
08/17/23 11:02:45 DaemonCore: command socket at <132.249.20.215:9618?addrs=132.249.20.215-9618&alias=nsgosg.sdsc.edu&noUDP&sock=schedd_74715_da9c>
08/17/23 11:02:45 DaemonCore: private command socket at <132.249.20.215:9618?addrs=132.249.20.215-9618&alias=nsgosg.sdsc.edu&noUDP&sock=schedd_74715_da9c>
08/17/23 11:02:45 History file rotation is enabled.
08/17/23 11:02:45   Maximum history file size is: 20971520 bytes
08/17/23 11:02:45   Number of rotated history files is: 2
08/17/23 11:02:45 Logging per-job history files to: /var/lib/condor/gratia/data
08/17/23 11:02:45 CronJobList: Adding job 'GRATIA'
08/17/23 11:02:45 CronJob: Initializing job 'GRATIA' (/usr/share/gratia/condor-ap/condor_meter)
08/17/23 11:02:45 Reloading job factories
08/17/23 11:02:45 Loaded 0 job factories, 0 were paused, 0 failed to load
08/17/23 11:02:45 TransferQueueManager stats: active up=0/100 down=0/100; waiting up=0 down=0; wait time up=0s down=0s
08/17/23 11:02:45 TransferQueueManager upload 1m I/O load: 0 bytes/s  0.000 disk load  0.000 net load
08/17/23 11:02:45 TransferQueueManager download 1m I/O load: 0 bytes/s  0.000 disk load  0.000 net load
08/17/23 11:02:47 DC_AUTHENTICATE: required authentication of 128.105.82.84 failed: AUTHENTICATE:1003:Failed to authenticate with any method|AUTHENTICATE:1004:Failed to authenticate using IDTOKENS|AUTHENTICATE:1004:Failed to authenticate using FS|FS:1004:Unable to lstat(/tmp/FS_XXXbONQUN)
08/17/23 11:02:47 DC_AUTHENTICATE: required authentication of 128.105.82.84 failed: AUTHENTICATE:1003:Failed to authenticate with any method|AUTHENTICATE:1004:Failed to authenticate using IDTOKENS|AUTHENTICATE:1004:Failed to authenticate using FS|FS:1004:Unable to lstat(/tmp/FS_XXXnCLVP8)
08/17/23 11:02:47 DC_AUTHENTICATE: required authentication of 128.105.82.84 failed: AUTHENTICATE:1003:Failed to authenticate with any method|AUTHENTICATE:1004:Failed to authenticate using IDTOKENS|AUTHENTICATE:1004:Failed to authenticate using FS|FS:1004:Unable to lstat(/tmp/FS_XXXIK0PTa)
08/17/23 11:03:10 DC_AUTHENTICATE: required authentication of 128.105.244.7 failed: AUTHENTICATE:1003:Failed to authenticate with any method|AUTHENTICATE:1004:Failed to authenticate using IDTOKENS|AUTHENTICATE:1004:Failed to authenticate using FS|FS:1004:Unable to lstat(/tmp/FS_XXXgv28H4)
08/17/23 11:12:12 DC_AUTHENTICATE: required authentication of 128.105.82.84 failed: AUTHENTICATE:1003:Failed to authenticate with any method|AUTHENTICATE:1004:Failed to authenticate using IDTOKENS|AUTHENTICATE:1004:Failed to authenticate using FS|FS:1004:Unable to lstat(/tmp/FS_XXXaw9ng1)
08/17/23 11:12:46 condor_write(): Socket closed when trying to write 4112 bytes to collector cm-1.ospool.osg-htc.org, fd is 16
08/17/23 11:12:46 Buf::write(): condor_write() failed
08/17/23 11:12:46 condor_write(): Socket closed when trying to write 4112 bytes to collector cm-2.ospool.osg-htc.org, fd is 17
08/17/23 11:12:46 Buf::write(): condor_write() failed
08/17/23 11:12:47 DC_AUTHENTICATE: required authentication of 128.105.244.7 failed: AUTHENTICATE:1003:Failed to authenticate with any method|AUTHENTICATE:1004:Failed to authenticate using IDTOKENS|AUTHENTICATE:1004:Failed to authenticate using FS|FS:1004:Unable to lstat(/tmp/FS_XXXPRUZxy)
```

`/var/log/condor/ToolLog`

```
03/21/23 18:21:28 condor_write(): Socket closed when trying to write 376 bytes to <128.105.244.7:46262>, fd is 19
03/21/23 18:21:28 Buf::write(): condor_write() failed
03/21/23 18:21:28 condor_history: Failed to write final ad to client
05/02/23 11:57:47 condor_write(): Socket closed when trying to write 376 bytes to <128.105.244.7:42001>, fd is 15
05/02/23 11:57:48 Buf::write(): condor_write() failed
05/02/23 11:57:48 condor_history: Failed to write final ad to client
05/02/23 14:30:32 condor_write(): Socket closed when trying to write 376 bytes to <128.105.244.7:46203>, fd is 15
05/02/23 14:30:32 Buf::write(): condor_write() failed
05/02/23 14:30:32 condor_history: Failed to write final ad to client
06/20/23 20:21:47 condor_write(): Socket closed when trying to write 376 bytes to <128.105.244.7:40272>, fd is 16
06/20/23 20:21:47 Buf::write(): condor_write() failed
06/20/23 20:21:47 condor_history: Failed to write final ad to client
06/20/23 20:41:30 condor_write(): Socket closed when trying to write 376 bytes to <128.105.244.7:34217>, fd is 15
06/20/23 20:41:30 Buf::write(): condor_write() failed
06/20/23 20:41:30 condor_history: Failed to write final ad to client
07/18/23 19:00:51 condor_write(): Socket closed when trying to write 376 bytes to <128.105.244.7:46187>, fd is 15
07/18/23 19:00:51 Buf::write(): condor_write() failed
07/18/23 19:00:51 condor_history: Failed to write final ad to client
08/15/23 18:16:03 condor_write(): Socket closed when trying to write 376 bytes to <128.105.244.7:44770>, fd is 15
08/15/23 18:16:03 Buf::write(): condor_write() failed
08/15/23 18:16:03 condor_history: Failed to write final ad to client
```

Moving back to v9.x security model.

```
[mkandes@nsgosg ~]$ cd /etc/condor/config.d/
[mkandes@nsgosg config.d]$ sudo vi 00-htcondor-9.0.config 
[sudo] password for mkandes: 
Duo two-factor login for mkandes

Enter a passcode or select one of the following options:

 1. Duo Push to XXX-XXX-7242
 2. SMS passcodes to XXX-XXX-7242

Passcode or option (1-2): 1

Please open Duo Mobile and check for Duo Push requests manually.
Success. Logging you in...
[mkandes@nsgosg config.d]$ grep ^use 00-htcondor-9.0.config 
use security:recommended_v9_0
[mkandes@nsgosg config.d]$
```

```
[mkandes@nsgosg config.d]$ sudo systemctl status condor
● condor.service - Condor Distributed High-Throughput-Computing
   Loaded: loaded (/usr/lib/systemd/system/condor.service; enabled; vendor preset: disabled)
  Drop-In: /usr/lib/systemd/system/condor.service.d
           └─osg-env.conf
   Active: active (running) since Thu 2023-08-17 11:16:43 PDT; 28s ago
 Main PID: 74932 (condor_master)
   Status: "All daemons are responding"
    Tasks: 4 (limit: 4194303)
   Memory: 9.9M
   CGroup: /system.slice/condor.service
           ├─74932 /usr/sbin/condor_master -f
           ├─74972 condor_procd -A /var/run/condor/procd_pipe -L /var/log/condor/ProcLog -R 1000000 -S 60>
           ├─74973 condor_shared_port
           └─74974 condor_schedd

Aug 17 11:16:43 nsgosg.sdsc.edu systemd[1]: Started Condor Distributed High-Throughput-Computing.
```

`/var/log/condor/MasterLog`

```
08/17/23 11:16:43 ******************************************************
08/17/23 11:16:43 ** condor_master (CONDOR_MASTER) STARTING UP
08/17/23 11:16:43 ** /usr/sbin/condor_master
08/17/23 11:16:43 ** SubsystemInfo: name=MASTER type=MASTER(1) class=DAEMON(1)
08/17/23 11:16:43 ** Configuration: subsystem:MASTER local:<NONE> class:DAEMON
08/17/23 11:16:43 ** $CondorVersion: 10.4.0 2023-04-07 PackageID: 10.4.0-1 $
08/17/23 11:16:43 ** $CondorPlatform: X86_64-Rocky_8.7 $
08/17/23 11:16:43 ** PID = 74932
08/17/23 11:16:43 ** Log last touched 8/17 11:16:43
08/17/23 11:16:43 ******************************************************
08/17/23 11:16:43 Using config source: /etc/condor/condor_config
08/17/23 11:16:43 Using local config sources: 
08/17/23 11:16:43    /usr/share/condor/config.d/50-gratia-gwms.conf
08/17/23 11:16:43    /etc/condor/config.d/00-htcondor-9.0.config
08/17/23 11:16:43    /etc/condor/config.d/01-xcache-reporter-auth.conf
08/17/23 11:16:43    /etc/condor/config.d/10-stash-plugin.conf
08/17/23 11:16:43    /etc/condor/config.d/80-osg-flocking.conf
08/17/23 11:16:43    /etc/condor/config.d/81-osg-flock-version.conf
08/17/23 11:16:43    /etc/condor/config.d/95-nsg-submit-attrs.conf
08/17/23 11:16:43    /etc/condor/config.d/99-local.conf
08/17/23 11:16:43    /etc/condor/condor_config.local
08/17/23 11:16:43 config Macros = 91, Sorted = 91, StringBytes = 3173, TablesBytes = 3380
08/17/23 11:16:43 CLASSAD_CACHING is OFF
08/17/23 11:16:43 Daemon Log is logging: D_ALWAYS D_ERROR D_STATUS
08/17/23 11:16:44 SharedPortEndpoint: waiting for connections to named socket master_74932_b2a9
08/17/23 11:16:44 SharedPortEndpoint: failed to open /var/lock/condor/shared_port_ad: No such file or directory
08/17/23 11:16:44 SharedPortEndpoint: did not successfully find SharedPortServer address. Will retry in 60s.
08/17/23 11:16:44 DaemonCore: private command socket at <132.249.20.215:0?alias=nsgosg.sdsc.edu&sock=master_74932_b2a9>
08/17/23 11:16:44 Adding SHARED_PORT to DAEMON_LIST, because USE_SHARED_PORT=true (to disable this, set AUTO_INCLUDE_SHARED_PORT_IN_DAEMON_LIST=False)
08/17/23 11:16:44 Master restart (GRACEFUL) is watching /usr/sbin/condor_master (mtime:1680877544)
08/17/23 11:16:44 Starting shared port with port: 9618
08/17/23 11:16:44 Started DaemonCore process "/usr/libexec/condor/condor_shared_port", pid and pgroup = 74973
08/17/23 11:16:44 Waiting for /var/lock/condor/shared_port_ad to appear.
08/17/23 11:16:44 Found /var/lock/condor/shared_port_ad.
08/17/23 11:16:44 Started DaemonCore process "/usr/sbin/condor_schedd", pid and pgroup = 74974
08/17/23 11:16:44 Daemons::StartAllDaemons all daemons were started
```

`/var/log/condor/SchedLog`

```
08/17/23 11:16:44 ******************************************************
08/17/23 11:16:44 ** condor_schedd (CONDOR_SCHEDD) STARTING UP
08/17/23 11:16:44 ** /usr/sbin/condor_schedd
08/17/23 11:16:44 ** SubsystemInfo: name=SCHEDD type=SCHEDD(4) class=DAEMON(1)
08/17/23 11:16:44 ** Configuration: subsystem:SCHEDD local:<NONE> class:DAEMON
08/17/23 11:16:44 ** $CondorVersion: 10.4.0 2023-04-07 PackageID: 10.4.0-1 $
08/17/23 11:16:44 ** $CondorPlatform: X86_64-Rocky_8.7 $
08/17/23 11:16:44 ** PID = 74974
08/17/23 11:16:44 ** Log last touched 8/17 11:16:43
08/17/23 11:16:44 ******************************************************
08/17/23 11:16:44 Using config source: /etc/condor/condor_config
08/17/23 11:16:44 Using local config sources: 
08/17/23 11:16:44    /usr/share/condor/config.d/50-gratia-gwms.conf
08/17/23 11:16:44    /etc/condor/config.d/00-htcondor-9.0.config
08/17/23 11:16:44    /etc/condor/config.d/01-xcache-reporter-auth.conf
08/17/23 11:16:44    /etc/condor/config.d/10-stash-plugin.conf
08/17/23 11:16:44    /etc/condor/config.d/80-osg-flocking.conf
08/17/23 11:16:44    /etc/condor/config.d/81-osg-flock-version.conf
08/17/23 11:16:44    /etc/condor/config.d/95-nsg-submit-attrs.conf
08/17/23 11:16:44    /etc/condor/config.d/99-local.conf
08/17/23 11:16:44    /etc/condor/condor_config.local
08/17/23 11:16:44 config Macros = 92, Sorted = 92, StringBytes = 3219, TablesBytes = 3416
08/17/23 11:16:44 CLASSAD_CACHING is ENABLED
08/17/23 11:16:44 Daemon Log is logging: D_ALWAYS D_ERROR D_STATUS D_AUDIT
08/17/23 11:16:44 SharedPortEndpoint: waiting for connections to named socket schedd_74932_b2a9
08/17/23 11:16:44 DaemonCore: command socket at <132.249.20.215:9618?addrs=132.249.20.215-9618&alias=nsgosg.sdsc.edu&noUDP&sock=schedd_74932_b2a9>
08/17/23 11:16:44 DaemonCore: private command socket at <132.249.20.215:9618?addrs=132.249.20.215-9618&alias=nsgosg.sdsc.edu&noUDP&sock=schedd_74932_b2a9>
08/17/23 11:16:44 History file rotation is enabled.
08/17/23 11:16:44   Maximum history file size is: 20971520 bytes
08/17/23 11:16:44   Number of rotated history files is: 2
08/17/23 11:16:44 Logging per-job history files to: /var/lib/condor/gratia/data
08/17/23 11:16:44 CronJobList: Adding job 'GRATIA'
08/17/23 11:16:44 CronJob: Initializing job 'GRATIA' (/usr/share/gratia/condor-ap/condor_meter)
08/17/23 11:16:44 Reloading job factories
08/17/23 11:16:44 Loaded 0 job factories, 0 were paused, 0 failed to load
08/17/23 11:16:44 TransferQueueManager stats: active up=0/100 down=0/100; waiting up=0 down=0; wait time up=0s down=0s
08/17/23 11:16:44 TransferQueueManager upload 1m I/O load: 0 bytes/s  0.000 disk load  0.000 net load
08/17/23 11:16:44 TransferQueueManager download 1m I/O load: 0 bytes/s  0.000 disk load  0.000 net load
```
After running `condor_q` command, this is the authentication error message created in the SchedLog.

```
08/17/23 11:20:29 DC_AUTHENTICATE: authentication of <132.249.20.215:13975> did not result in a valid mapped user name, which is required for this command (519 QUERY_JOB_ADS_WITH_AUTH), so aborting.
08/17/23 11:20:29 DC_AUTHENTICATE: reason for authentication failure: AUTHENTICATE:1003:Failed to authenticate with any method
```

Let's try changing the ownership of the ID tokens as suggested in the HTCondor Wiki link above.

```
Step 3: Directory permission changed in /etc/condor/tokens.d

HTCondor now reads files in /etc/condor/tokens.d as root. If you have files in that directory, you should change their ownership, using the following command (run as root):

   # chown -R root:root /etc/condor/tokens.d
```

```
[mkandes@nsgosg ~]$ sudo ls -lahtr /etc/condor/tokens.d
[sudo] password for mkandes: 
Duo two-factor login for mkandes

Enter a passcode or select one of the following options:

 1. Duo Push to XXX-XXX-7242
 2. SMS passcodes to XXX-XXX-7242

Passcode or option (1-2): 1

Please open Duo Mobile and check for Duo Push requests manually.
Success. Logging you in...
total 8.0K
-rw-------. 1 condor condor 410 May  2 10:52 ospool.token
drwxr-xr-x. 6 root   root   160 May  2 11:52 ..
-rw-------. 1 condor condor 236 May  2 12:14 nsgosg.token
drwx------. 2 root   root    46 May  2 12:14 .
[mkandes@nsgosg ~]$ sudo chown -R root:root /etc/condor/tokens.d
[sudo] password for mkandes: 
Duo two-factor login for mkandes

Enter a passcode or select one of the following options:

 1. Duo Push to XXX-XXX-7242
 2. SMS passcodes to XXX-XXX-7242

Passcode or option (1-2): 1

Please open Duo Mobile and check for Duo Push requests manually.
Success. Logging you in...
[mkandes@nsgosg ~]$ sudo ls -lahtr /etc/condor/tokens.d
total 8.0K
-rw-------. 1 root root 410 May  2 10:52 ospool.token
drwxr-xr-x. 6 root root 160 May  2 11:52 ..
-rw-------. 1 root root 236 May  2 12:14 nsgosg.token
drwx------. 2 root root  46 May  2 12:14 .
[mkandes@nsgosg ~]$
```

Still not a fix. Let's then try a fresh install with the latest version of HTCondor. Before we begin, let's make sure we have a copy of the tokens.

```
[mkandes@nsgosg ~]$ md5sum ospool.token 
490ad3f9ab57f5d6e2e03937709abb0c  ospool.token
[mkandes@nsgosg ~]$ sudo md5sum /etc/condor/tokens.d/ospool.token
[sudo] password for mkandes: 
Duo two-factor login for mkandes

Enter a passcode or select one of the following options:

 1. Duo Push to XXX-XXX-7242
 2. SMS passcodes to XXX-XXX-7242

Passcode or option (1-2): 1

Please open Duo Mobile and check for Duo Push requests manually.
Please open Duo Mobile and check for Duo Push requests manually.
Success. Logging you in...
490ad3f9ab57f5d6e2e03937709abb0c  /etc/condor/tokens.d/ospool.token
[mkandes@nsgosg ~]$
[mkandes@nsgosg ~]$ md5sum nsgosg.token 
ca30187991677bf2d335bbffbbfc25f5  nsgosg.token
[mkandes@nsgosg ~]$ sudo md5sum /etc/condor/tokens.d/nsgosg.token
ca30187991677bf2d335bbffbbfc25f5  /etc/condor/tokens.d/nsgosg.token
[mkandes@nsgosg ~]$
```

Other than that, I don't think we'll need any additional information about the current configuration saved. However, let's backup the `config.d` directory for comparison with the fresh install.

```
[mkandes@nsgosg ~]$ condor_config_val -summary > saved_condor_config_before_upgrade.20230817
[mkandes@nsgosg ~]$ sudo cp /etc/condor/
condor_config                           known_hosts
condor_ssh_to_job_sshd_config_template  passwords.d/
config.d/                               tokens.d/
ganglia.d/                              
[mkandes@nsgosg ~]$ sudo cp -rp /etc/condor/config.d/  ./
[sudo] password for mkandes: 
Duo two-factor login for mkandes

Enter a passcode or select one of the following options:

 1. Duo Push to XXX-XXX-7242
 2. SMS passcodes to XXX-XXX-7242

Passcode or option (1-2): 1

Please open Duo Mobile and check for Duo Push requests manually.
Success. Logging you in...
cp: cannot create directory './config.d': Permission denied
[mkandes@nsgosg ~]$ sudo cp -rp /etc/condor/config.d/  /tmp
[mkandes@nsgosg ~]$ ls -lahtr
total 2.2M
-rw-r--r--. 1 mkandes sdsc 3.4K Dec 18  2013 .login
-rw-r--r--. 1 mkandes sdsc 2.9K Dec 18  2013 .cshrc
-rw-------. 1 mkandes sdsc 119K May 11  2015 .mysql_history
drwxr-xr-x. 4 root    root   37 Dec 10  2020 ..
-rw-r--r--. 1 mkandes sdsc 1.5K Dec 15  2020 bash_pi.sh
drwxr-sr-x. 6 mkandes sdsc    8 Nov 29  2021 nsg-developer-env
-rw-r--r--. 1 mkandes sdsc   75 Nov 29  2021 .gitconfig
drwx--S---. 3 mkandes sdsc    3 Nov 29  2021 .config
drwxr-sr-x. 2 mkandes sdsc    5 Nov 29  2021 job_work_dir
-rw-r--r--. 1 mkandes sdsc 3.2K Nov 29  2021 inputfile
-rw-r--r--. 1 mkandes sdsc  503 Jun  7  2022 .bashrc
drwx--S---. 2 mkandes sdsc    4 Jun 23  2022 .ssh
-rw-r--r--. 1 mkandes sdsc  494 Aug  2  2022 bash_pi.htcondor
-rw-r--r--. 1 mkandes sdsc 2.4K Feb 21 10:59 saved_condor_config_before_upgrade.20230221
-rwxr-xr-x. 1 mkandes sdsc  42K Feb 21 11:59 .gwms-user-job-wrapper.sh
-rw-------. 1 mkandes sdsc 1.7K Feb 22 07:56 nsgosg.sdsc.edu-key.pem
-rw-------. 1 mkandes sdsc 1.1K Feb 22 07:56 nsgosg.sdsc.edu.req
-rw-r--r--. 1 mkandes sdsc 2.3K Feb 22 13:09 nsgosg.sdsc.edu-cert.pem
-rw-------. 1 mkandes sdsc   44 Feb 28 09:21 .lesshst
-rw-r--r--. 1 mkandes sdsc  410 May  2 10:40 ospool.token
-rw-r--r--. 1 mkandes sdsc 2.7K May  2 11:40 saved_condor_config_before_upgrade.20230502
-rw-r--r--. 1 mkandes sdsc  236 May  2 12:13 nsgosg.token
-rw-r--r--. 1 mkandes sdsc 4.1K May  2 14:14 condor_config
-rw-r--r--. 1 mkandes sdsc   50 May  2 14:18 99-local.conf
drwxr-sr-x. 2 mkandes sdsc    3 May  2 14:19 .condor
-rw-------. 1 mkandes sdsc  28K Jul 28 11:00 .bash_history
-rw-------. 1 mkandes sdsc  16K Aug 17 09:58 .viminfo
drwxr-sr-x. 7 mkandes sdsc   29 Aug 17 12:39 .
-rw-r--r--. 1 mkandes sdsc 3.1K Aug 17 12:39 saved_condor_config_before_upgrade.20230817
[mkandes@nsgosg ~]$ sudo chown -R mkandes:sdsc /tmp/config.d/
[mkandes@nsgosg ~]$ cp -rp /tmp/config.d/ ./
[mkandes@nsgosg ~]$ ls -lahtr
total 2.2M
-rw-r--r--. 1 mkandes sdsc 3.4K Dec 18  2013 .login
-rw-r--r--. 1 mkandes sdsc 2.9K Dec 18  2013 .cshrc
-rw-------. 1 mkandes sdsc 119K May 11  2015 .mysql_history
drwxr-xr-x. 4 root    root   37 Dec 10  2020 ..
-rw-r--r--. 1 mkandes sdsc 1.5K Dec 15  2020 bash_pi.sh
drwxr-sr-x. 6 mkandes sdsc    8 Nov 29  2021 nsg-developer-env
-rw-r--r--. 1 mkandes sdsc   75 Nov 29  2021 .gitconfig
drwx--S---. 3 mkandes sdsc    3 Nov 29  2021 .config
drwxr-sr-x. 2 mkandes sdsc    5 Nov 29  2021 job_work_dir
-rw-r--r--. 1 mkandes sdsc 3.2K Nov 29  2021 inputfile
-rw-r--r--. 1 mkandes sdsc  503 Jun  7  2022 .bashrc
drwx--S---. 2 mkandes sdsc    4 Jun 23  2022 .ssh
-rw-r--r--. 1 mkandes sdsc  494 Aug  2  2022 bash_pi.htcondor
-rw-r--r--. 1 mkandes sdsc 2.4K Feb 21 10:59 saved_condor_config_before_upgrade.20230221
-rwxr-xr-x. 1 mkandes sdsc  42K Feb 21 11:59 .gwms-user-job-wrapper.sh
-rw-------. 1 mkandes sdsc 1.7K Feb 22 07:56 nsgosg.sdsc.edu-key.pem
-rw-------. 1 mkandes sdsc 1.1K Feb 22 07:56 nsgosg.sdsc.edu.req
-rw-r--r--. 1 mkandes sdsc 2.3K Feb 22 13:09 nsgosg.sdsc.edu-cert.pem
-rw-------. 1 mkandes sdsc   44 Feb 28 09:21 .lesshst
-rw-r--r--. 1 mkandes sdsc  410 May  2 10:40 ospool.token
-rw-r--r--. 1 mkandes sdsc 2.7K May  2 11:40 saved_condor_config_before_upgrade.20230502
-rw-r--r--. 1 mkandes sdsc  236 May  2 12:13 nsgosg.token
-rw-r--r--. 1 mkandes sdsc 4.1K May  2 14:14 condor_config
-rw-r--r--. 1 mkandes sdsc   50 May  2 14:18 99-local.conf
drwxr-sr-x. 2 mkandes sdsc    3 May  2 14:19 .condor
-rw-------. 1 mkandes sdsc  28K Jul 28 11:00 .bash_history
-rw-------. 1 mkandes sdsc  16K Aug 17 09:58 .viminfo
drwxr-xr-x. 2 mkandes sdsc    9 Aug 17 11:15 config.d
-rw-r--r--. 1 mkandes sdsc 3.1K Aug 17 12:39 saved_condor_config_before_upgrade.20230817
drwxr-sr-x. 8 mkandes sdsc   30 Aug 17 12:41 .
[mkandes@nsgosg ~]$
```

Let's first take an inventory of the repos enabled and packages installed via OSG.

```
[mkandes@nsgosg ~]$ yum repolist
repo id                                                    repo name
SDSC-AppStream                                             Rocky Linux 8 AppStream
SDSC-BaseOS                                                Rocky Linux 8 BaseOS
SDSC-extras                                                Rocky Linux 8 extras
duosecurity                                                Duo Security Repository
epel                                                       Extra Packages for Enterprise Linux 8 - x86_64
osg                                                        OSG Software for Enterprise Linux 8 - x86_64
[mkandes@nsgosg ~]$
```

```
[mkandes@nsgosg ~]$ yum list | grep osg
condor.x86_64                                                     10.4.0-1.osg36up.el8                                       @osg-upcoming  
condor-blahp.x86_64                                               10.4.0-1.osg36up.el8                                       @osg-upcoming  
condor-classads.x86_64                                            10.4.0-1.osg36up.el8                                       @osg-upcoming  
condor-procd.x86_64                                               10.4.0-1.osg36up.el8                                       @osg-upcoming  
condor-stash-plugin.x86_64                                        6.12.1-1.osg36.el8                                         @osg           
gratia-probe-common.noarch                                        2.8.4-1.osg36.el8                                          @osg           
gratia-probe-condor-ap.noarch                                     2.8.4-1.osg36.el8                                          @osg           
igtf-ca-certs.noarch                                              1.122-1.osg36.el8                                          @osg           
osg-flock.noarch                                                  1.9-2.osg36.el8                                            @osg           
osg-pki-tools.noarch                                              3.5.2-1.osg36.el8                                          @osg           
osg-release.noarch                                                3.6-11.osg36.el8                                           @osg           
osg-xrootd.noarch                                                 3.6-20.osg36.el8                                           @osg           
python3-condor.x86_64                                             10.4.0-1.osg36up.el8                                       @osg-upcoming  
python3-xrootd.x86_64                                             1:5.5.5-1.2.osg36.el8                                      @osg           
stash-origin.x86_64                                               3.5.0-2.osg36.el8                                          @osg           
vo-client.noarch                                                  131-1.osg36.el8                                            @osg           
voms.x86_64                                                       2.1.0-0.14.rc2.6.osg36.el8                                 @osg           
voms-clients-cpp.x86_64                                           2.1.0-0.14.rc2.6.osg36.el8                                 @osg           
xcache.x86_64                                                     3.5.0-2.osg36.el8                                          @osg           
xrootd.x86_64                                                     1:5.5.5-1.2.osg36.el8                                      @osg           
xrootd-client.x86_64                                              1:5.5.5-1.2.osg36.el8                                      @osg           
xrootd-client-libs.x86_64                                         1:5.5.5-1.2.osg36.el8                                      @osg           
xrootd-libs.x86_64                                                1:5.5.5-1.2.osg36.el8                                      @osg           
xrootd-scitokens.x86_64                                           1:5.5.5-1.2.osg36.el8                                      @osg           
xrootd-selinux.noarch                                             1:5.5.5-1.2.osg36.el8                                      @osg           
xrootd-server.x86_64                                              1:5.5.5-1.2.osg36.el8                                      @osg           
xrootd-server-libs.x86_64                                         1:5.5.5-1.2.osg36.el8                                      @osg           
xrootd-voms.x86_64                                                1:5.5.5-1.2.osg36.el8                                      @osg           
atlas-xcache.x86_64                                               3.5.0-2.osg36.el8                                          osg            
blahp.x86_64                                                      2.2.1-1.osg36.el8                                          osg            
blahp-debugsource.x86_64                                          2.2.1-1.osg36.el8                                          osg            
cigetcert.noarch                                                  1.21-1.osg36.el8                                           osg            
cilogon-openid-ca-cert.noarch                                     1.1-5.osg36.el8                                            osg            
cms-xcache.x86_64                                                 3.5.0-2.osg36.el8                                          osg            
condor-all.x86_64                                                 10.0.7-1.osg36.el8                                         osg            
condor-annex-ec2.x86_64                                           10.0.7-1.osg36.el8                                         osg            
condor-bosco.x86_64                                               9.0.17-3.osg36.el8                                         osg            
condor-classads-devel.x86_64                                      10.0.7-1.osg36.el8                                         osg            
condor-credmon-oauth.x86_64                                       10.0.7-1.osg36.el8                                         osg            
condor-credmon-vault.x86_64                                       10.0.7-1.osg36.el8                                         osg            
condor-debugsource.x86_64                                         10.0.7-1.osg36.el8                                         osg            
condor-devel.x86_64                                               10.0.7-1.osg36.el8                                         osg            
condor-kbdd.x86_64                                                10.0.7-1.osg36.el8                                         osg            
condor-test.x86_64                                                10.0.7-1.osg36.el8                                         osg            
condor-upgrade-checks.x86_64                                      10.0.7-1.osg36.el8                                         osg            
condor-vm-gahp.x86_64                                             10.0.7-1.osg36.el8                                         osg            
cvmfs.x86_64                                                      2.10.1-1.2.osg36.el8                                       osg            
cvmfs-config-osg.noarch                                           2.5-2.osg36.el8                                            osg            
cvmfs-devel.x86_64                                                2.10.1-1.2.osg36.el8                                       osg            
cvmfs-ducc.x86_64                                                 2.10.1-1.2.osg36.el8                                       osg            
cvmfs-fuse3.x86_64                                                2.10.1-1.2.osg36.el8                                       osg            
cvmfs-gateway.x86_64                                              2.10.1-1.2.osg36.el8                                       osg            
cvmfs-libs.x86_64                                                 2.10.1-1.2.osg36.el8                                       osg            
cvmfs-server.x86_64                                               2.10.1-1.2.osg36.el8                                       osg            
cvmfs-shrinkwrap.x86_64                                           2.10.1-1.2.osg36.el8                                       osg            
cvmfs-unittests.x86_64                                            2.10.1-1.2.osg36.el8                                       osg            
cvmfs-x509-helper.x86_64                                          2.2-2.osg36.el8                                            osg            
cvmfs-x509-helper-debugsource.x86_64                              2.2-2.osg36.el8                                            osg            
frontier-squid.x86_64                                             11:5.9-1.1.osg36.el8                                       osg            
glideinwms-common-tools.noarch                                    3.10.1-1.osg36.el8                                         osg            
glideinwms-condor-common-config.noarch                            3.10.1-1.osg36.el8                                         osg            
glideinwms-factory.noarch                                         3.10.1-1.osg36.el8                                         osg            
glideinwms-factory-condor.noarch                                  3.10.1-1.osg36.el8                                         osg            
glideinwms-factory-core.noarch                                    3.10.1-1.osg36.el8                                         osg            
glideinwms-factory-httpd.noarch                                   3.10.1-1.osg36.el8                                         osg            
glideinwms-glidecondor-tools.noarch                               3.10.1-1.osg36.el8                                         osg            
glideinwms-libs.noarch                                            3.10.1-1.osg36.el8                                         osg            
glideinwms-minimal-condor.noarch                                  3.10.1-1.osg36.el8                                         osg            
glideinwms-usercollector.noarch                                   3.10.1-1.osg36.el8                                         osg            
glideinwms-userschedd.noarch                                      3.10.1-1.osg36.el8                                         osg            
glideinwms-vofrontend.noarch                                      3.10.1-1.osg36.el8                                         osg            
glideinwms-vofrontend-core.noarch                                 3.10.1-1.osg36.el8                                         osg            
glideinwms-vofrontend-glidein.noarch                              3.10.1-1.osg36.el8                                         osg            
glideinwms-vofrontend-httpd.noarch                                3.10.1-1.osg36.el8                                         osg            
glideinwms-vofrontend-libs.noarch                                 3.10.1-1.osg36.el8                                         osg            
glideinwms-vofrontend-standalone.noarch                           3.10.1-1.osg36.el8                                         osg            
gratia-probe-condor.noarch                                        2.8.4-1.osg36.el8                                          osg            
gratia-probe-dcache-storagegroup.noarch                           2.8.4-1.osg36.el8                                          osg            
gratia-probe-dcache-transfer.noarch                               2.8.4-1.osg36.el8                                          osg            
gratia-probe-enstore-storage.noarch                               2.8.4-1.osg36.el8                                          osg            
gratia-probe-enstore-tapedrive.noarch                             2.8.4-1.osg36.el8                                          osg            
gratia-probe-enstore-transfer.noarch                              2.8.4-1.osg36.el8                                          osg            
gratia-probe-htcondor-ce.noarch                                   2.8.4-1.osg36.el8                                          osg            
gratia-probe-lsf.noarch                                           2.8.4-1.osg36.el8                                          osg            
gratia-probe-onevm.noarch                                         2.8.4-1.osg36.el8                                          osg            
gratia-probe-osg-pilot-container.noarch                           2.8.4-1.osg36.el8                                          osg            
gratia-probe-pbs-lsf.noarch                                       2.8.4-1.osg36.el8                                          osg            
gratia-probe-services.noarch                                      2.8.4-1.osg36.el8                                          osg            
gratia-probe-sge.noarch                                           2.8.4-1.osg36.el8                                          osg            
gratia-probe-slurm.noarch                                         2.8.4-1.osg36.el8                                          osg            
gratia-probe-xrootd-transfer.noarch                               2.1.0-1.osg36.el8                                          osg            
hosted-ce-tools.noarch                                            1.0-4.osg36.el8                                            osg            
htcondor-ce.noarch                                                6.0.0-1.osg36.el8                                          osg            
htcondor-ce-bosco.noarch                                          6.0.0-1.osg36.el8                                          osg            
htcondor-ce-client.noarch                                         6.0.0-1.osg36.el8                                          osg            
htcondor-ce-collector.noarch                                      6.0.0-1.osg36.el8                                          osg            
htcondor-ce-condor.noarch                                         6.0.0-1.osg36.el8                                          osg            
htcondor-ce-lsf.noarch                                            6.0.0-1.osg36.el8                                          osg            
htcondor-ce-pbs.noarch                                            6.0.0-1.osg36.el8                                          osg            
htcondor-ce-sge.noarch                                            6.0.0-1.osg36.el8                                          osg            
htcondor-ce-slurm.noarch                                          6.0.0-1.osg36.el8                                          osg            
htcondor-ce-view.noarch                                           6.0.0-1.osg36.el8                                          osg            
htgettoken.x86_64                                                 1.18-1.osg36.el8                                           osg            
htvault-config.x86_64                                             1.15-1.osg36.el8                                           osg            
javascriptrrd.noarch                                              1.1.1-1.1.osg36.el8                                        osg            
liboidc-agent-devel.x86_64                                        4.2.4-1.1.osg36.el8                                        osg            
liboidc-agent4.x86_64                                             4.2.4-1.1.osg36.el8                                        osg            
minicondor.x86_64                                                 10.0.7-1.osg36.el8                                         osg            
oidc-agent.x86_64                                                 4.2.4-1.1.osg36.el8                                        osg            
oidc-agent-cli.x86_64                                             4.2.4-1.1.osg36.el8                                        osg            
oidc-agent-debugsource.x86_64                                     4.2.4-1.1.osg36.el8                                        osg            
oidc-agent-desktop.x86_64                                         4.2.4-1.1.osg36.el8                                        osg            
osg-ca-certs.noarch                                               1.113-1.osg36.el8                                          osg            
osg-ca-certs-updater.noarch                                       2.0-1.1.osg36.el8                                          osg            
osg-ca-scripts.noarch                                             1.2.4-2.osg36.el8                                          osg            
osg-ce.x86_64                                                     3.6-6.osg36.el8                                            osg            
osg-ce-attributes-generator.noarch                                4.1.1-1.osg36.el8                                          osg            
osg-ce-bosco.x86_64                                               3.6-6.osg36.el8                                            osg            
osg-ce-condor.x86_64                                              3.6-6.osg36.el8                                            osg            
osg-ce-lsf.x86_64                                                 3.6-6.osg36.el8                                            osg            
osg-ce-pbs.x86_64                                                 3.6-6.osg36.el8                                            osg            
osg-ce-sge.x86_64                                                 3.6-6.osg36.el8                                            osg            
osg-ce-slurm.x86_64                                               3.6-6.osg36.el8                                            osg            
osg-configure.noarch                                              4.1.1-1.osg36.el8                                          osg            
osg-configure-bosco.noarch                                        4.1.1-1.osg36.el8                                          osg            
osg-configure-ce.noarch                                           4.1.1-1.osg36.el8                                          osg            
osg-configure-cluster.noarch                                      4.1.1-1.osg36.el8                                          osg            
osg-configure-condor.noarch                                       4.1.1-1.osg36.el8                                          osg            
osg-configure-gateway.noarch                                      4.1.1-1.osg36.el8                                          osg            
osg-configure-gip.noarch                                          4.1.1-1.osg36.el8                                          osg            
osg-configure-gratia.noarch                                       4.1.1-1.osg36.el8                                          osg            
osg-configure-infoservices.noarch                                 4.1.1-1.osg36.el8                                          osg            
osg-configure-libs.noarch                                         4.1.1-1.osg36.el8                                          osg            
osg-configure-lsf.noarch                                          4.1.1-1.osg36.el8                                          osg            
osg-configure-misc.noarch                                         4.1.1-1.osg36.el8                                          osg            
osg-configure-pbs.noarch                                          4.1.1-1.osg36.el8                                          osg            
osg-configure-rsv.noarch                                          4.1.1-1.osg36.el8                                          osg            
osg-configure-sge.noarch                                          4.1.1-1.osg36.el8                                          osg            
osg-configure-siteinfo.noarch                                     4.1.1-1.osg36.el8                                          osg            
osg-configure-slurm.noarch                                        4.1.1-1.osg36.el8                                          osg            
osg-configure-squid.noarch                                        4.1.1-1.osg36.el8                                          osg            
osg-configure-tests.noarch                                        4.1.1-1.osg36.el8                                          osg            
osg-oasis.noarch                                                  19-3.osg36.el8                                             osg            
osg-scitokens-mapfile.x86_64                                      12-1.osg36.el8                                             osg            
osg-system-profiler.noarch                                        1.6.0-2.osg36.el8                                          osg            
osg-system-profiler-viewer.noarch                                 1.6.0-2.osg36.el8                                          osg            
osg-token-renewer.noarch                                          0.8.3-2.osg36.el8                                          osg            
osg-update-data.noarch                                            1.4.1-1.osg36.el8                                          osg            
osg-update-vos.noarch                                             1.4.1-1.osg36.el8                                          osg            
osg-wn-client.noarch                                              3.6-5.osg36.el8                                            osg            
osg-xrootd-standalone.noarch                                      3.6-20.osg36.el8                                           osg            
pegasus.x86_64                                                    5.0.1-1.1.osg36.el8                                        osg            
pegasus-debugsource.x86_64                                        5.0.1-1.1.osg36.el8                                        osg            
python3-scitokens.noarch                                          1.7.4-1.osg36.el8                                          osg            
python3-scitokens-credmon.noarch                                  0.8.1-1.3.osg36.el8                                        osg            
stash-cache.x86_64                                                3.5.0-2.osg36.el8                                          osg            
stashcache-client.noarch                                          6.1.0-1.osg36.el8                                          osg            
stashcp.x86_64                                                    6.12.1-1.osg36.el8                                         osg            
vault.x86_64                                                      1.13.2-1.osg36.el8                                         osg            
vo-client-dcache.noarch                                           131-1.osg36.el8                                            osg            
vo-client-lcmaps-voms.noarch                                      131-1.osg36.el8                                            osg            
voms-debugsource.x86_64                                           2.1.0-0.14.rc2.6.osg36.el8                                 osg            
voms-devel.x86_64                                                 2.1.0-0.14.rc2.6.osg36.el8                                 osg            
voms-doc.noarch                                                   2.1.0-0.14.rc2.6.osg36.el8                                 osg            
voms-server.x86_64                                                2.1.0-0.14.rc2.6.osg36.el8                                 osg            
xcache-consistency-check.x86_64                                   3.5.0-2.osg36.el8                                          osg            
xcache-redirector.x86_64                                          3.5.0-2.osg36.el8                                          osg            
xrdcl-http.x86_64                                                 1:5.5.5-1.2.osg36.el8                                      osg            
xrootd-client-compat.x86_64                                       1:5.5.5-1.2.osg36.el8                                      osg            
xrootd-client-devel.x86_64                                        1:5.5.5-1.2.osg36.el8                                      osg            
xrootd-debugsource.x86_64                                         1:5.5.5-1.2.osg36.el8                                      osg            
xrootd-devel.x86_64                                               1:5.5.5-1.2.osg36.el8                                      osg            
xrootd-doc.noarch                                                 1:5.5.5-1.2.osg36.el8                                      osg            
xrootd-fuse.x86_64                                                1:5.5.5-1.2.osg36.el8                                      osg            
xrootd-lcmaps.x86_64                                              99-1.osg36.el8                                             osg            
xrootd-monitoring-shoveler.x86_64                                 1.1.2-1.osg36.el8                                          osg            
xrootd-multiuser.x86_64                                           2.1.3-1.3.osg36.el8                                        osg            
xrootd-multiuser-debugsource.x86_64                               2.1.3-1.3.osg36.el8                                        osg            
xrootd-private-devel.x86_64                                       1:5.5.5-1.2.osg36.el8                                      osg            
xrootd-server-compat.x86_64                                       1:5.5.5-1.2.osg36.el8                                      osg            
xrootd-server-devel.x86_64                                        1:5.5.5-1.2.osg36.el8                                      osg            
xrootd-tcp-stats.x86_64                                           1.0.0-1.osg36.el8                                          osg            
xrootd-tcp-stats-debugsource.x86_64                               1.0.0-1.osg36.el8                                          osg            
[mkandes@nsgosg ~]$
```

Before uninstalling all OSG-related packages, let's make sure all related services are shutdown.

```
[mkandes@nsgosg ~]$ sudo systemctl status gratia-probes-cron
[sudo] password for mkandes: 
Duo two-factor login for mkandes

Enter a passcode or select one of the following options:

 1. Duo Push to XXX-XXX-7242
 2. SMS passcodes to XXX-XXX-7242

Passcode or option (1-2): 1

Please open Duo Mobile and check for Duo Push requests manually.
Please open Duo Mobile and check for Duo Push requests manually.
Success. Logging you in...
● gratia-probes-cron.service - SYSV: Enable specified gratia probes to run via cron. based on fetch-crl-cron script (Steve Traylen <steve.traylen@cer>
   Loaded: loaded (/etc/rc.d/init.d/gratia-probes-cron; generated)
   Active: inactive (dead)
     Docs: man:systemd-sysv-generator(8)
```

```
[mkandes@nsgosg ~]$ sudo systemctl stop condor
[mkandes@nsgosg ~]$ sudo systemctl status condor
● condor.service - Condor Distributed High-Throughput-Computing
   Loaded: loaded (/usr/lib/systemd/system/condor.service; enabled; vendor preset: disabled)
  Drop-In: /usr/lib/systemd/system/condor.service.d
           └─osg-env.conf
   Active: inactive (dead) since Thu 2023-08-17 14:56:42 PDT; 3s ago
  Process: 75328 ExecStart=/usr/sbin/condor_master -f (code=exited, status=0/SUCCESS)
 Main PID: 75328 (code=exited, status=0/SUCCESS)
   Status: "All daemons are responding"

Aug 17 11:49:21 nsgosg.sdsc.edu systemd[1]: condor.service: Succeeded.
Aug 17 11:49:21 nsgosg.sdsc.edu systemd[1]: Stopped Condor Distributed High-Throughput-Computing.
Aug 17 11:49:21 nsgosg.sdsc.edu systemd[1]: Started Condor Distributed High-Throughput-Computing.
Aug 17 14:56:41 nsgosg.sdsc.edu systemd[1]: Stopping Condor Distributed High-Throughput-Computing...
Aug 17 14:56:42 nsgosg.sdsc.edu systemd[1]: condor.service: Succeeded.
Aug 17 14:56:42 nsgosg.sdsc.edu systemd[1]: Stopped Condor Distributed High-Throughput-Computing.
[mkandes@nsgosg ~]$
```

Now removing OSG packages ...

```
[mkandes@nsgosg ~]$ sudo dnf repository-packages osg remove
Dependencies resolved.
======================================================================================================================================================
 Package                               Architecture         Version                                               Repository                     Size
======================================================================================================================================================
Removing:
 condor-stash-plugin                   x86_64               6.12.1-1.osg36.el8                                    @osg                          6.2 M
 gratia-probe-common                   noarch               2.8.4-1.osg36.el8                                     @osg                          651 k
 gratia-probe-condor-ap                noarch               2.8.4-1.osg36.el8                                     @osg                          5.8 k
 igtf-ca-certs                         noarch               1.122-1.osg36.el8                                     @osg                          364 k
 osg-flock                             noarch               1.9-2.osg36.el8                                       @osg                          1.2 k
 osg-pki-tools                         noarch               3.5.2-1.osg36.el8                                     @osg                           66 k
 osg-release                           noarch               3.6-11.osg36.el8                                      @osg                           15 k
 osg-xrootd                            noarch               3.6-20.osg36.el8                                      @osg                          7.0 k
 python3-xrootd                        x86_64               1:5.5.5-1.2.osg36.el8                                 @osg                          494 k
 stash-origin                          x86_64               3.5.0-2.osg36.el8                                     @osg                           12 k
 vo-client                             noarch               131-1.osg36.el8                                       @osg                           16 k
 voms                                  x86_64               2.1.0-0.14.rc2.6.osg36.el8                            @osg                          440 k
 voms-clients-cpp                      x86_64               2.1.0-0.14.rc2.6.osg36.el8                            @osg                          651 k
 xcache                                x86_64               3.5.0-2.osg36.el8                                     @osg                           32 k
 xrootd                                x86_64               1:5.5.5-1.2.osg36.el8                                 @osg                            0  
 xrootd-client                         x86_64               1:5.5.5-1.2.osg36.el8                                 @osg                          964 k
 xrootd-client-libs                    x86_64               1:5.5.5-1.2.osg36.el8                                 @osg                          2.8 M
 xrootd-libs                           x86_64               1:5.5.5-1.2.osg36.el8                                 @osg                          2.1 M
 xrootd-scitokens                      x86_64               1:5.5.5-1.2.osg36.el8                                 @osg                          117 k
 xrootd-selinux                        noarch               1:5.5.5-1.2.osg36.el8                                 @osg                           82 k
 xrootd-server                         x86_64               1:5.5.5-1.2.osg36.el8                                 @osg                          1.2 M
 xrootd-server-libs                    x86_64               1:5.5.5-1.2.osg36.el8                                 @osg                          2.4 M
 xrootd-voms                           x86_64               1:5.5.5-1.2.osg36.el8                                 @osg                           85 k
Removing dependent packages:
 condor                                x86_64               10.4.0-1.osg36up.el8                                  @osg-upcoming                  25 M
Removing unused dependencies:
 condor-blahp                          x86_64               10.4.0-1.osg36up.el8                                  @osg-upcoming                 1.4 M
 condor-classads                       x86_64               10.4.0-1.osg36up.el8                                  @osg-upcoming                 805 k
 condor-procd                          x86_64               10.4.0-1.osg36up.el8                                  @osg-upcoming                 307 k
 expect                                x86_64               5.45.4-5.el8                                          @SDSC-BaseOS                  569 k
 fetch-crl                             noarch               3.0.22-1.el8                                          @epel                         137 k
 libcgroup                             x86_64               0.41-19.el8                                           @baseos                       134 k
 libicu                                x86_64               60.3-2.el8_1                                          @baseos                        31 M
 libmacaroons                          x86_64               0.3.0-6.el8                                           @epel                          64 k
 libsodium                             x86_64               1.0.18-2.el8                                          @epel                         399 k
 mailcap                               noarch               2.1.48-3.el8                                          @baseos                        71 k
 munge-libs                            x86_64               0.5.13-2.el8                                          @appstream                     41 k
 net-tools                             x86_64               2.0-0.52.20160912git.el8                              @baseos                       942 k
 perl-Data-Dump                        noarch               1.23-7.module+el8.6.0+965+850557f9                    @SDSC-AppStream                50 k
 perl-Digest-HMAC                      noarch               1.03-17.module+el8.6.0+965+850557f9                   @SDSC-AppStream                11 k
 perl-File-Listing                     noarch               6.04-17.module+el8.6.0+965+850557f9                   @SDSC-AppStream                16 k
 perl-HTML-Parser                      x86_64               3.72-15.module+el8.6.0+965+850557f9                   @SDSC-AppStream               223 k
 perl-HTML-Tagset                      noarch               3.20-34.module+el8.6.0+965+850557f9                   @SDSC-AppStream                19 k
 perl-HTTP-Cookies                     noarch               6.04-2.module+el8.6.0+965+850557f9                    @SDSC-AppStream                68 k
 perl-HTTP-Date                        noarch               6.02-19.module+el8.6.0+965+850557f9                   @SDSC-AppStream                19 k
 perl-HTTP-Message                     noarch               6.18-1.module+el8.6.0+965+850557f9                    @SDSC-AppStream               204 k
 perl-HTTP-Negotiate                   noarch               6.01-19.module+el8.6.0+965+850557f9                   @SDSC-AppStream                28 k
 perl-IO-HTML                          noarch               1.001-11.module+el8.6.0+965+850557f9                  @SDSC-AppStream                42 k
 perl-LWP-MediaTypes                   noarch               6.02-15.module+el8.6.0+965+850557f9                   @SDSC-AppStream                61 k
 perl-LWP-Protocol-https               noarch               6.07-4.module+el8.6.0+965+850557f9                    @SDSC-AppStream                12 k
 perl-NTLM                             noarch               1.09-17.module+el8.6.0+965+850557f9                   @SDSC-AppStream                31 k
 perl-Net-HTTP                         noarch               6.17-2.module+el8.6.0+965+850557f9                    @SDSC-AppStream                75 k
 perl-TimeDate                         noarch               1:2.30-15.module+el8.6.0+965+850557f9                 @SDSC-AppStream                94 k
 perl-Try-Tiny                         noarch               0.30-7.module+el8.6.0+965+850557f9                    @SDSC-AppStream                65 k
 perl-WWW-RobotRules                   noarch               6.02-18.module+el8.6.0+965+850557f9                   @SDSC-AppStream                25 k
 perl-libwww-perl                      noarch               6.34-1.module+el8.6.0+965+850557f9                    @SDSC-AppStream               505 k
 postfix                               x86_64               2:3.5.8-4.el8                                         @SDSC-BaseOS                  4.3 M
 python3-chardet                       noarch               3.0.4-7.el8                                           @baseos                       904 k
 python3-condor                        x86_64               10.4.0-1.osg36up.el8                                  @osg-upcoming                 3.4 M
 python3-idna                          noarch               2.5-5.el8                                             @baseos                       509 k
 python3-m2crypto                      x86_64               0.35.2-5.el8                                          @epel                         1.4 M
 python3-pysocks                       noarch               1.6.8-3.el8                                           @baseos                        75 k
 python3-requests                      noarch               2.20.0-2.1.el8_1                                      @baseos                       369 k
 python3-urllib3                       noarch               1.24.2-5.el8                                          @baseos                       606 k
 scitokens-cpp                         x86_64               1.0.2-1.el8                                           @epel                         414 k
 tcl                                   x86_64               1:8.6.8-2.el8                                         @SDSC-BaseOS                  4.4 M

Transaction Summary
======================================================================================================================================================
Remove  64 Packages

Freed space: 97 M
Is this ok [y/N]:y
Running transaction check
Transaction check succeeded.
Running transaction test
Transaction test succeeded.
Running transaction
  Preparing        :                                                                                                                              1/1 
  Running scriptlet: stash-origin-3.5.0-2.osg36.el8.x86_64                                                                                        1/1 
  Running scriptlet: stash-origin-3.5.0-2.osg36.el8.x86_64                                                                                       1/64 
  Erasing          : stash-origin-3.5.0-2.osg36.el8.x86_64                                                                                       1/64 
  Running scriptlet: stash-origin-3.5.0-2.osg36.el8.x86_64                                                                                       1/64 
  Running scriptlet: xcache-3.5.0-2.osg36.el8.x86_64                                                                                             2/64 
  Erasing          : xcache-3.5.0-2.osg36.el8.x86_64                                                                                             2/64 
  Running scriptlet: xcache-3.5.0-2.osg36.el8.x86_64                                                                                             2/64 
  Erasing          : osg-xrootd-3.6-20.osg36.el8.noarch                                                                                          3/64 
warning: /etc/xrootd/config.d/10-common-site-local.cfg saved as /etc/xrootd/config.d/10-common-site-local.cfg.rpmsave

  Running scriptlet: fetch-crl-3.0.22-1.el8.noarch                                                                                               4/64 
  Erasing          : fetch-crl-3.0.22-1.el8.noarch                                                                                               4/64 
  Running scriptlet: fetch-crl-3.0.22-1.el8.noarch                                                                                               4/64 
  Erasing          : perl-LWP-Protocol-https-6.07-4.module+el8.6.0+965+850557f9.noarch                                                           5/64 
  Erasing          : perl-libwww-perl-6.34-1.module+el8.6.0+965+850557f9.noarch                                                                  6/64 
  Erasing          : perl-HTTP-Cookies-6.04-2.module+el8.6.0+965+850557f9.noarch                                                                 7/64 
  Erasing          : xrootd-1:5.5.5-1.2.osg36.el8.x86_64                                                                                         8/64 
  Erasing          : osg-flock-1.9-2.osg36.el8.noarch                                                                                            9/64 
  Erasing          : gratia-probe-condor-ap-2.8.4-1.osg36.el8.noarch                                                                            10/64 
warning: /etc/gratia/condor-ap/ProbeConfig saved as /etc/gratia/condor-ap/ProbeConfig.rpmsave

  Erasing          : perl-NTLM-1.09-17.module+el8.6.0+965+850557f9.noarch                                                                       11/64 
  Erasing          : perl-File-Listing-6.04-17.module+el8.6.0+965+850557f9.noarch                                                               12/64 
  Erasing          : perl-HTTP-Negotiate-6.01-19.module+el8.6.0+965+850557f9.noarch                                                             13/64 
  Erasing          : vo-client-131-1.osg36.el8.noarch                                                                                           14/64 
  Erasing          : osg-pki-tools-3.5.2-1.osg36.el8.noarch                                                                                     15/64 
  Erasing          : igtf-ca-certs-1.122-1.osg36.el8.noarch                                                                                     16/64 
  Erasing          : perl-Digest-HMAC-1.03-17.module+el8.6.0+965+850557f9.noarch                                                                17/64 
  Erasing          : gratia-probe-common-2.8.4-1.osg36.el8.noarch                                                                               18/64 
  Erasing          : xrootd-selinux-1:5.5.5-1.2.osg36.el8.noarch                                                                                19/64 
  Running scriptlet: xrootd-selinux-1:5.5.5-1.2.osg36.el8.noarch                                                                                19/64 
  Erasing          : perl-Data-Dump-1.23-7.module+el8.6.0+965+850557f9.noarch                                                                   20/64 
  Erasing          : perl-Net-HTTP-6.17-2.module+el8.6.0+965+850557f9.noarch                                                                    21/64 
  Erasing          : perl-Try-Tiny-0.30-7.module+el8.6.0+965+850557f9.noarch                                                                    22/64 
  Erasing          : perl-WWW-RobotRules-6.02-18.module+el8.6.0+965+850557f9.noarch                                                             23/64 
  Erasing          : osg-release-3.6-11.osg36.el8.noarch                                                                                        24/64 
  Erasing          : python3-condor-10.4.0-1.osg36up.el8.x86_64                                                                                 25/64 
  Running scriptlet: condor-10.4.0-1.osg36up.el8.x86_64                                                                                         26/64 
  Erasing          : condor-10.4.0-1.osg36up.el8.x86_64                                                                                         26/64 
warning: /etc/condor/config.d/00-htcondor-9.0.config saved as /etc/condor/config.d/00-htcondor-9.0.config.rpmsave

  Running scriptlet: condor-10.4.0-1.osg36up.el8.x86_64                                                                                         26/64 
  Erasing          : condor-procd-10.4.0-1.osg36up.el8.x86_64                                                                                   27/64 
  Erasing          : xrootd-client-1:5.5.5-1.2.osg36.el8.x86_64                                                                                 28/64 
  Erasing          : xrootd-scitokens-1:5.5.5-1.2.osg36.el8.x86_64                                                                              29/64 
  Erasing          : python3-requests-2.20.0-2.1.el8_1.noarch                                                                                   30/64 
  Running scriptlet: xrootd-server-1:5.5.5-1.2.osg36.el8.x86_64                                                                                 31/64 
  Erasing          : xrootd-server-1:5.5.5-1.2.osg36.el8.x86_64                                                                                 31/64 
  Running scriptlet: xrootd-server-1:5.5.5-1.2.osg36.el8.x86_64                                                                                 31/64 
  Erasing          : xrootd-server-libs-1:5.5.5-1.2.osg36.el8.x86_64                                                                            32/64 
  Running scriptlet: xrootd-server-libs-1:5.5.5-1.2.osg36.el8.x86_64                                                                            32/64 
  Running scriptlet: postfix-2:3.5.8-4.el8.x86_64                                                                                               33/64 
  Erasing          : postfix-2:3.5.8-4.el8.x86_64                                                                                               33/64 
warning: /etc/postfix/main.cf saved as /etc/postfix/main.cf.rpmsave

  Running scriptlet: postfix-2:3.5.8-4.el8.x86_64                                                                                               33/64 
  Erasing          : xrootd-voms-1:5.5.5-1.2.osg36.el8.x86_64                                                                                   34/64 
  Erasing          : python3-xrootd-1:5.5.5-1.2.osg36.el8.x86_64                                                                                35/64 
  Erasing          : xrootd-client-libs-1:5.5.5-1.2.osg36.el8.x86_64                                                                            36/64 
  Running scriptlet: xrootd-client-libs-1:5.5.5-1.2.osg36.el8.x86_64                                                                            36/64 
  Erasing          : perl-HTML-Parser-3.72-15.module+el8.6.0+965+850557f9.x86_64                                                                37/64 
  Erasing          : perl-HTTP-Message-6.18-1.module+el8.6.0+965+850557f9.noarch                                                                38/64 
  Erasing          : voms-clients-cpp-2.1.0-0.14.rc2.6.osg36.el8.x86_64                                                                         39/64 
  Running scriptlet: voms-clients-cpp-2.1.0-0.14.rc2.6.osg36.el8.x86_64                                                                         39/64 
  Erasing          : perl-HTTP-Date-6.02-19.module+el8.6.0+965+850557f9.noarch                                                                  40/64 
  Erasing          : perl-LWP-MediaTypes-6.02-15.module+el8.6.0+965+850557f9.noarch                                                             41/64 
  Erasing          : python3-urllib3-1.24.2-5.el8.noarch                                                                                        42/64 
  Erasing          : python3-pysocks-1.6.8-3.el8.noarch                                                                                         43/64 
  Erasing          : mailcap-2.1.48-3.el8.noarch                                                                                                44/64 
  Erasing          : perl-TimeDate-1:2.30-15.module+el8.6.0+965+850557f9.noarch                                                                 45/64 
  Erasing          : perl-IO-HTML-1.001-11.module+el8.6.0+965+850557f9.noarch                                                                   46/64 
  Erasing          : perl-HTML-Tagset-3.20-34.module+el8.6.0+965+850557f9.noarch                                                                47/64 
  Erasing          : python3-chardet-3.0.4-7.el8.noarch                                                                                         48/64 
  Erasing          : python3-idna-2.5-5.el8.noarch                                                                                              49/64 
  Erasing          : condor-stash-plugin-6.12.1-1.osg36.el8.x86_64                                                                              50/64 
  Erasing          : libmacaroons-0.3.0-6.el8.x86_64                                                                                            51/64 
  Erasing          : expect-5.45.4-5.el8.x86_64                                                                                                 52/64 
  Erasing          : tcl-1:8.6.8-2.el8.x86_64                                                                                                   53/64 
  Running scriptlet: tcl-1:8.6.8-2.el8.x86_64                                                                                                   53/64 
  Erasing          : libsodium-1.0.18-2.el8.x86_64                                                                                              54/64 
  Erasing          : voms-2.1.0-0.14.rc2.6.osg36.el8.x86_64                                                                                     55/64 
  Erasing          : xrootd-libs-1:5.5.5-1.2.osg36.el8.x86_64                                                                                   56/64 
  Running scriptlet: xrootd-libs-1:5.5.5-1.2.osg36.el8.x86_64                                                                                   56/64 
  Erasing          : libicu-60.3-2.el8_1.x86_64                                                                                                 57/64 
  Running scriptlet: libicu-60.3-2.el8_1.x86_64                                                                                                 57/64 
  Erasing          : scitokens-cpp-1.0.2-1.el8.x86_64                                                                                           58/64 
  Erasing          : libcgroup-0.41-19.el8.x86_64                                                                                               59/64 
  Running scriptlet: libcgroup-0.41-19.el8.x86_64                                                                                               59/64 
  Erasing          : condor-blahp-10.4.0-1.osg36up.el8.x86_64                                                                                   60/64 
  Erasing          : condor-classads-10.4.0-1.osg36up.el8.x86_64                                                                                61/64 
  Erasing          : munge-libs-0.5.13-2.el8.x86_64                                                                                             62/64 
  Erasing          : net-tools-2.0-0.52.20160912git.el8.x86_64                                                                                  63/64 
  Running scriptlet: net-tools-2.0-0.52.20160912git.el8.x86_64                                                                                  63/64 
  Erasing          : python3-m2crypto-0.35.2-5.el8.x86_64                                                                                       64/64 
  Running scriptlet: python3-m2crypto-0.35.2-5.el8.x86_64                                                                                       64/64 
  Verifying        : condor-10.4.0-1.osg36up.el8.x86_64                                                                                          1/64 
  Verifying        : condor-blahp-10.4.0-1.osg36up.el8.x86_64                                                                                    2/64 
  Verifying        : condor-classads-10.4.0-1.osg36up.el8.x86_64                                                                                 3/64 
  Verifying        : condor-procd-10.4.0-1.osg36up.el8.x86_64                                                                                    4/64 
  Verifying        : condor-stash-plugin-6.12.1-1.osg36.el8.x86_64                                                                               5/64 
  Verifying        : expect-5.45.4-5.el8.x86_64                                                                                                  6/64 
  Verifying        : fetch-crl-3.0.22-1.el8.noarch                                                                                               7/64 
  Verifying        : gratia-probe-common-2.8.4-1.osg36.el8.noarch                                                                                8/64 
  Verifying        : gratia-probe-condor-ap-2.8.4-1.osg36.el8.noarch                                                                             9/64 
  Verifying        : igtf-ca-certs-1.122-1.osg36.el8.noarch                                                                                     10/64 
  Verifying        : libcgroup-0.41-19.el8.x86_64                                                                                               11/64 
  Verifying        : libicu-60.3-2.el8_1.x86_64                                                                                                 12/64 
  Verifying        : libmacaroons-0.3.0-6.el8.x86_64                                                                                            13/64 
  Verifying        : libsodium-1.0.18-2.el8.x86_64                                                                                              14/64 
  Verifying        : mailcap-2.1.48-3.el8.noarch                                                                                                15/64 
  Verifying        : munge-libs-0.5.13-2.el8.x86_64                                                                                             16/64 
  Verifying        : net-tools-2.0-0.52.20160912git.el8.x86_64                                                                                  17/64 
  Verifying        : osg-flock-1.9-2.osg36.el8.noarch                                                                                           18/64 
  Verifying        : osg-pki-tools-3.5.2-1.osg36.el8.noarch                                                                                     19/64 
  Verifying        : osg-release-3.6-11.osg36.el8.noarch                                                                                        20/64 
  Verifying        : osg-xrootd-3.6-20.osg36.el8.noarch                                                                                         21/64 
  Verifying        : perl-Data-Dump-1.23-7.module+el8.6.0+965+850557f9.noarch                                                                   22/64 
  Verifying        : perl-Digest-HMAC-1.03-17.module+el8.6.0+965+850557f9.noarch                                                                23/64 
  Verifying        : perl-File-Listing-6.04-17.module+el8.6.0+965+850557f9.noarch                                                               24/64 
  Verifying        : perl-HTML-Parser-3.72-15.module+el8.6.0+965+850557f9.x86_64                                                                25/64 
  Verifying        : perl-HTML-Tagset-3.20-34.module+el8.6.0+965+850557f9.noarch                                                                26/64 
  Verifying        : perl-HTTP-Cookies-6.04-2.module+el8.6.0+965+850557f9.noarch                                                                27/64 
  Verifying        : perl-HTTP-Date-6.02-19.module+el8.6.0+965+850557f9.noarch                                                                  28/64 
  Verifying        : perl-HTTP-Message-6.18-1.module+el8.6.0+965+850557f9.noarch                                                                29/64 
  Verifying        : perl-HTTP-Negotiate-6.01-19.module+el8.6.0+965+850557f9.noarch                                                             30/64 
  Verifying        : perl-IO-HTML-1.001-11.module+el8.6.0+965+850557f9.noarch                                                                   31/64 
  Verifying        : perl-LWP-MediaTypes-6.02-15.module+el8.6.0+965+850557f9.noarch                                                             32/64 
  Verifying        : perl-LWP-Protocol-https-6.07-4.module+el8.6.0+965+850557f9.noarch                                                          33/64 
  Verifying        : perl-NTLM-1.09-17.module+el8.6.0+965+850557f9.noarch                                                                       34/64 
  Verifying        : perl-Net-HTTP-6.17-2.module+el8.6.0+965+850557f9.noarch                                                                    35/64 
  Verifying        : perl-TimeDate-1:2.30-15.module+el8.6.0+965+850557f9.noarch                                                                 36/64 
  Verifying        : perl-Try-Tiny-0.30-7.module+el8.6.0+965+850557f9.noarch                                                                    37/64 
  Verifying        : perl-WWW-RobotRules-6.02-18.module+el8.6.0+965+850557f9.noarch                                                             38/64 
  Verifying        : perl-libwww-perl-6.34-1.module+el8.6.0+965+850557f9.noarch                                                                 39/64 
  Verifying        : postfix-2:3.5.8-4.el8.x86_64                                                                                               40/64 
  Verifying        : python3-chardet-3.0.4-7.el8.noarch                                                                                         41/64 
  Verifying        : python3-condor-10.4.0-1.osg36up.el8.x86_64                                                                                 42/64 
  Verifying        : python3-idna-2.5-5.el8.noarch                                                                                              43/64 
  Verifying        : python3-m2crypto-0.35.2-5.el8.x86_64                                                                                       44/64 
  Verifying        : python3-pysocks-1.6.8-3.el8.noarch                                                                                         45/64 
  Verifying        : python3-requests-2.20.0-2.1.el8_1.noarch                                                                                   46/64 
  Verifying        : python3-urllib3-1.24.2-5.el8.noarch                                                                                        47/64 
  Verifying        : python3-xrootd-1:5.5.5-1.2.osg36.el8.x86_64                                                                                48/64 
  Verifying        : scitokens-cpp-1.0.2-1.el8.x86_64                                                                                           49/64 
  Verifying        : stash-origin-3.5.0-2.osg36.el8.x86_64                                                                                      50/64 
  Verifying        : tcl-1:8.6.8-2.el8.x86_64                                                                                                   51/64 
  Verifying        : vo-client-131-1.osg36.el8.noarch                                                                                           52/64 
  Verifying        : voms-2.1.0-0.14.rc2.6.osg36.el8.x86_64                                                                                     53/64 
  Verifying        : voms-clients-cpp-2.1.0-0.14.rc2.6.osg36.el8.x86_64                                                                         54/64 
  Verifying        : xcache-3.5.0-2.osg36.el8.x86_64                                                                                            55/64 
  Verifying        : xrootd-1:5.5.5-1.2.osg36.el8.x86_64                                                                                        56/64 
  Verifying        : xrootd-client-1:5.5.5-1.2.osg36.el8.x86_64                                                                                 57/64 
  Verifying        : xrootd-client-libs-1:5.5.5-1.2.osg36.el8.x86_64                                                                            58/64 
  Verifying        : xrootd-libs-1:5.5.5-1.2.osg36.el8.x86_64                                                                                   59/64 
  Verifying        : xrootd-scitokens-1:5.5.5-1.2.osg36.el8.x86_64                                                                              60/64 
  Verifying        : xrootd-selinux-1:5.5.5-1.2.osg36.el8.noarch                                                                                61/64 
  Verifying        : xrootd-server-1:5.5.5-1.2.osg36.el8.x86_64                                                                                 62/64 
  Verifying        : xrootd-server-libs-1:5.5.5-1.2.osg36.el8.x86_64                                                                            63/64 
  Verifying        : xrootd-voms-1:5.5.5-1.2.osg36.el8.x86_64                                                                                   64/64 

Removed:
  condor-10.4.0-1.osg36up.el8.x86_64                                          condor-blahp-10.4.0-1.osg36up.el8.x86_64                                
  condor-classads-10.4.0-1.osg36up.el8.x86_64                                 condor-procd-10.4.0-1.osg36up.el8.x86_64                                
  condor-stash-plugin-6.12.1-1.osg36.el8.x86_64                               expect-5.45.4-5.el8.x86_64                                              
  fetch-crl-3.0.22-1.el8.noarch                                               gratia-probe-common-2.8.4-1.osg36.el8.noarch                            
  gratia-probe-condor-ap-2.8.4-1.osg36.el8.noarch                             igtf-ca-certs-1.122-1.osg36.el8.noarch                                  
  libcgroup-0.41-19.el8.x86_64                                                libicu-60.3-2.el8_1.x86_64                                              
  libmacaroons-0.3.0-6.el8.x86_64                                             libsodium-1.0.18-2.el8.x86_64                                           
  mailcap-2.1.48-3.el8.noarch                                                 munge-libs-0.5.13-2.el8.x86_64                                          
  net-tools-2.0-0.52.20160912git.el8.x86_64                                   osg-flock-1.9-2.osg36.el8.noarch                                        
  osg-pki-tools-3.5.2-1.osg36.el8.noarch                                      osg-release-3.6-11.osg36.el8.noarch                                     
  osg-xrootd-3.6-20.osg36.el8.noarch                                          perl-Data-Dump-1.23-7.module+el8.6.0+965+850557f9.noarch                
  perl-Digest-HMAC-1.03-17.module+el8.6.0+965+850557f9.noarch                 perl-File-Listing-6.04-17.module+el8.6.0+965+850557f9.noarch            
  perl-HTML-Parser-3.72-15.module+el8.6.0+965+850557f9.x86_64                 perl-HTML-Tagset-3.20-34.module+el8.6.0+965+850557f9.noarch             
  perl-HTTP-Cookies-6.04-2.module+el8.6.0+965+850557f9.noarch                 perl-HTTP-Date-6.02-19.module+el8.6.0+965+850557f9.noarch               
  perl-HTTP-Message-6.18-1.module+el8.6.0+965+850557f9.noarch                 perl-HTTP-Negotiate-6.01-19.module+el8.6.0+965+850557f9.noarch          
  perl-IO-HTML-1.001-11.module+el8.6.0+965+850557f9.noarch                    perl-LWP-MediaTypes-6.02-15.module+el8.6.0+965+850557f9.noarch          
  perl-LWP-Protocol-https-6.07-4.module+el8.6.0+965+850557f9.noarch           perl-NTLM-1.09-17.module+el8.6.0+965+850557f9.noarch                    
  perl-Net-HTTP-6.17-2.module+el8.6.0+965+850557f9.noarch                     perl-TimeDate-1:2.30-15.module+el8.6.0+965+850557f9.noarch              
  perl-Try-Tiny-0.30-7.module+el8.6.0+965+850557f9.noarch                     perl-WWW-RobotRules-6.02-18.module+el8.6.0+965+850557f9.noarch          
  perl-libwww-perl-6.34-1.module+el8.6.0+965+850557f9.noarch                  postfix-2:3.5.8-4.el8.x86_64                                            
  python3-chardet-3.0.4-7.el8.noarch                                          python3-condor-10.4.0-1.osg36up.el8.x86_64                              
  python3-idna-2.5-5.el8.noarch                                               python3-m2crypto-0.35.2-5.el8.x86_64                                    
  python3-pysocks-1.6.8-3.el8.noarch                                          python3-requests-2.20.0-2.1.el8_1.noarch                                
  python3-urllib3-1.24.2-5.el8.noarch                                         python3-xrootd-1:5.5.5-1.2.osg36.el8.x86_64                             
  scitokens-cpp-1.0.2-1.el8.x86_64                                            stash-origin-3.5.0-2.osg36.el8.x86_64                                   
  tcl-1:8.6.8-2.el8.x86_64                                                    vo-client-131-1.osg36.el8.noarch                                        
  voms-2.1.0-0.14.rc2.6.osg36.el8.x86_64                                      voms-clients-cpp-2.1.0-0.14.rc2.6.osg36.el8.x86_64                      
  xcache-3.5.0-2.osg36.el8.x86_64                                             xrootd-1:5.5.5-1.2.osg36.el8.x86_64                                     
  xrootd-client-1:5.5.5-1.2.osg36.el8.x86_64                                  xrootd-client-libs-1:5.5.5-1.2.osg36.el8.x86_64                         
  xrootd-libs-1:5.5.5-1.2.osg36.el8.x86_64                                    xrootd-scitokens-1:5.5.5-1.2.osg36.el8.x86_64                           
  xrootd-selinux-1:5.5.5-1.2.osg36.el8.noarch                                 xrootd-server-1:5.5.5-1.2.osg36.el8.x86_64                              
  xrootd-server-libs-1:5.5.5-1.2.osg36.el8.x86_64                             xrootd-voms-1:5.5.5-1.2.osg36.el8.x86_64                                

Complete!
[mkandes@nsgosg ~]$
```

Manually removed the following directories to clean up a bit further. 
```
1188  sudo rm -rf /etc/condor/
 1189  sudo rm -rf /etc/xrootd
 1190  sudo rm -rf /etc/gratia/
 1191  sudo rm -rf /etc/ganglia/
 1193  sudo rm -rf /var/log/condor/
 1194 sudo rm -rf /var/log/gratia
```
