#!/usr/bin/env python

import lib
import sys
import os
import sets
import time
import tarfile
import stat

def main(argv=None):
    """
    Usage is:
    
    checkjobs.py
       
    Expects a list of jobs on stdin, one per line. Just the "short id",
    the numeric part. Returns on stdout, the subset of those jobs that
    are no longer running or queued.
    """
    if argv is None:
        argv=sys.argv

    # Want to return jobids that are in queryJobs and not in queuedJobs
    # (i.e. jobs that have finished)
    queryJobs = sys.stdin.readlines()
    queryJobs = [ x.strip() for x in queryJobs if x.strip() != '']

    try:
        queuedJobs = lib.jobInQueue()
    except SystemError, theException:
        print >> sys.stderr, "Caught exception:", theException 
        return 1

    finishedJobs = list(set(queryJobs) - (set(queuedJobs)))
    for j in finishedJobs:
        print j


if __name__ == "__main__":
    sys.exit(main())
