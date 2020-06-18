# Repo Overview
This repo holds scripts and guides necessary for the nsg-dev platform. The
platform seeks to provide an environment in the SDSC Cloud that is as
close to production as possible. This environment is saved as an image in the
SDSC Cloud. There are [Ansible scripts](https://github.com/sdsc/nsg-developer-env/tree/master/create_image/ansible)
in **create_image** that can be run
against a stock Ubuntu 18.04 image on the SDSC cloud in order to create the
development environment (see the 
[guide](https://github.com/sdsc/nsg-developer-env/tree/master/guides/internal/create_cloud_image)). 

Once the image is created, it needs to be shared to each SDSC Cloud project
that should have access to it (see the
[guide](https://github.com/sdsc/nsg-developer-env/tree/master/guides/internal/share_image)).


## /guides
This folder contains **public** guides meant for end users (developers on the
platform) and **internal** guides meant for those maintaining the platform.

## /create_image
This folder has scripts for creating an image with the nsg-dev stack. See the 
[guide](https://github.com/sdsc/nsg-developer-env/tree/master/guides/internal/create_cloud_image)
for instructions on how to run
the Ansible scripts. Note that **create_image/create_image.py** is an attempt
to automate the image creation process, but never worked 100%. Instead of using
this script, you should follow the guide to manually create the image.