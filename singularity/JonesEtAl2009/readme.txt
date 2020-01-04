Code for Simulations in

Jones SR, Pritchett DL, Sikora MA, Stufflebeam SM, Hamalainen M, Moore
CI (2009) Quantitative Analysis and Biophysically Realistic Neural
Modeling of the MEG Mu Rhythm: Rhythmogenesis and Modulation of
Sensory-Evoked Responses. J Neurophysiol 102:3554-72

These files were contributed by Stephanie Jones.
Here is a description of the files:

File: sj10-cortex.hoc
Creates cells and network (grid of layer 5 and layer 2/3 cells - 100
pyramidal neurons and 35 interneurons in each layer).

Contains templates for multi-compartment Layer 5 and Layer 2/3
pyramidal neurons and single compartment inhibitory neurons, and all
synaptic conductances in the SI cortical column model.

Creates a template "FeedX" that is used to externally drive the
network when simulating an "evoked response" (specified in Batch.hoc
and scale_ep_thresh.hoc) and/or an "ongoing mu rhythm" (specified in
MuBurst_10.hoc and E_FFFBx_fixed_10.hoc).

Creates a 2-D grid of cells with all possible connections such that
the inhibitory neurons are placed every 2 pyramidal neurons with
procedure I_zig_zag.

Creates a "dipole current" for each cell (defined in dipole.hoc) and
each layer.

File: wiring_proc_2Dv2.hoc
Procedures for simulating synaptic connections across the local SI
cortical column model.  These are set up with a Gaussian decay profile
for weight and delay from a center of mass in the network. The maximum
weights, min delays, synapse type, and post-synaptic targeted
dendritic compartment numbers are defined in wiring-SmlFeed-3_7.hoc.

File: wiring-SmlFeed-3_7.hoc
Defines the fixed connections within the SI network by specifying
weights, delays, synapse type, and post-synaptic dendritic target
compartments numbers.

File noise2D_v2.hoc
Procedures for simulating ongoing background noise to the network.
The weights are defined in Batch.hoc.

File:  MuBurst_10.hoc
Procedure (make_MuBursts) creates "feedforward (FF)" and
"feedback(FB)" external driving input to the SI cortical column model
(as FeedX objects) simulating an ongoing "mu" rhythms such that the SI
network is driven ever 100ms for (starting at 150ms – to allow the
network to reach a steady state – until 1450) by 10 spiking neurons
(totaling 150 spike driving neurons over a 1500ms simulation, see Fig
2 in Jones et al. 2009). The weight of these inputs and the delay
between FF and FB drive are set in E-FFFBx_10.hoc

File: E_FFFBx_fixed_10.hoc 
Procedure (e_fffbx) defines the weight and delay between the ongoing
FF and FB input to the SI network, with a different weight during the
period in which an evoked response is simulated (550-850ms).

File: scale_ep_thresh.hoc
Defines the properties of the simulated "evoked response" input by
specifying weights, delays, synapse type, and post-synaptic dendritic
target compartments numbers.

File dipole.hoc
Creates a template that defines the "dipole current" for each
cells. The dipole current is the measure of a magnetoencepholography
(MEG) signal.
 
File: batch.hoc 
Calls in all the necessary files, sets default parameters, initial
conditions, and runs the simulations creating 26 runs of a 1500ms
simulation of an ongoing mu rhythm with a simulated evoked response
starting at 450ms.

Folder: STATES
Contains data files for all of the initial conditions. 

Folder: mod_files
The .mod files.  In addition the default hh mechanism is used.

Usage instructions:
This version of the model was parallelized by Michael Hines.  Please
check your NEURON version (the message that neuron outputs when
started).  For example, running nrniv might display NEURON -- VERSION
7.2 (499:91db257165c4) 2011-01-25.  The number before the colon needs
to be greater than or equal to 499 as above.

After unzipping the attached file (on the parallel cluster master) and
cd'ing to the created folder compile the mod files with the command

nrnivmodl mod_files

and then type

mpirun -n 4 nrniv -mpi Batch.hoc

replacing the 4 above with a number of processors that you have
available.

20120409 euler method updated to cnexp in km.mod, kca.mod, cat.mod,
ca.mod, and ar.mod; and updated to derivimplicit in cad.mod as per
http://www.neuron.yale.edu/phpBB/viewtopic.php?f=28&t=592
