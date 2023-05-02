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
