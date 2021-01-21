#!/usr/bin/env bash
#
# Configure OSG submit node
#
# All commands run interactively as root on nsgosg.sdsc.edu to complete
# its initial configuration as an HTCondor submit node that is capable 
# of submitting jobs to the Open Science Grid (OSG). Please note that 
# this bash script did not exist at the time of configuration. It was 
# create after the fact to document the configuration process such that
# this script may serve as an outline for how such a configuration 
# script may be constructed in the future should the Neuroscience
# Gateway (NSG) project need to replicate and/or automate the deployment
# of the submit node.
#
# Related documentation: https://opensciencegrid.org/docs/submit/osg-flock
# 
# IMPORTANT: Below you'll see the use of non-production OSG rpm repos 
#            such as osg-upcoming-testing and osg-development. These 
#            non-production repos were utilized during the initial 
#            configuration of the NSG submit node because CentOS 8 
#            support was still new for HTCondor and OSG at the time.

yum -y clean all --enablerepo=*
yum -y update
yum -y install epel-release
yum -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm
yum -y install https://repo.opensciencegrid.org/osg/3.5/osg-3.5-el8-release-latest.rpm

echo 'upgrade_type = security' > /etc/dnf/automatic.conf

yum -y install http://mirror.centos.org/centos/8/PowerTools/x86_64/os/Packages/boost-python3-1.66.0-10.el8.x86_64.rpm

yum install condor --enablerepo=osg-upcoming-testing

yum -y install wget

cd /etc/condor/config.d/
wget https://raw.githubusercontent.com/opensciencegrid/osg-flock/master/rpm/80-osg-flocking.conf

echo 'ProjectName = "NeuroscienceGateway"' > /etc/condor/config.d/95-nsg-submit-attrs.config
echo 'SUBMIT_EXPRS = $(SUBMIT_EXPRS) ProjectName' >> /etc/condor/config.d/95-nsg-submit-attrs.config

cd /etc/condor/tokens.d/
echo '<INSERT TOKEN HERE>' > /etc/condor/tokens.d/flock.opensciencegrid.org
chown condor:condor flock.opensciencegrid.org
chmod go-r flock.opensciencegrid.org

yum -y install osg-flock --enablerepo=osg-development

cd /etc/gratia/condor/
mv ProbeConfig ProbeConfig.bak
mv ProbeConfig-flocking ProbeConfig
sed -i 's/ProbeName="condor:<HOSTNAME>"/ProbeName="condor:nsgosg.sdsc.edu"/' ProbeConfig
sed -i 's/SiteName="OSG_US_EXAMPLE_SUBMIT"/SiteName="SDSC"/' ProbeConfig
sed -i 's/EnableProbe="0"/EnableProbe="1"/' ProbeConfig
sed -i 's/MapUnknownToGroup="0"/MapUnknownToGroup="1"/' ProbeConfig
sed -i 's/MapGroupToRole="0"/MapGroupToRole="1"/' ProbeConfig
sed -i 's/VOOverride="OSG"/VOOverride="OSG"/' ProbeConfig

yum -y update gratia* --enablerepo=osg-testing

chkconfig gratia-probes-cron on
systemctl start gratia-probes-cron
systemctl status gratia-probes-cron

systemctl start condor
systemctl status condor
condor_reconfig
