#!/usr/bin/env python

import lib
import sys
import os
import getopt

def main(argv=None):
    """
    Usage is:

    delete.py -j jobid [-u url] -d workingdir

    """
    if argv is None:
        argv=sys.argv

    jobid = url = None
    options, remainder = getopt.getopt(argv[1:], "-j:-u:-d:")
    for opt, arg in options:
        if opt in ("-j"):
            jobid = int(arg)
        elif opt in ("-u"):
            url = arg
        elif opt in ("-d"):
            workingdir = arg

    try:
        if not jobid:
            raise SystemError("Internal error, delete.py invoked without jobid.")
        lib.deleteJob(jobid, workingdir)
    except SystemError as theException:
        print >> sys.stderr, "Caught exception:", theException 
        return 1


if __name__ == "__main__":
    sys.exit(main())
    


