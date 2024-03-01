#!/usr/bin/env python

import lib
import sys
import os
import zipfile
import uu
import stat
import string
import re
import subprocess
import shutil

def main(argv=None):
    """
    Usage is:

    submit.py [id=<chargecode>] <url> <commandline> 

    Run from the working dir of the job, which must contain (in addition
    to the job files) a file named scheduler.conf with scheduler 
    properties for the job.

    id=<chargecode> if present gives the project to charge the job to.
    Url is url of the submitting website including taskid parameter.

    Returns 0 with "jobid=<jobid>" on stdout if job submitted ok
    Returns 1 with multiline error message on stdout if error.
    Returns 2 for the specific error of queue limit exceeded.
    """
    if argv is None:
        argv=sys.argv
    print("argv (%s)" % (argv,))
    debugfile = open('nsgdebug', "w") 
    debugfile.write("argv (%s)\n" % (argv,))
    splits = argv[1].split("=", 1)
    if (len(splits) == 2 and splits[0] == "id"):
        account = splits[1]
        url = argv[2]
        cmdline = argv[3:]
    elif (len(splits) == 1 and splits[0] == "--account"):
        account = argv[2]
        url = argv[4]
        cmdline = argv[6:]
    else:
        print("failed to account information!")
        sys.exit(1)

    job_properties = lib.getProperties('_JOBINFO.TXT')
    print("job_properties['Tool'] (%s)" % job_properties['Tool'])

    tooltype = lib.getToolType(job_properties['Tool'])
    print("tool type is %s" % tooltype)

    # HTCondor does not have the notion of queues and/or partition. This 
    # is simply a place holder value with no meaning.
    queue="condor" 

    # The inputfile archive must currently be unzipped locally prior to
    # job submission. Otherwise, a 'failed to find modeldir!' error will
    # be thrown. However, the inputfile archive must be transferred to a
    # remote OSG site and unzipped locally at the site to run job. As
    # such, it may make more sense to restructure when this 'modeldir!'
    # error is thrown. For example, perhaps at job runtime, not prior to 
    # submission.
    print("New input file used")
    os.system('unzip -n inputfile > /dev/null')

    scheduler_properties = lib.getProperties("scheduler.conf")
    print(scheduler_properties)

    scheduler_info = lib.schedulerInfo(scheduler_properties, tooltype)
    print(scheduler_info)

    hocfile = scheduler_properties['fname']
    if ('outfilename' in scheduler_properties):
        outfilename=scheduler_properties['outfilename']
    else:
        outfilename="output"

    runtime = int(scheduler_info["runtime"])
    useLocalDisk = False

    cwdir = os.getcwd()

    # assume that the modeldir is the only dir in the working dir
    file_list = os.listdir('.')
    modeldir = None
    for filename in file_list:
        stat_tuple = os.lstat(filename)
        if stat.S_ISDIR(stat_tuple[stat.ST_MODE]) and filename != '__MACOSX':
            modeldir = filename
    if modeldir == None:
        print("failed to find modeldir!")
        sys.exit(1)

    if 'subdirname' in scheduler_properties:
        subdirname = scheduler_properties['subdirname']
    else:
        subdirname = None

    if (tooltype != "singularityparametersearch"):
        if subdirname != None:
            modeldir = subdirname

    # What is this section used for? Compiling models/libs on the fly
    # before the job is run? Mostly for neuron only?
    if (tooltype == "neuron77" or (('nrnivmodloption' in scheduler_properties) and scheduler_properties['nrnivmodloption'] == "1")):
        nrnivmodl = '/projects/ps-nsg/home/nsguser/applications_centos7/neuron7.7/nrn-7.7/x86_64/bin/nrnivmodl'
        print("running makelib.sh in %s %s" % (modeldir,nrnivmodl))
        os.system("/projects/ps-nsg/home/nsguser/ngbw/contrib/scripts/makelib.sh %s %s" % (modeldir,nrnivmodl))
    else:
        print("tooltype (%s) not neuron, not running makelib.sh" % tooltype)

    fullpathmodeldir = None



    # # # Create batch_command.cmdline file. # # #
    rfile = open(lib.cmdfile, "w")
    rfile.write("#!/usr/bin/env bash\n")

    # Again, for OSG, you will need to transfer inputfile to remote
    # system and unzip it locally on remote machine before starting
    # standard 'tooltype' commands.
    rfile.write("unzip -n inputfile > /dev/null\n") 

    # # Why does each nsg job allow a custom directory name? Would it
    # not make sense to standardize name based on say a gateway job id?
    rfile.write("cd job_work_dir\n") 

    # Record job's start date and time and then report job start to the
    # gateway frontend.
    rfile.write("echo Job starting at `date` > ../start.txt\n")
    rfile.writelines(("curl %s\&status=START" % (url), "\n"))
    rfile.writelines(("export CIPRES_THREADSPP=%d" % (int(scheduler_info["threads_per_process"])), "\n"))
    rfile.writelines(("export CIPRES_NP=%d" % (int(scheduler_info["ppn"])*int(scheduler_info["nodes"])), "\n"))

    if (tooltype == "bash"):

        rfile.writelines(("printenv\n",))
        rfile.writelines(("lscpu\n",))
        fname, interp, args = cmdline[0].split(" ", 2)
        rfile.writelines(("time -p bash %s %s" % (hocfile,args), "\n"))

    elif (tooltype == "freesurf"):
 
        rfile.writelines(("printenv\n"))
        rfile.writelines(("lscpu\n",))
        rfile.writelines((". /opt/setup.sh\n",)) # Setup osgvo-neuroimaging environment
        rfile.writelines(('export FS_LICENSE="${PWD}/license.txt"\n',))
        rfile.writelines(('export SUBJECTS_DIR="${PWD}/subjects"\n',))
        rfile.writelines(('mkdir -p "${SUBJECTS_DIR}"\n',))
        fname, interp, args = cmdline[0].split(" ", 2)
        rfile.writelines(("time -p recon-all %s" % (args), "\n"))

    elif (tooltype == "python"):

        # OSG is no longer using modules, and the Python environment
        # comes either from the container image, or if you want to make
        # a custom environment with for example Conda. For now,
        # use the environment from Rocky 9:
        # https://github.com/osg-htc/htc-images/blob/main/htc/rocky%3A9/Dockerfile
        rfile.writelines(("printenv\n",))
        rfile.writelines(("lscpu\n",))
        rfname, interp, args = cmdline[0].split(" ", 2)
        rfile.writelines(("time -p python3 %s %s" % (hocfile,args), "\n"))

    elif (tooltype == "tensorflow"):

        rfile.writelines(("printenv\n",))
        rfile.writelines(("lscpu\n",))
        if (scheduler_info['gpus'] == 1):
           rfile.writelines(("nvidia-smi\n",)) 
        fname, interp, args = cmdline[0].split(" ", 2)
        rfile.writelines(("time -p python3 %s %s" % (hocfile,args), "\n"))

    else:

       print('ERROR :: tooltype unknown!')
       sys.exit(1)

    # Record job's end date and time.
    rfile.write("echo Job finished at `date` > ../done.txt\n")

    # Once the main set of job commands have been run, move up and out
    # of the primary job_work_dir ...
    rfile.write("cd ../\n")

    # ... then create a compressed tarball of the job_work_dir and all 
    # other files created during the job. For all compressed tarballs 
    # less than 1GB, the tarball may be transferred back to the job's
    # HTCondor submit node via HTCondor's native file transfer 
    # mechanism. Large file transfers greater than 1GB should use an
    # alternative mechanism such as via globus-url-copy or stachcp. 
    # i.e., eventually there will need to be a rewrite of the logic here
    # to switch between different file transfer mechanisms depending on
    # job type and/or job attributes. For now, we assume only HTCondor 
    # file transfer mechanism will be utilized.
    if (tooltype == "eeglab_tg" or tooltype == "dynasim_tg"):
        rfile.writelines(("/bin/tar -cvzf %s.tar.gz ./%s ./scheduler_stderr.txt ./scheduler_stdout.txt ./stderr.txt ./stdout.txt" % (outfilename, modeldir), "\n"))
    else:
        rfile.writelines(("/bin/tar -cvzf %s.tar.gz ./*" % (outfilename), "\n"))

    # Report job completion to the gateway frontend. 
    rfile.write("curl %s\&status=DONE\n" %  url)

    # # # batch_command.cmdline file creation complete. Close file # # #
    # # # and set file permissions.
    rfile.close()
    os.chmod(lib.cmdfile, 0o744)



    # There is no inherent concept of a max wallclock time in HTCondor.
    # While one could be implemented, on OSG, we should assume all jobs
    # are preemptible. As such, setting wallclock time for jobs can be
    # eliminated for OSG-bound jobs. The following timestring settings
    # were left in the OSG version of the submit.py script for 
    # completeness to compare with the submit.py script for Comet. The 
    # lines can be eliminated, if desired.
    days, remainderminutes = divmod(runtime, 60 * 24)
    hours, remainderminutes = divmod(remainderminutes, 60)
    timestring = '{}-{:02d}:{:02d}:00'.format(days, hours, remainderminutes)


    # # # Create the HTCondor submit description file # # #
    rfile = open(lib.runfile, 'w')
    rfile.writelines(('universe = vanilla\n',))
    rfile.writelines(('executable = batch_command.cmdline\n',))
    #rfile.writelines(('arguments = %s' % (if_batch_command.cmdline_took_args), '\n'))
    rfile.writelines(('request_cpus = %s' % (scheduler_info['threads_per_process']), '\n'))
    rfile.writelines(('request_memory = %s' % (scheduler_info['memory']), '\n'))
    rfile.writelines(('request_disk = %s' % (scheduler_info['disk']), '\n'))
    if (scheduler_info['gpus'] == 1): # OSG currently only supports 1 GPU per job
        rfile.writelines(('request_gpus = 1\n',))
        rfile.writelines(('requirements = '
                          '(Arch == "X86_64") && '
                          '(OpSys == "LINUX") && '
                          '(HAS_SINGULARITY == True)', '\n'))
        rfile.writelines(('require_gpus = '
                          '(Capability >= 7.0), '\n'))'
    else:
        rfile.writelines(('requirements = '
                          '(Arch == "X86_64") && '
                          '(OpSys == "LINUX") && '
                          '(HAS_SINGULARITY == True)', '\n'))
    rfile.writelines(('input = %s' % (fname), '\n'))
    #rfile.writelines(('transfer_input_files = %s' % (if_there_were_other_input_files), '\n'))
    rfile.writelines(('output = scheduler_stdout.txt\n',))
    #rfile.writelines(('transfer_output_files = %s' % (if_wanted_only_subset_of_output_files), '\n'))
    rfile.writelines(('error = scheduler_stderr.txt\n',))
    rfile.writelines(('log = scheduler_stdlog.txt\n',))
    rfile.writelines(('should_transfer_files = YES\n',))
    rfile.writelines(('when_to_transfer_output = ON_EXIT_OR_EVICT\n',))
    rfile.writelines(('notify_user = = %s' % (lib.email), '\n'))
    rfile.writelines(('notification = Always\n',))
    if (tooltype == "freesurf"):
        rfile.writelines(('+SingularityImage = "/cvmfs/singularity.opensciencegrid.org/opensciencegrid/osgvo-freesurfer:latest"', '\n'))
    elif (tooltype == "tensorflow"):
        rfile.writelines(('+SingularityImage = "/cvmfs/singularity.opensciencegrid.org/htc/tensorflow:2.15"', '\n'))
    else:
        rfile.writelines(('+SingularityImage = "/cvmfs/singularity.opensciencegrid.org/htc/rocky:9"', '\n'))
    rfile.writelines(('+ProjectName = "%s"' % (account), '\n'))
    rfile.writelines(('queue 1\n',))
    rfile.close()

    # # # Create epilog file. Is this file needed for OSG integration? # # #
    rfile = open('./epilog', "w")
    rfile.write("#!/usr/bin/env bash\n")
    rfile.writelines(("curl %s\&status=DONE" % (url), "\n"))
    rfile.close()
    os.chmod('./epilog', 0o755)

    # Close nsgdebug file.
    debugfile.close()

    # Submit job to HTCondor.
    return lib.submitJob(partition=queue)
    return 0

if __name__ == "__main__":
    sys.exit(main())
