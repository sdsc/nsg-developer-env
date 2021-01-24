#!/usr/bin/env bash

./submit.py id=osg.NeuroscienceGateway https://nsgdev.sdsc.edu:8443/portal2/taskupdate.action?taskId=99997 "$(cat COMMANDLINE)"
