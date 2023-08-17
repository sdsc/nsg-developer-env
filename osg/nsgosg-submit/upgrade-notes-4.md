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
