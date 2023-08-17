2023/08/17

Continuing from `upgrade-notes-3.md`, we're again attempting to fix the authentication issue with nsgosg.sdsc.edu. In addition, RDS has created and NFS share for the `xrootd` user on their OSDF origin server, which we should now be able to use to export data to via this share. As such, we need to get it mounted as well. 
