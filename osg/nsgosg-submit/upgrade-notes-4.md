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
