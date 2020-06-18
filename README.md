# Repo Overview

## guides
This folder contains **public** guides meant for end users (developers on the
platform) and **internal** guides meant for those maintaining the platform.

## create_image
This folder has scripts for creating an image with the nsg-dev stack. See the 
guide in **guides/internal/create_cloud_image** for instructions on how to run
the Ansible scripts. Note that **create_image/create_image.py** is an attempt
to automate the image creation process, but never worked 100%. Instead of using
this script, you should follow the guide to manually create the image.