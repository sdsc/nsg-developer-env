# Setting up an MPI Cluster
This guide will show you how to set up a two node cluster that is configured to
run OpenMPI across itself.

1. Log in to the [SDSC Cloud](https://dashboard.cloud.sdsc.edu/)
2. Navigate to **Project -> Orchestration -> Stacks** using the menu on the
left.
![Dashboard view of stacks](res/stacks.png)

3. Click **Launch Stack** on the upper right of the screen.
![Dashboard view of stacks](res/launch_stack.png)

4. Change **Template Source** to URL and paste the following URL into
**Template URL**:

```
https://raw.githubusercontent.com/sdsc/nsg-developer-env/master/guides/public/mpi_cluster/res/cluster-template.yaml
```

5. Click **Next**.

6. Fill out the form that shows up:
* **Stack Name** - whatever you would like to name your cluster
* **Password for [username]** - your openstack password
* **Image Name** - the name of the image that you would like to use for
all nodes in the cluster
* **Key Name** - the name of the SSH key that you would like to use to access
nodes in the cluster
* **Network Name** - should be "[project name]s_network" where your replace 
[project name] with the name of your project. This value should be in the upper
left corner.
![Project name example](res/project_name.png)
For example, the project name here is "nsg-dev"

7. Click **Launch**. The stack will create two compute instances called
"nsg-node-1" and "nsg-node-2". You can connect to these nodes via ssh using
the ssh key specified earlier. Use whatever username is default for the image
that you specified earlier. If you specified an nsg-dev image, then the user
should be "ubuntu".

# Destroying an MPI Cluster
1. Log in to the [SDSC Cloud](https://dashboard.cloud.sdsc.edu/)
2. Navigate to **Project -> Orchestration -> Stacks** using the menu on the
left.
![Dashboard view of stacks](res/stacks.png)

3. Select the check mark for the stack that you would like to destroy. Then
click **Delete Stacks** in the upper right. 