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

