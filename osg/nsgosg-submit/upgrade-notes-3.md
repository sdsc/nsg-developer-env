2023/05/02

Upgrading HTCondor and other OSG packages on nsgosg.sdsc.edu after recently running into an authentication problem to the OSPool. In addition to the following upgrades, we were issued a new ospool.token that should support 'capabilities' in HTCondor.

```
[mkandes@nsgosg ~]$ condor_q --version
$CondorVersion: 9.0.17 Oct 04 2022 PackageID: 9.0.17-1.1 $
$CondorPlatform: X86_64-Rocky_8.6 $
[mkandes@nsgosg ~]$
```

```
[mkandes@nsgosg ~]$ yum repolist enabled
repo id                 repo name
SDSC-AppStream          Rocky Linux 8 AppStream
SDSC-BaseOS             Rocky Linux 8 BaseOS
SDSC-extras             Rocky Linux 8 extras
duosecurity             Duo Security Repository
epel                    Extra Packages for Enterprise Linux 8 - x86_64
osg                     OSG Software for Enterprise Linux 8 - x86_64
[mkandes@nsgosg ~]$
```

```
[mkandes@nsgosg ~]$ yum info osg-release
Last metadata expiration check: 0:28:59 ago on Tue 02 May 2023 11:08:44 AM PDT.
Installed Packages
Name         : osg-release
Version      : 3.6
Release      : 11.osg36.el8
Architecture : noarch
Size         : 15 k
Source       : osg-release-3.6-11.osg36.el8.src.rpm
Repository   : @System
From repo    : osg
Summary      : OSG Software for Enterprise Linux repository configuration
URL          : https://repo.opensciencegrid.org/
License      : GPL
Description  : This package contains the OSG Software for Enterprise Linux
             : repository configuration for yum.

[mkandes@nsgosg ~]$
```

```
[mkandes@nsgosg ~]$ sudo yum clean all --enablerepo=*
[sudo] password for mkandes: 
Duo two-factor login for mkandes

Enter a passcode or select one of the following options:

 1. Duo Push to XXX-XXX-7242
 2. SMS passcodes to XXX-XXX-7242

Passcode or option (1-2): 1

Please open Duo Mobile and check for Duo Push requests manually.
Success. Logging you in...
44 files removed
[mkandes@nsgosg ~]$
```

```
[mkandes@nsgosg ~]$ condor_config_val -summary > saved_condor_config_before_upgrade.20230502
[mkandes@nsgosg ~]$
```

```
[mkandes@nsgosg ~]$ sudo yum-config-manager --enable powertools
[mkandes@nsgosg ~]$
```

```
[mkandes@nsgosg ~]$ sudo systemctl stop condor
[mkandes@nsgosg ~]$ sudo systemctl status condor
● condor.service - Condor Distributed High-Throughput-Computing
   Loaded: loaded (/usr/lib/systemd/system/condor.service; enabled; vendor pres>
  Drop-In: /usr/lib/systemd/system/condor.service.d
           └─osg-env.conf
   Active: inactive (dead) since Tue 2023-05-02 11:43:04 PDT; 10s ago
  Process: 498351 ExecStart=/usr/sbin/condor_master -f (code=exited, status=0/S>
 Main PID: 498351 (code=exited, status=0/SUCCESS)
   Status: "All daemons are responding"

May 02 10:56:27 nsgosg.sdsc.edu systemd[1]: Started Condor Distributed High-Thr>
May 02 11:43:03 nsgosg.sdsc.edu systemd[1]: Stopping Condor Distributed High-Th>
May 02 11:43:04 nsgosg.sdsc.edu systemd[1]: condor.service: Succeeded.
May 02 11:43:04 nsgosg.sdsc.edu systemd[1]: Stopped Condor Distributed High-Thr>
[mkandes@nsgosg ~]$
```

```
[mkandes@nsgosg ~]$ sudo systemctl stop gratia-probes-cron
[mkandes@nsgosg ~]$ sudo systemctl status gratia-probes-cron
● gratia-probes-cron.service - SYSV: Enable specified gratia probes to run via >
   Loaded: loaded (/etc/rc.d/init.d/gratia-probes-cron; generated)
   Active: inactive (dead)
     Docs: man:systemd-sysv-generator(8)
[mkandes@nsgosg ~]$
```

```
[mkandes@nsgosg ~]$ sudo yum update
Rocky Linux 8 AppStream                          69 MB/s |  11 MB     00:00    
Rocky Linux 8 BaseOS                             80 MB/s | 6.1 MB     00:00    
Rocky Linux 8 extras                            502 kB/s |  14 kB     00:00    
OSG Software for Enterprise Linux 8 - x86_64    1.7 MB/s | 1.8 MB     00:01    
Rocky Linux 8 - PowerTools                      3.4 MB/s | 2.8 MB     00:00    
Duo Security Repository                          28 kB/s | 2.0 kB     00:00    
Extra Packages for Enterprise Linux 8 - x86_64  2.3 MB/s |  14 MB     00:05    
Dependencies resolved.
================================================================================
 Package               Arch        Version               Repository        Size
================================================================================
Upgrading:
 emacs-filesystem      noarch      1:26.1-7.el8_7.1      SDSC-BaseOS       69 k

Transaction Summary
================================================================================
Upgrade  1 Package

Total download size: 69 k
Is this ok [y/N]: y
Downloading Packages:
emacs-filesystem-26.1-7.el8_7.1.noarch.rpm      2.7 MB/s |  69 kB     00:00    
--------------------------------------------------------------------------------
Total                                           2.3 MB/s |  69 kB     00:00     
Running transaction check
Transaction check succeeded.
Running transaction test
Transaction test succeeded.
Running transaction
  Preparing        :                                                        1/1 
  Upgrading        : emacs-filesystem-1:26.1-7.el8_7.1.noarch               1/2 
  Cleanup          : emacs-filesystem-1:26.1-7.el8.noarch                   2/2 
  Verifying        : emacs-filesystem-1:26.1-7.el8_7.1.noarch               1/2 
  Verifying        : emacs-filesystem-1:26.1-7.el8.noarch                   2/2 

Upgraded:
  emacs-filesystem-1:26.1-7.el8_7.1.noarch                                      

Complete!
[mkandes@nsgosg ~]$
```

```
[mkandes@nsgosg ~]$ yum info condor
Rocky Linux 8 - PowerTools                      3.4 MB/s | 2.8 MB     00:00    
Installed Packages
Name         : condor
Version      : 9.0.17
Release      : 1.1.osg36.el8
Architecture : x86_64
Size         : 21 M
Source       : condor-9.0.17-1.1.osg36.el8.src.rpm
Repository   : @System
From repo    : osg
Summary      : HTCondor: High Throughput Computing
URL          : http://www.cs.wisc.edu/condor/
License      : ASL 2.0
Description  : HTCondor is a specialized workload management system for
             : compute-intensive jobs. Like other full-featured batch systems, HTCondor
             : provides a job queueing mechanism, scheduling policy, priority scheme,
             : resource monitoring, and resource management. Users submit their
             : serial or parallel jobs to HTCondor, HTCondor places them into a queue,
             : chooses when and where to run the jobs based upon a policy, carefully
             : monitors their progress, and ultimately informs the user upon
             : completion.

[mkandes@nsgosg ~]$
```

```
[mkandes@nsgosg ~]$ yum info --enablerepo=osg-upcoming condor
Last metadata expiration check: 0:01:06 ago on Tue 02 May 2023 11:46:59 AM PDT.
Installed Packages
Name         : condor
Version      : 9.0.17
Release      : 1.1.osg36.el8
Architecture : x86_64
Size         : 21 M
Source       : condor-9.0.17-1.1.osg36.el8.src.rpm
Repository   : @System
From repo    : osg
Summary      : HTCondor: High Throughput Computing
URL          : http://www.cs.wisc.edu/condor/
License      : ASL 2.0
Description  : HTCondor is a specialized workload management system for
             : compute-intensive jobs. Like other full-featured batch systems,
             : HTCondor provides a job queueing mechanism, scheduling policy,
             : priority scheme, resource monitoring, and resource management.
             : Users submit their serial or parallel jobs to HTCondor, HTCondor
             : places them into a queue, chooses when and where to run the jobs
             : based upon a policy, carefully monitors their progress, and
             : ultimately informs the user upon completion.

Available Packages
Name         : condor
Version      : 10.4.0
Release      : 1.osg36up.el8
Architecture : x86_64
Size         : 8.3 M
Source       : condor-10.4.0-1.osg36up.el8.src.rpm
Repository   : osg-upcoming
Summary      : HTCondor: High Throughput Computing
URL          : https://www.cs.wisc.edu/htcondor/
License      : ASL 2.0
Description  : HTCondor is a specialized workload management system for
             : compute-intensive jobs. Like other full-featured batch systems,
             : HTCondor provides a job queueing mechanism, scheduling policy,
             : priority scheme, resource monitoring, and resource management.
             : Users submit their serial or parallel jobs to HTCondor, HTCondor
             : places them into a queue, chooses when and where to run the jobs
             : based upon a policy, carefully monitors their progress, and
             : ultimately informs the user upon completion.

[mkandes@nsgosg ~]$
```

```
[mkandes@nsgosg ~]$ yum --enablerepo=osg-upcoming,osg-testing --showduplicates list condor
OSG Software for Enterprise Linux 8 - Testing - 267 kB/s | 239 kB     00:00    
Installed Packages
condor.x86_64                9.0.17-1.1.osg36.el8                   @osg        
Available Packages
condor.x86_64                9.0.0-1.5.osg36.el8                    osg         
condor.x86_64                9.0.1-1.2.osg36.el8                    osg         
condor.x86_64                9.0.2-1.1.osg36.el8                    osg         
condor.x86_64                9.0.4-1.1.osg36.el8                    osg         
condor.x86_64                9.0.5-1.osg36.el8                      osg         
condor.x86_64                9.0.6-1.osg36.el8                      osg         
condor.x86_64                9.0.7-1.osg36.el8                      osg         
condor.x86_64                9.0.8-1.osg36.el8                      osg         
condor.x86_64                9.0.9-1.osg36.el8                      osg         
condor.x86_64                9.0.10-1.osg36.el8                     osg         
condor.x86_64                9.0.11-1.osg36.el8                     osg         
condor.x86_64                9.0.12-1.1.osg36.el8                   osg         
condor.x86_64                9.0.13-1.1.osg36.el8                   osg         
condor.x86_64                9.0.15-1.1.osg36.el8                   osg         
condor.x86_64                9.0.16-1.1.osg36.el8                   osg         
condor.x86_64                9.0.17-1.1.osg36.el8                   osg         
condor.x86_64                9.1.0-1.2.osg36up.el8                  osg-upcoming
condor.x86_64                9.1.2-1.1.osg36up.el8                  osg-upcoming
condor.x86_64                9.2.0-1.osg36up.el8                    osg-upcoming
condor.x86_64                9.3.0-1.osg36up.el8                    osg-upcoming
condor.x86_64                9.4.0-1.osg36up.el8                    osg-upcoming
condor.x86_64                9.6.0-1.osg36up.el8                    osg-upcoming
condor.x86_64                9.7.0-1.osg36up.el8                    osg-upcoming
condor.x86_64                9.8.1-1.osg36up.el8                    osg-upcoming
condor.x86_64                9.9.1-1.osg36up.el8                    osg-upcoming
condor.x86_64                9.10.1-1.osg36up.el8                   osg-upcoming
condor.x86_64                9.11.0-1.osg36up.el8                   osg-upcoming
condor.x86_64                9.12.0-1.1.osg36up.el8                 osg-upcoming
condor.x86_64                10.0.3-1.osg36.el8                     osg-testing 
condor.x86_64                10.4.0-1.osg36up.el8                   osg-upcoming
[mkandes@nsgosg ~]$
```

```
[mkandes@nsgosg ~]$ sudo yum upgrade --enablerepo=osg-upcoming condor
[sudo] password for mkandes: 
Duo two-factor login for mkandes

Enter a passcode or select one of the following options:

 1. Duo Push to XXX-XXX-7242
 2. SMS passcodes to XXX-XXX-7242

Passcode or option (1-2): 1

Please open Duo Mobile and check for Duo Push requests manually.
Success. Logging you in...
OSG Software for Enterprise Linux 8 - Upcoming  287 kB/s | 279 kB     00:00    
Dependencies resolved.
================================================================================
 Package                Arch      Version                 Repository       Size
================================================================================
Upgrading:
 condor                 x86_64    10.4.0-1.osg36up.el8    osg-upcoming    8.3 M
 condor-classads        x86_64    10.4.0-1.osg36up.el8    osg-upcoming    342 k
 condor-procd           x86_64    10.4.0-1.osg36up.el8    osg-upcoming    179 k
 python3-condor         x86_64    10.4.0-1.osg36up.el8    osg-upcoming    832 k
Installing dependencies:
 condor-blahp           x86_64    10.4.0-1.osg36up.el8    osg-upcoming    391 k
     replacing  blahp.x86_64 2.2.1-1.osg36.el8
 condor-stash-plugin    x86_64    6.10.0-1.osg36.el8      osg             2.2 M

Transaction Summary
================================================================================
Install  2 Packages
Upgrade  4 Packages

Total download size: 12 M
Is this ok [y/N]: y
Downloading Packages:
                    186% [=====================================] 1.4 kB/s | 496 (1/6): condor-procd-10.4.0-1.osg36up.el8.x86_64 393 kB/s | 179 kB     00:00    
(2/6): condor-blahp-10.4.0-1.osg36up.el8.x86_64 775 kB/s | 391 kB     00:00    
(3/6): condor-stash-plugin-6.10.0-1.osg36.el8.x 3.2 MB/s | 2.2 MB     00:00    
(4/6): python3-condor-10.4.0-1.osg36up.el8.x86_ 3.4 MB/s | 832 kB     00:00    
(5/6): condor-classads-10.4.0-1.osg36up.el8.x86 2.9 MB/s | 342 kB     00:00    
(6/6): condor-10.4.0-1.osg36up.el8.x86_64.rpm    20 MB/s | 8.3 MB     00:00    
--------------------------------------------------------------------------------
Total                                            10 MB/s |  12 MB     00:01     
Running transaction check
Transaction check succeeded.
Running transaction test
Transaction test succeeded.
Running transaction
  Preparing        :                                                                                                                                              1/1 
  Running scriptlet: condor-classads-10.4.0-1.osg36up.el8.x86_64                                                                                                  1/1 
  Upgrading        : condor-classads-10.4.0-1.osg36up.el8.x86_64                                                                                                 1/11 
  Upgrading        : condor-procd-10.4.0-1.osg36up.el8.x86_64                                                                                                    2/11 
  Installing       : condor-blahp-10.4.0-1.osg36up.el8.x86_64                                                                                                    3/11 
  Upgrading        : python3-condor-10.4.0-1.osg36up.el8.x86_64                                                                                                  4/11 
  Running scriptlet: condor-10.4.0-1.osg36up.el8.x86_64                                                                                                          5/11 
  Upgrading        : condor-10.4.0-1.osg36up.el8.x86_64                                                                                                          5/11 
  Running scriptlet: condor-10.4.0-1.osg36up.el8.x86_64                                                                                                          5/11 
Boolean condor_domain_can_network_connect is not defined

  Installing       : condor-stash-plugin-6.10.0-1.osg36.el8.x86_64                                                                                               6/11 
  Running scriptlet: condor-9.0.17-1.1.osg36.el8.x86_64                                                                                                          7/11 
  Cleanup          : condor-9.0.17-1.1.osg36.el8.x86_64                                                                                                          7/11 
  Running scriptlet: condor-9.0.17-1.1.osg36.el8.x86_64                                                                                                          7/11 
  Running scriptlet: blahp-2.2.1-1.osg36.el8.x86_64                                                                                                              8/11 
  Obsoleting       : blahp-2.2.1-1.osg36.el8.x86_64                                                                                                              8/11 
  Cleanup          : python3-condor-9.0.17-1.1.osg36.el8.x86_64                                                                                                  9/11 
  Cleanup          : condor-classads-9.0.17-1.1.osg36.el8.x86_64                                                                                                10/11 
  Cleanup          : condor-procd-9.0.17-1.1.osg36.el8.x86_64                                                                                                   11/11 
  Running scriptlet: condor-procd-9.0.17-1.1.osg36.el8.x86_64                                                                                                   11/11 
  Verifying        : condor-stash-plugin-6.10.0-1.osg36.el8.x86_64                                                                                               1/11 
  Verifying        : condor-blahp-10.4.0-1.osg36up.el8.x86_64                                                                                                    2/11 
  Verifying        : blahp-2.2.1-1.osg36.el8.x86_64                                                                                                              3/11 
  Verifying        : condor-procd-10.4.0-1.osg36up.el8.x86_64                                                                                                    4/11 
  Verifying        : condor-procd-9.0.17-1.1.osg36.el8.x86_64                                                                                                    5/11 
  Verifying        : condor-10.4.0-1.osg36up.el8.x86_64                                                                                                          6/11 
  Verifying        : condor-9.0.17-1.1.osg36.el8.x86_64                                                                                                          7/11 
  Verifying        : python3-condor-10.4.0-1.osg36up.el8.x86_64                                                                                                  8/11 
  Verifying        : python3-condor-9.0.17-1.1.osg36.el8.x86_64                                                                                                  9/11 
  Verifying        : condor-classads-10.4.0-1.osg36up.el8.x86_64                                                                                                10/11 
  Verifying        : condor-classads-9.0.17-1.1.osg36.el8.x86_64                                                                                                11/11 

Upgraded:
  condor-10.4.0-1.osg36up.el8.x86_64 condor-classads-10.4.0-1.osg36up.el8.x86_64 condor-procd-10.4.0-1.osg36up.el8.x86_64 python3-condor-10.4.0-1.osg36up.el8.x86_64
Installed:
  condor-blahp-10.4.0-1.osg36up.el8.x86_64                                        condor-stash-plugin-6.10.0-1.osg36.el8.x86_64                                       

Complete!
[mkandes@nsgosg ~]$
```
