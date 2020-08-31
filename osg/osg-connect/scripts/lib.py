#!/usr/bin/env python

import os
import string
import math
import re
import subprocess
import shutil
import sys
import os.path

# All OSG jobs are single-node jobs. Maximum number of cores per 
# node (or, more correctly, cores per glidein) is currently unknown. 
# However, we can look this up. Average is likely 8 cores per node 
# (glidein).
shared_queue = 'None'
shared_queue_limit = 12.0
max_nodes = 1
cores_per_node = 8
max_cores = max_nodes * cores_per_node
default_cores = cores_per_node
# Include memory related defaults? disk?
#mem_per_core = 4096
#default_mem = cores_per_node * mem_per_core
account = "osg.NeuroscienceGateway"
scheduler_file = "scheduler.conf"
email = "nsgprod@sdsc.edu"
# No max gpus?
jobname = os.environ.get("WB_JOBID", "nsg")
jobdir = os.getcwd()
local_jobdir = "/scratch/${USER}/$SLURM_JOB_ID"
runfile = "./batch_command.run"
statusfile = "./batch_command.status"
cmdfile = "./batch_command.cmdline"
scriptfile = "./batch_command.script"


def getProperties(filename):
    propFile= file( filename, "rU" )
    propDict= dict()
    for propLine in propFile:
        propDef= propLine.strip()
        if len(propDef) == 0:
            continue
        if propDef[0] in ( '!', '#' ):
            continue
        punctuation= [ propDef.find(c) for c in ':= ' ] + [ len(propDef) ]
        found= min( [ pos for pos in punctuation if pos != -1 ] )
        name= propDef[:found].rstrip()
        value= propDef[found:].lstrip(":= ").rstrip()
        propDict[name]= value
    propFile.close()
    return propDict


def getToolType(commandlineString):
    print "Command line string is : %s" % commandlineString
    if re.search(r'bash', "".join(commandlineString).lower()):
        return "bash"
    elif re.search(r'freesurf',"".join(commandlineString).lower()):
        return "freesurf"
    elif re.search(r'py',"".join(commandlineString).lower()):
	return "python"
    elif re.search(r'tensorflow',"".join(commandlineString).lower()):
        return "tensorflow"
    return None 
    

def schedulerInfo(properties, tooltype):
    """ 
    properties is a dictionary containing keys: 

       jobtype, 
       mpi_processes, 
       threads_per_process,
       nodes,
       runhours,
       memory,
       gpus,
       disk.

    Based on properties and hardcoded info about the resource this
    returns a dictionary containing:

       is_mpi,
       queue,
       runtime,
       mpi_processes,
       nodes, 
       ppn

    """
    # There is no built-in, native max wallclock time attribute in 
    # HTCondor. Get runhours from properties and convert it to minutes,
    # default to zero if not specified.
    try:
        runtime  = properties.get("runhours", 0.0)
        runtime = math.ceil(float(runtime) * 60 )
    except:
        runtime = 0.0

    # There is no concept of a 'queue' in HTCondor.
    queue = None

    # Create retval and set values we just determined for runtime and
    # queue.  Set defaults for some if the other retvals which may be
    # overriden below.  Note that for serial jobs we'll need to set 
    # nodes=1 and ppn=1 in the job run script.
    retval = {"queue":queue,
              "nodes": int(properties.get("nodes", 1)),
              "threads_per_process": int(properties.get("threads_per_process", 0)),
              "ppn": int(1),
              "memory":int(properties.get("memory", 4096)),
              "disk":int(properties.get("disk", 8388608)),
              "gpus":int(properties.get("gpus", 0)),
              "runtime":runtime}

    print(retval)

    if properties.get("jobtype") == "direct":
        retval["is_direct"]  = True 
        return retval
    else:
        retval["is_direct"] = False

    if properties.get("jobtype", "")  == "mpi":
        retval["is_mpi"]  = True 
    else:
        retval["is_mpi"] = False 

    if (retval["is_mpi"] == True):
        # Some of our pise xml interfaces just specify the number of mpi
        # processes they want. We round it down to a multiple of the
        # number of cores per node and request enough nodes so that each
        # mpi process has its own core.
        #
        # Not sure if we still have any interfaces like I just described
        # but it's definitely not how we want to run garli here, so
        # explicitly exclude it.  Garli just specifies the number of mpi
        # processes but we always want to use a single node for it.
        if ((properties.get("nodes", "") == "") and 
            (properties.get("thread_per_process", "") == "") and 
            (tooltype != "garli")):
            processes = int(properties.get("mpi_processes", 1))
            processes = int(processes / cores_per_node) * cores_per_node
            processes = min(max(processes, default_cores), max_cores)
            retval["nodes"] = processes / cores_per_node 
            retval["mpi_processes"] = processes 
            retval["ppn"] = int(retval["mpi_processes"]) / int(retval["nodes"]);
        # Pise interfaces that have more knowledge of the specific
        # machine explicitly specify the number of nodes as well as the
        # number of mpi processes; we don't 2nd guess them.
        #elif tooltype in ['pgenesis','neuron','pynn','nest','brian','moose']:
        elif tooltype in ['pgenesis24',
                          'pgenesis',
                          'lsnm_tg', 
                          'rtool_tg',
                          'octave',
                          'neuron74single',
                          'neuron73',
                          'neuron75',
                          'freesurf',
                          'neuron74',
                          'pynn',
                          'nest',
                          'brian',
                          'moose',
                          'neuron73_py',
                          'neuron74_py',
                          'nest_py',
                          'python',
                          'nest_py_as',
                          'bluepyopt',
                          'osbpython',
                          'tensorflow_python',
                          'matlab_tg',
                          'singularityparametersearch',
                          'singularityhnn',
                          'py_tg_centos7',
                          'neuron77']:
            retval["nodes"] = int(properties.get("nodes", 1));
            retval["mpi_processes"] = int(properties.get("mpi_processes", 1));
            #retval["ppn"] = int(retval["mpi_processes"]) / int(retval["nodes"]);
            retval["ppn"] = int(retval["threads_per_process"])
        else:
            retval["nodes"] = int(properties.get("nodes", 1));
            retval["mpi_processes"] = int(properties.get("mpi_processes", 1));
            retval["ppn"] = int(retval["mpi_processes"]) / int(retval["nodes"]);

	if ((tooltype == "carlsim") and 
            (retval["submission_type"] == "0")):
	    retval["queue"] = shared_gpu_queue
        elif ((tooltype == "carlsim") and 
              (retval["submission_type"] == "1")):
	    retval["queue"] = shared_queue
	    
        # Special case for garli.  Run small jobs in shared queue.
        if ((tooltype == "garli") and 
            (retval["mpi_processes"] < cores_per_node)):
            retval["queue"] = shared_queue
            if runtime > shared_queue_limit:
                runtime = shared_queue_limit
                retval["runtime"] = runtime
    else:
        # Special case for small, non-mpi raxml jobs, run in the shared
        # queue. Also for beast.
        if ((retval["nodes"] == 1) and 
            ((retval["threads_per_process"] == 8) or 
             (tooltype == "beast"))):
            queue = shared_queue
            retval["queue"] = queue
            retval["ppn"] = retval["threads_per_process"]
            if runtime > shared_queue_limit:
                runtime = shared_queue_limit
                retval["runtime"] = runtime

    return retval


def log(filename, message):
    f = open(filename, "a")
    f.write(message)
    f.close()


def deleteJob(jobid, workingdir):
    if os.path.isfile(workingdir + "cancelJobs"):
        print "In dependency job cancel"
        os.chdir(workingdir)
        cmd = "./cancelJobs %d" % jobid
    else:
        cmd = "condor_rm %d" % jobid
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, 
                         stderr=subprocess.PIPE)
    outerr = p.communicate()
    output =  outerr[0]
    err = outerr[1]
    if (p.returncode != 0):
        raise SystemError("Error running '%s', return code is %d. stdout is '%s', stderr is '%s'" % (cmd,  
            p.returncode, output, err))


def jobInQueue():
    cmd = 'condor_q -nobatch "$(whoami)" | grep "$(whoami)"'
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, 
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outerr = p.communicate()
    output =  outerr[0]
    err = outerr[1]

    if (len(err) != 0):
        raise SystemError("Error piping qstat thru grep:  %s" % (err))

    output_rows = output.split("\n")
    # Last row in output is empty. This creates an empty element in the
    # list. Remove (.pop()) this empty element to allow jobs.append() to
    # proceed successfully below.
    #
    # Note: This empty list element exists on Comet for Slurm as well. 
    # However, it does not appear to affect call to lib.jobInQueue().
    # Perhaps this is the reason for the comparison of len(r) > r? 
    output_rows.pop()
    jobs = [] 
    for row in output_rows:
        r = row.split()
        # Below, I don't understand the comparison of len(r) > r.
        # len(r) is an integer, while r is a list. Commenting out and 
        # replacing for OSG/HTCondor integration for the time being.
        #if len(r) > r and r[5] != "C":
        if r[5] != "C":
            # Modified jobs.append(r[0]) to return HTCondor job ids
            # as a list of strings that are whole integer values. i.e.,
            # we assume that all HTCondor submit description files set
            # queue = 1, always. No job arrays (queue > 1) are allowed.
            jobs.append(str(int(float(r[0])))) 

    return jobs


def submitJob(partition='condor'):  
    cmd = "condor_submit %s 2>> %s" % (runfile, statusfile)
    print "submit command (%s)" % (cmd,)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)  
    output =  p.communicate()[0]
    retval = p.returncode
    if retval != 0:
        # read HTCondor wrote to the statusfile and print it to stdout
        print "Error submitting job:\n"
        f = open(statusfile, "r"); print f.read(), "\n\n"; f.close()
        print output 
        log(statusfile, "submit_job is returning %d\n" %  retval)
        return retval

    log(statusfile, "condor_submit output is: " + output + "\n" + 
        "======================================================================" +  "\n")

    p = re.compile(r"^1 job\(s\) submitted to cluster (?P<jobid>\d+).", re.M)
    m = p.search(output)
    if m != None:
        jobid = m.group('jobid')
        short_jobid = m.group('jobid')
        print "jobid=%d" % int(short_jobid)
        log(statusfile, "JOBID is %s\n" % jobid)
        log("./_JOBINFO.TXT", "\nJOBID=%s\n" % jobid)
        job_properties = getProperties('_JOBINFO.TXT')
        log("./_JOBINFO.TXT", "\njob_properties (%s)\n" % (job_properties,))
        gatewayuser = string.split(job_properties['User'],'=')[1]
        log("./_JOBINFO.TXT", "\ngatewayuser (%s)\n" % (gatewayuser,))
        resourcespec = 'comet.sdsc.xsede'
	cmd = "curl -XPOST --data @$HOME/.xsede-gateway-attributes-apikey --data-urlencode \"gatewayuser=%s\"  --data-urlencode \"xsederesourcename=%s\" --data-urlencode \"jobid=%s\" --data-urlencode \"submittime=`date '+%%F %%T %%:z'`\" https://xsede-xdcdb-api.xsede.org/gateway/v2/job_attributes" % (gatewayuser, resourcespec, jobid )
        log("./_JOBINFO.TXT", "\ngateway_submit_attributes=%s\n" % cmd)
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        output =  p.communicate()[0]
        retval = p.returncode
        log("./_JOBINFO.TXT", "\ngateway_submit_attributes retval (%s) output (%s)\n" % (retval,output))
        return 0

    else:
        print "Error, condor_submit says: %s" % output
        log(statusfile, "can't get jobid, submit_job is returning 1\n")
        return 1
